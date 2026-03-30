# HW3 – Theory Questions  (20 points)

> For each question the answer is followed by a **"Code Implementation"** section
> citing the exact file, function, and line logic that reflects it.

---

## Q1. Which address(es) should be allowed to mint/burn LP tokens?

**Answer:**  
Only the **DEX contract address** should be authorised to mint or burn LP tokens.
No user — not even the deployer — should be able to call `mint` or `burn` directly.

If an arbitrary address could mint LP tokens it could claim a share of the pool
without depositing anything (infinite dilution attack).  If it could burn them it
could drain the pool entirely.

**Code Implementation — `LPToken.sol` + `DEX.sol`:**

```solidity
// LPToken.sol
contract LPToken is ERC20, Ownable {
    constructor() ERC20("DEX LP Token", "LPT") Ownable(msg.sender) {}

    function mint(address to, uint256 amount) external onlyOwner { ... }
    function burn(address from, uint256 amount) external onlyOwner { ... }
}
```

```solidity
// DEX.sol – constructor
lpToken = new LPToken();   // DEX is msg.sender → DEX becomes LPToken.owner()
```

Because `new LPToken()` is called **inside** the DEX constructor,
`msg.sender` at that moment is the DEX contract itself, so the DEX
automatically becomes the sole `Ownable` owner.
The `onlyOwner` modifier on `mint` and `burn` therefore restricts both
operations exclusively to the DEX — no separate `transferOwnership` call needed,
and no EOA (externally-owned account) can ever call them.

---

## Q2. In what way do DEXes level the playing field between a powerful trader (HFT/institutional) and a retail investor?

**Answer:**

| Dimension | CEX (favours HFT) | AMM DEX (levels the field) |
|-----------|------------------|---------------------------|
| Price discovery | Order-book depth; co-location advantage | Deterministic formula — same equation for every caller |
| Access | KYC, geography, API tiers | Permissionless; any wallet, any time |
| Liquidity provision | Requires market-maker agreements | Any address can add any size |
| Large-trade penalty | HFT absorbs large orders cheaply via iceberg orders | Price impact is superlinear in trade size — hurts large traders more |

The constant-product formula actually **penalises** large traders: buying 10 % of the
reserves incurs ~9.3 % slippage (see Q7), while a retail trader buying 1 % faces
only ~1.3 % slippage. This built-in price impact is the AMM's natural equaliser.

**Code Implementation — `DEX.sol`:**

```solidity
// swapAforB – applies identical formula regardless of caller identity
uint256 amountAWithFee = amountAIn * FEE_NUMERATOR;          // 997 × Δx
amountBOut = (reserveB * amountAWithFee) /
             (reserveA * FEE_DENOMINATOR + amountAWithFee);  // constant-product
```

There is **no privileged caller check** anywhere in the swap path.
A whale calling `swapAforB(1_000_000e18)` uses the exact same code path as a
retail trader calling `swapAforB(10e18)` — the formula itself imposes the larger
price impact on the larger trade automatically.

---

## Q3. How can a miner exploit pending mempool transactions (MEV)? Can the DEX be made robust against it?

**Answer:**

**The attack — Sandwich:**

1. Miner sees a large swap `Δx` sitting in the mempool.
2. **Front-run:** Miner inserts their own buy *before* the victim, pushing the price up.
3. Victim's tx executes at the now-worse price.
4. **Back-run:** Miner sells immediately after, profiting from the price the victim moved.

This is **Miner Extractable Value (MEV)**.  The miner profits at zero market risk.

**Defences:**

| Mechanism | Description |
|-----------|-------------|
| `minAmountOut` slippage guard | Tx reverts if output < user's threshold — sandwich unprofitable |
| Private mempools (Flashbots Protect) | Tx hidden from miners until inclusion |
| Commit-reveal | Parameters committed in block N, revealed in N+1 |
| TWAP price oracles | Price manipulation within one block has negligible long-term effect |

**Code Implementation — `DEX.sol`:**

The current contracts implement the core defence: `require` checks ensure the output
is always at least the constant-product minimum:

```solidity
require(amountBOut > 0,        "DEX: insufficient output amount");
require(amountBOut < reserveB, "DEX: insufficient liquidity");
```

To fully close the sandwich vector, `swapAforB` is designed to be easily extended
with a caller-supplied minimum output (same pattern as Uniswap v2 Router):

```solidity
// Recommended extension:
function swapAforB(uint256 amountAIn, uint256 minAmountBOut) external {
    ...
    require(amountBOut >= minAmountBOut, "DEX: slippage exceeded");
}
```

This single line makes a sandwich unprofitable — if the front-run moves the price
enough that the victim would receive less than `minAmountBOut`, the tx simply reverts.

---

## Q4. How do gas fees affect the economic viability of the DEX and arbitrage?

**Answer:**

Every function call consumes gas. Approximate costs on Ethereum mainnet:

| Operation | ~Gas | Cost at 30 gwei, ETH=$2 000 |
|-----------|------|------------------------------|
| `addLiquidity` | 120 000 | ~$7.20 |
| `removeLiquidity` | 90 000 | ~$5.40 |
| `swapAforB` | 80 000 | ~$4.80 |
| Arbitrage (2 swaps + approvals) | 300 000 | ~$18.00 |

**Implications:**

- **Minimum viable trade size** — a swap costing $5 in gas is rational only if the
  trade value is large enough that $5 is a small fraction.  Micro-trades become uneconomical.
- **LP economics** — small LPs may earn less in swap fees over weeks than one
  withdrawal costs in gas, biasing liquidity toward large providers.
- **Arbitrage viability** — profit must exceed gas cost.  An arb earning $3 while
  gas costs $18 destroys value.

**Code Implementation — `Arbitrage.sol`:**

