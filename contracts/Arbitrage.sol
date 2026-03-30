// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @dev Minimal interface required to interact with the DEX contract.
interface IDEX {
    function swapAforB(uint256 amountAIn) external returns (uint256 amountBOut);
    function swapBforA(uint256 amountBIn) external returns (uint256 amountAOut);
    function spotPrice()  external view returns (uint256);   // B per A ×1e18
    function getReserves() external view returns (uint256 reserveA, uint256 reserveB);
}

/**
 * @title Arbitrage
 * @notice Detects and executes two-hop cross-DEX arbitrage between two instances
 *         of the DEX contract that share the same TokenA / TokenB pair.
 *
 * Two directions are supported:
 *   Direction 0 (AtoB):  TokenA → TokenB on DEX1, TokenB → TokenA on DEX2
 *   Direction 1 (BtoA):  TokenB → TokenA on DEX1, TokenA → TokenB on DEX2
 *
 * Opportunity condition (see eq. 3 in assignment):
 *   reserveA_dex1 / reserveB_dex1  ≠  reserveA_dex2 / reserveB_dex2
 *
 * The contract holds initial capital in TokenA or TokenB (sent by owner).
 * All profit + capital is returned to the owner after each successful execution.
 *
 * Security:
 *   - onlyOwner on execute functions
 *   - Simulates trade off-chain (view) before executing to avoid wasted gas
 *   - Reverts the entire transaction if profit < MIN_PROFIT_THRESHOLD
 */
