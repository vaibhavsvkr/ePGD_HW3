// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./LPToken.sol";

/**
 * @title DEX - Constant-Product Automated Market Maker
 * @notice Implements a Uniswap-v2-style AMM for a TokenA / TokenB pair.
 *
 * Core invariant:  reserveA × reserveB = k  (enforced during swaps)
 * Swap fee:        0.3%  (997 / 1000 of input is effectively used)
 *
 * Security measures (see report section):
 *   1. ReentrancyGuard on all state-changing functions
 *   2. Solidity 0.8+ checked arithmetic (no SafeMath needed)
 *   3. require() guards on all inputs and state preconditions
 *   4. LPToken minting/burning restricted to this contract (Ownable)
 *   5. Token transfers verified via return value
 *   6. Reserves updated BEFORE external token transfers (Checks-Effects-Interactions)
 *   7. immutable token addresses prevent post-deployment tampering
 */
contract DEX is ReentrancyGuard {

    // ──────────────────────────────────────────────────────────────────
    // State variables
    // ──────────────────────────────────────────────────────────────────

    IERC20  public immutable tokenA;
    IERC20  public immutable tokenB;
    LPToken public immutable lpToken;

    uint256 public reserveA;
    uint256 public reserveB;

    // 0.3% fee: effective input = amountIn * 997 / 1000
    uint256 public constant FEE_NUMERATOR   = 997;
    uint256 public constant FEE_DENOMINATOR = 1000;

    // Cumulative fees retained in the pool (informational; not withdrawn separately)
    uint256 public totalFeesA;
    uint256 public totalFeesB;

    // ──────────────────────────────────────────────────────────────────
    // Events
    // ──────────────────────────────────────────────────────────────────

    event LiquidityAdded(
        address indexed provider,
        uint256 amountA,
        uint256 amountB,
        uint256 lpMinted
    );
    event LiquidityRemoved(
        address indexed provider,
        uint256 amountA,
        uint256 amountB,
        uint256 lpBurned
    );
    event Swap(
        address indexed trader,
        address indexed tokenIn,
        uint256 amountIn,
        uint256 amountOut
    );

    // ──────────────────────────────────────────────────────────────────
    // Constructor - deploys its own LPToken so DEX is the sole minter
    // ──────────────────────────────────────────────────────────────────

    constructor(address _tokenA, address _tokenB) {
        require(_tokenA != address(0) && _tokenB != address(0), "DEX: zero address");
        require(_tokenA != _tokenB, "DEX: identical tokens");
        tokenA  = IERC20(_tokenA);
        tokenB  = IERC20(_tokenB);
        lpToken = new LPToken();   // DEX contract is LPToken.owner()
    }

    // ──────────────────────────────────────────────────────────────────
    // Liquidity operations
    // ──────────────────────────────────────────────────────────────────

    /**
     * @notice Deposit TokenA and TokenB into the pool.
     *         The first depositor sets the ratio; subsequent deposits must
     *         preserve the existing ratio (amountA / amountB == reserveA / reserveB).
     * @param amountA  Amount of TokenA to deposit.
     * @param amountB  Amount of TokenB to deposit (must satisfy ratio).
     * @return lpMinted  LP tokens issued to the caller.
     */
    function addLiquidity(uint256 amountA, uint256 amountB)
        external
        nonReentrant
        returns (uint256 lpMinted)
    {
        require(amountA > 0 && amountB > 0, "DEX: amounts must be > 0");

        uint256 totalLP = lpToken.totalSupply();

        if (totalLP == 0) {
            // ── First deposit: caller sets the price ratio ──────────
            lpMinted = amountA;   // LP amount = amountA (18-decimal aligned)
        } else {
            // ── Subsequent deposits must preserve ratio ──────────────
            // Required: amountA * reserveB == amountB * reserveA
            require(
                amountA * reserveB == amountB * reserveA,
                "DEX: ratio mismatch - adjust token amounts to match current pool ratio"
            );
            lpMinted = (amountA * totalLP) / reserveA;
        }

        require(lpMinted > 0, "DEX: zero LP minted");

        // Checks-Effects-Interactions: update state before external calls
        reserveA += amountA;
        reserveB += amountB;

        require(tokenA.transferFrom(msg.sender, address(this), amountA), "DEX: TokenA transfer failed");
        require(tokenB.transferFrom(msg.sender, address(this), amountB), "DEX: TokenB transfer failed");

        lpToken.mint(msg.sender, lpMinted);

        emit LiquidityAdded(msg.sender, amountA, amountB, lpMinted);
    }

    /**
     * @notice Burn LP tokens and receive proportional TokenA + TokenB.
     * @param lpAmount  Amount of LP tokens to burn.
     * @return amountA  TokenA returned.
     * @return amountB  TokenB returned.
     */
    function removeLiquidity(uint256 lpAmount)
        external
        nonReentrant
        returns (uint256 amountA, uint256 amountB)
    {
        require(lpAmount > 0, "DEX: lpAmount must be > 0");

        uint256 totalLP = lpToken.totalSupply();
        require(totalLP > 0, "DEX: pool is empty");
        require(lpToken.balanceOf(msg.sender) >= lpAmount, "DEX: insufficient LP balance");

        amountA = (lpAmount * reserveA) / totalLP;
        amountB = (lpAmount * reserveB) / totalLP;
        require(amountA > 0 && amountB > 0, "DEX: withdrawal too small");

        // Checks-Effects-Interactions
        reserveA -= amountA;
        reserveB -= amountB;

        lpToken.burn(msg.sender, lpAmount);

        require(tokenA.transfer(msg.sender, amountA), "DEX: TokenA transfer failed");
        require(tokenB.transfer(msg.sender, amountB), "DEX: TokenB transfer failed");

        emit LiquidityRemoved(msg.sender, amountA, amountB, lpAmount);
    }

    // ──────────────────────────────────────────────────────────────────
    // Swap operations  (constant product:  x * y = k)
    // ──────────────────────────────────────────────────────────────────

    /**
     * @notice Swap TokenA for TokenB.
     *         Output: dy = reserveB * (amountIn*997) / (reserveA*1000 + amountIn*997)
     * @param amountAIn  Amount of TokenA to sell.
     * @return amountBOut  Amount of TokenB received.
     */
    function swapAforB(uint256 amountAIn)
        external
        nonReentrant
        returns (uint256 amountBOut)
    {
        require(amountAIn > 0, "DEX: amountIn must be > 0");
        require(reserveA > 0 && reserveB > 0, "DEX: no liquidity");

        uint256 amountAWithFee = amountAIn * FEE_NUMERATOR;
        amountBOut = (reserveB * amountAWithFee) /
                     (reserveA * FEE_DENOMINATOR + amountAWithFee);

        require(amountBOut > 0,         "DEX: insufficient output amount");
        require(amountBOut < reserveB,  "DEX: insufficient liquidity");

        // Track fee retained in pool (informational)
        totalFeesA += amountAIn - (amountAIn * FEE_NUMERATOR) / FEE_DENOMINATOR;

        // Checks-Effects-Interactions
        reserveA += amountAIn;
        reserveB -= amountBOut;

        require(tokenA.transferFrom(msg.sender, address(this), amountAIn),
                "DEX: TokenA transfer failed");
        require(tokenB.transfer(msg.sender, amountBOut),
                "DEX: TokenB transfer failed");

        emit Swap(msg.sender, address(tokenA), amountAIn, amountBOut);
    }

    /**
     * @notice Swap TokenB for TokenA.
     * @param amountBIn  Amount of TokenB to sell.
     * @return amountAOut  Amount of TokenA received.
     */
    function swapBforA(uint256 amountBIn)
        external
        nonReentrant
        returns (uint256 amountAOut)
    {
        require(amountBIn > 0, "DEX: amountIn must be > 0");
        require(reserveA > 0 && reserveB > 0, "DEX: no liquidity");

        uint256 amountBWithFee = amountBIn * FEE_NUMERATOR;
        amountAOut = (reserveA * amountBWithFee) /
                     (reserveB * FEE_DENOMINATOR + amountBWithFee);

        require(amountAOut > 0,         "DEX: insufficient output amount");
        require(amountAOut < reserveA,  "DEX: insufficient liquidity");

        totalFeesB += amountBIn - (amountBIn * FEE_NUMERATOR) / FEE_DENOMINATOR;

        reserveB += amountBIn;
        reserveA -= amountAOut;

        require(tokenB.transferFrom(msg.sender, address(this), amountBIn),
                "DEX: TokenB transfer failed");
        require(tokenA.transfer(msg.sender, amountAOut),
                "DEX: TokenA transfer failed");

        emit Swap(msg.sender, address(tokenB), amountBIn, amountAOut);
    }

    // ──────────────────────────────────────────────────────────────────
    // View / getter functions
    // ──────────────────────────────────────────────────────────────────

    /// @notice Returns (reserveA, reserveB).
    function getReserves() external view returns (uint256, uint256) {
        return (reserveA, reserveB);
    }

    /**
     * @notice Spot price: how many TokenB per TokenA.
     *         Scaled by 1e18 to preserve precision (divide by 1e18 to get decimal).
     */
    function spotPrice() external view returns (uint256) {
        require(reserveA > 0, "DEX: no liquidity");
        return (reserveB * 1e18) / reserveA;
    }

    /// @notice Price of 1 TokenA expressed in TokenB (×1e18).
    function getPriceAinB() external view returns (uint256) {
        require(reserveA > 0, "DEX: no liquidity");
        return (reserveB * 1e18) / reserveA;
    }

    /// @notice Price of 1 TokenB expressed in TokenA (×1e18).
    function getPriceBinA() external view returns (uint256) {
        require(reserveB > 0, "DEX: no liquidity");
        return (reserveA * 1e18) / reserveB;
    }

    /**
     * @notice Reserve ratio TokenA / TokenB (×1e18).
     *         This is also the "Spot Price" as per the assignment definition.
     */
    function getReserveRatio() external view returns (uint256) {
        require(reserveB > 0, "DEX: no liquidity");
        return (reserveA * 1e18) / reserveB;
    }

    /**
     * @notice Simulate output for a given TokenA input (no state change).
     *         Useful for front-ends and arbitrage contracts.
     */
    function getAmountOut(uint256 amountAIn) external view returns (uint256 amountBOut) {
        require(amountAIn > 0 && reserveA > 0 && reserveB > 0, "DEX: invalid input");
        uint256 aWithFee = amountAIn * FEE_NUMERATOR;
        amountBOut = (reserveB * aWithFee) / (reserveA * FEE_DENOMINATOR + aWithFee);
    }
}