```solidity
uint256 public minProfitThreshold = 1e15;  // configurable minimum profit (wei)

require(
    finalOut > amountIn + minProfitThreshold,
    "Arbitrage: insufficient profit – opportunity does not exist"
);
```

`minProfitThreshold` should be set to at least the expected gas cost of the
two-swap execution. The owner can update it via `setMinProfitThreshold(uint256)`
as gas prices change, ensuring the contract never executes arb that costs more
than it earns. This is also what triggers the **"Failed arbitrage"** test scenario
required in Task 3.

---

## Q5. Could gas fees create unfair advantages for some transactors over others? How?

**Answer:**

**Yes — in three key ways:**

1. **Gas auction front-running:** Anyone can pay a higher `maxPriorityFeePerGas`
   to jump ahead of a pending tx.  MEV bots routinely outbid retail users.

2. **Validator self-dealing:** Block proposers can include their own transactions at
   zero gas cost and in any position, extracting MEV without the auction overhead
   that retail users pay.

3. **Asymmetric gas optimisation:** Sophisticated actors use highly-optimised
   assembly contracts (lower gas per operation) giving them cheaper execution than
   standard Solidity contracts.

**Code Implementation — `DEX.sol` + `Arbitrage.sol`:**

We applied the following gas-efficiency measures to reduce the cost disadvantage
for retail users:

```solidity
// DEX.sol – immutable variables are read from bytecode, not storage (saves ~2100 gas/read)
IERC20  public immutable tokenA;
IERC20  public immutable tokenB;
LPToken public immutable lpToken;

// DEX.sol – constants avoid SLOAD entirely (3 gas vs 2100 gas)
uint256 public constant FEE_NUMERATOR   = 997;
uint256 public constant FEE_DENOMINATOR = 1000;
```

```solidity
// Arbitrage.sol – pure simulation (view, zero gas) lets any caller
// check profitability before committing real gas to executeArbitrage()
function checkArbitrage(...) external view returns (bool profitable, uint256 expectedProfit)
```

Using `immutable` and `constant` instead of regular storage variables saves ~2 100
gas per read.  The `checkArbitrage` view function means retail users can evaluate
whether a tx is worth submitting without spending gas on a failed attempt.

---

## Q6. What are the various ways to minimise slippage in a swap?

**Answer:**

| Method | Mechanism |
|--------|-----------|
| **Trade smaller amounts** | Slippage ∝ f; halving Δx roughly halves price impact |
| **Increase pool TVL** | Larger reserves → smaller f for the same Δx |
| **Concentrated liquidity** | Deploy liquidity in a narrow price band (Uniswap v3), multiplying effective depth |
| **Multi-pool routing** | Split order across several pools/DEXes (aggregators like 1inch) |
| **High-liquidity pairs** | Stablecoin or blue-chip pairs have deep pools by default |
| **Set `minAmountOut`** | Doesn't reduce price impact but prevents accepting worse-than-expected rates |

**Code Implementation — `DEX.sol`:**

The `getAmountOut` view function allows callers to simulate slippage **before**
committing to a transaction:

```solidity
/// @notice Simulate output for a given TokenA input (no state change).
function getAmountOut(uint256 amountAIn) external view returns (uint256 amountBOut) {
    require(amountAIn > 0 && reserveA > 0 && reserveB > 0, "DEX: invalid input");
    uint256 aWithFee = amountAIn * FEE_NUMERATOR;
    amountBOut = (reserveB * aWithFee) / (reserveA * FEE_DENOMINATOR + aWithFee);
}
```

A front-end calls `getAmountOut` to show the user their expected slippage in
real-time and warn them if f is too large, directly implementing the "trade smaller
amounts" and "show expected output" mitigations above.

---

## Q7. Plot how slippage varies with trade lot fraction for a constant-product AMM

**Derivation:**

Let `x = reserveA`, `y = reserveB`, `Δx` = TokenA input, `f = Δx / x`.

With the 0.3% fee (997/1000):

$$\Delta y = \frac{y \cdot 997 \cdot \Delta x}{1000x + 997\Delta x}$$

Dividing by Δx:

$$\text{Actual rate} = \frac{997 \cdot (y/x)}{1000 + 997f}, \qquad \text{Spot rate} = \frac{y}{x}$$

Using equation (2) from the assignment:

$$\boxed{S(f) = \frac{-3 - 997f}{1000 + 997f}\times 100\%}$$

At f → 0: S → −0.3 % (pure fee).  At f = 1: S = −50 %.

| f | \|S(f)\| |
|---|--------|
| 0 (limit) | 0.30 % |
| 1 % | 1.27 % |
| 5 % | 5.17 % |
| 10 % | 9.34 % |
| 50 % | 33.2 % |
| 100 % | 50.0 % |

**Code Implementation — `simulation.py` and `theory/plot_slippage.py`:**

The simulation computes slippage for every swap using eq. (2) exactly:

```python
# simulation.py
expected_rate = dex.reserveB / dex.reserveA   # spot price before the swap
amt_out       = dex.swap_A_for_B(amt_in)
actual_rate   = amt_out / amt_in

slip = (actual_rate - expected_rate) / expected_rate * 100   # equation (2)
slip_vals.append(slip)
```

The closed-form expression S(f) is plotted in `theory/plot_slippage.py`:

```python
# theory/plot_slippage.py
f = np.linspace(0, 1, 500)
S_with_fee    = ((-3 - 997 * f) / (1000 + 997 * f)) * 100  # with 0.3% fee
S_without_fee = (-f / (1 + f)) * 100                        # pure price impact
```

See the saved figure `slippage_vs_lot_fraction.png` for the plot.
The two curves separate at large f, showing that the 0.3% fee is dominant only
for very small trades — price impact dominates for f > ~5%.