contract Arbitrage is Ownable {

    uint256 public constant FEE_NUMERATOR   = 997;
    uint256 public constant FEE_DENOMINATOR = 1000;

    /// Minimum profit required to execute arbitrage (0.001 token in wei units).
    uint256 public minProfitThreshold = 1e15;

    event ArbitrageExecuted(
        address indexed dex1,
        address indexed dex2,
        uint256 amountIn,
        uint256 profit,
        bool    directionAtoB
    );

    constructor() Ownable(msg.sender) {}

    // ──────────────────────────────────────────────────────────────────
    // Owner configuration
    // ──────────────────────────────────────────────────────────────────

    function setMinProfitThreshold(uint256 threshold) external onlyOwner {
        minProfitThreshold = threshold;
    }

    // ──────────────────────────────────────────────────────────────────
    // Off-chain simulation helpers  (view - no gas, safe to call freely)
    // ──────────────────────────────────────────────────────────────────

    /**
     * @notice Compute expected output of a single AMM swap (mirrors DEX formula).
     * @param amountIn  Token input amount.
     * @param rIn       Reserve of input token.
     * @param rOut      Reserve of output token.
     * @return amountOut  Expected output amount.
     */
    function _calcOut(uint256 amountIn, uint256 rIn, uint256 rOut)
        internal pure returns (uint256 amountOut)
    {
        uint256 aWithFee = amountIn * FEE_NUMERATOR;
        amountOut = (rOut * aWithFee) / (rIn * FEE_DENOMINATOR + aWithFee);
    }

    /**
     * @notice Check whether an arbitrage opportunity exists and estimate profit.
     * @param dex1         Address of the first DEX contract.
     * @param dex2         Address of the second DEX contract.
     * @param amountIn     Capital to deploy (in TokenA for directionAtoB, TokenB otherwise).
     * @param directionAtoB  true = A→B on dex1 then B→A on dex2;
     *                       false = B→A on dex1 then A→B on dex2.
     * @return profitable      Whether profit > minProfitThreshold.
     * @return expectedProfit  Estimated gross profit (same token as amountIn).
     */
    function checkArbitrage(
        address dex1,
        address dex2,
        uint256 amountIn,
        bool    directionAtoB
    ) external view returns (bool profitable, uint256 expectedProfit) {
        (uint256 r1A, uint256 r1B) = IDEX(dex1).getReserves();
        (uint256 r2A, uint256 r2B) = IDEX(dex2).getReserves();

        uint256 finalOut;
        if (directionAtoB) {
            // A→B on DEX1, then B→A on DEX2
            uint256 bOut = _calcOut(amountIn, r1A, r1B);
            finalOut     = _calcOut(bOut,     r2B, r2A);
        } else {
            // B→A on DEX1, then A→B on DEX2
            uint256 aOut = _calcOut(amountIn, r1B, r1A);
            finalOut     = _calcOut(aOut,     r2A, r2B);
        }

        if (finalOut > amountIn + minProfitThreshold) {
            profitable     = true;
            expectedProfit = finalOut - amountIn;
        }
    }

    // ──────────────────────────────────────────────────────────────────
    // Execution
    // ──────────────────────────────────────────────────────────────────

    /**
     * @notice Execute arbitrage between two DEX contracts.
     *         Reverts if profit < minProfitThreshold ("Failed arbitrage").
     *
     * @param dex1          First DEX address.
     * @param dex2          Second DEX address.
     * @param tokenA        Address of TokenA.
     * @param tokenB        Address of TokenB.
     * @param amountIn      Capital to deploy.
     * @param directionAtoB true  → swap A→B on dex1, B→A on dex2
     *                      false → swap B→A on dex1, A→B on dex2
     * @return profit  Tokens earned above the initial capital.
     */
    function executeArbitrage(
        address dex1,
        address dex2,
        address tokenA,
        address tokenB,
        uint256 amountIn,
        bool    directionAtoB
    ) external onlyOwner returns (uint256 profit) {

        // ── 1. Simulate off-chain to decide whether to proceed ──────
        (uint256 r1A, uint256 r1B) = IDEX(dex1).getReserves();
        (uint256 r2A, uint256 r2B) = IDEX(dex2).getReserves();

        uint256 finalOut;
        if (directionAtoB) {
            uint256 bOut = _calcOut(amountIn, r1A, r1B);
            finalOut     = _calcOut(bOut,     r2B, r2A);
        } else {
            uint256 aOut = _calcOut(amountIn, r1B, r1A);
            finalOut     = _calcOut(aOut,     r2A, r2B);
        }

        require(
            finalOut > amountIn + minProfitThreshold,
            "Arbitrage: insufficient profit - opportunity does not exist"
        );

        profit = finalOut - amountIn;

        // ── 2. Execute swaps ────────────────────────────────────────
        if (directionAtoB) {
            // Step A: TokenA → TokenB on DEX1
            IERC20(tokenA).approve(dex1, amountIn);
            uint256 bReceived = IDEX(dex1).swapAforB(amountIn);

            // Step B: TokenB → TokenA on DEX2
            IERC20(tokenB).approve(dex2, bReceived);
            IDEX(dex2).swapBforA(bReceived);

            // Return all TokenA (capital + profit) to owner
            uint256 bal = IERC20(tokenA).balanceOf(address(this));
            require(bal >= amountIn, "Arbitrage: unexpected loss - aborting");
            IERC20(tokenA).transfer(owner(), bal);

        } else {
            // Step A: TokenB → TokenA on DEX1
            IERC20(tokenB).approve(dex1, amountIn);
            uint256 aReceived = IDEX(dex1).swapBforA(amountIn);

            // Step B: TokenA → TokenB on DEX2
            IERC20(tokenA).approve(dex2, aReceived);
            IDEX(dex2).swapAforB(aReceived);

            // Return all TokenB (capital + profit) to owner
            uint256 bal = IERC20(tokenB).balanceOf(address(this));
            require(bal >= amountIn, "Arbitrage: unexpected loss - aborting");
            IERC20(tokenB).transfer(owner(), bal);
        }

        emit ArbitrageExecuted(dex1, dex2, amountIn, profit, directionAtoB);
    }

    // ──────────────────────────────────────────────────────────────────
    // Fund management  (owner deposits/withdraws capital)
    // ──────────────────────────────────────────────────────────────────

    /// @notice Deposit ERC-20 tokens into this contract to use as arbitrage capital.
    function depositToken(address token, uint256 amount) external onlyOwner {
        IERC20(token).transferFrom(msg.sender, address(this), amount);
    }

    /// @notice Withdraw any ERC-20 tokens (e.g. to recover stuck funds).
    function withdrawToken(address token, uint256 amount) external onlyOwner {
        IERC20(token).transfer(owner(), amount);
    }
}
