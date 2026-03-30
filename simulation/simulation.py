"""
HW3 – DEX Simulation  (Task 2, Testing Requirements)
=====================================================
Off-chain Python simulation that mirrors the Solidity constant-product AMM.

Users:  5 Liquidity Providers  (LP1–LP5)  +  8 Traders  (T1–T8)
N    :  75 random transactions

Metrics plotted:
  1. Total Value Locked (TVL)
  2. Reserve Ratio  (TokenA / TokenB)
  3. Spot Price  (TokenB per TokenA)
  4. LP Token Distribution
  5. Cumulative Swap Volume
  6. Cumulative Fee Accumulation
  7. Slippage per swap
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random
from collections import defaultdict

# ──────────────────────────────────────────────────────────────────────────────
# Reproducibility
# ──────────────────────────────────────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ──────────────────────────────────────────────────────────────────────────────
# Constant-product AMM  (mirrors DEX.sol logic exactly)
# ──────────────────────────────────────────────────────────────────────────────
FEE_NUM = 997          # 0.3% fee
FEE_DEN = 1000


class DEX:
    def __init__(self):
        self.reserveA  = 0.0
        self.reserveB  = 0.0
        self.lp_supply = 0.0
        self.lp        = defaultdict(float)   # user → LP balance
        self.fees_A    = 0.0
        self.fees_B    = 0.0

    # ── Liquidity ────────────────────────────────────────────────────────────

    def add_liquidity(self, user, amtA, amtB=None):
        """
        Returns (amtA_used, amtB_used, lp_minted).
        For existing pools amtB is recomputed to preserve ratio.
        """
        if amtA <= 0:
            return 0, 0, 0

        if self.lp_supply == 0:
            # First deposit – caller sets the ratio
            if amtB is None or amtB <= 0:
                return 0, 0, 0
            lp_minted = amtA                         # LP = amtA (arbitrary initial scale)
        else:
            # Enforce existing ratio
            amtB = amtA * self.reserveB / self.reserveA
            lp_minted = amtA * self.lp_supply / self.reserveA

        if lp_minted <= 0:
            return 0, 0, 0

        self.reserveA  += amtA
        self.reserveB  += amtB
        self.lp_supply += lp_minted
        self.lp[user]  += lp_minted
        return amtA, amtB, lp_minted

    def remove_liquidity(self, user, lp_amt):
        """Burn lp_amt LP tokens, return (amtA, amtB)."""
        lp_amt = min(lp_amt, self.lp[user])
        if lp_amt <= 0 or self.lp_supply <= 0:
            return 0, 0
        share = lp_amt / self.lp_supply
        amtA  = share * self.reserveA
        amtB  = share * self.reserveB
        self.reserveA  -= amtA
        self.reserveB  -= amtB
        self.lp_supply -= lp_amt
        self.lp[user]  -= lp_amt
        return amtA, amtB

    # ── Swaps ────────────────────────────────────────────────────────────────

    def swap_A_for_B(self, amtA):
        """Returns TokenB received. Applies 0.3% fee."""
        if amtA <= 0 or self.reserveA <= 0 or self.reserveB <= 0:
            return 0
        aFee   = amtA * FEE_NUM
        amtB   = self.reserveB * aFee / (self.reserveA * FEE_DEN + aFee)
        fee    = amtA * (FEE_DEN - FEE_NUM) / FEE_DEN
        self.fees_A   += fee
        self.reserveA += amtA
        self.reserveB -= amtB
        return amtB

    def swap_B_for_A(self, amtB):
        """Returns TokenA received. Applies 0.3% fee."""
        if amtB <= 0 or self.reserveA <= 0 or self.reserveB <= 0:
            return 0
        bFee   = amtB * FEE_NUM
        amtA   = self.reserveA * bFee / (self.reserveB * FEE_DEN + bFee)
        fee    = amtB * (FEE_DEN - FEE_NUM) / FEE_DEN
        self.fees_B   += fee
        self.reserveB += amtB
        self.reserveA -= amtA
        return amtA

    # ── Metrics ──────────────────────────────────────────────────────────────

    def spot_price(self):
        """TokenB per TokenA (= reserveB / reserveA)."""
        return self.reserveB / self.reserveA if self.reserveA > 0 else 0

    def tvl(self):
        """Total value locked in TokenA units using the spot price."""
        sp = self.spot_price()
        if sp == 0:
            return 0
        # TVL_A = reserveA + reserveB / sp  = 2 * reserveA  (always, for CPAMM)
        return self.reserveA + self.reserveB / sp


# ──────────────────────────────────────────────────────────────────────────────
# Users & initial balances
# ──────────────────────────────────────────────────────────────────────────────
LP_NAMES     = [f"LP{i}" for i in range(1, 6)]
TRADER_NAMES = [f"T{i}"  for i in range(1, 9)]
ALL_USERS    = LP_NAMES + TRADER_NAMES

balA = {u: 10_000.0 for u in LP_NAMES}
balA.update({u: 5_000.0 for u in TRADER_NAMES})
balB = {u: 10_000.0 for u in LP_NAMES}
balB.update({u: 5_000.0 for u in TRADER_NAMES})

dex = DEX()

# ── Bootstrap: LP1 seeds the pool ────────────────────────────────────────────
INIT_A, INIT_B = 2_000.0, 3_000.0
_, _, lp0 = dex.add_liquidity("LP1", INIT_A, INIT_B)
balA["LP1"] -= INIT_A
balB["LP1"] -= INIT_B

# ──────────────────────────────────────────────────────────────────────────────
# Metric history
# ──────────────────────────────────────────────────────────────────────────────
N = 75

tvl_hist       = []
ratio_hist     = []
spot_hist      = []
vol_A_hist     = []
vol_B_hist     = []
fee_A_hist     = []
fee_B_hist     = []
slip_indices   = []
slip_vals      = []
lp_hist        = {lp: [] for lp in LP_NAMES}

cum_vol_A = 0.0
cum_vol_B = 0.0


def snapshot():
    tvl_hist.append(dex.tvl())
    ratio_hist.append(dex.reserveA / dex.reserveB if dex.reserveB > 0 else 0)
    spot_hist.append(dex.spot_price())
    vol_A_hist.append(cum_vol_A)
    vol_B_hist.append(cum_vol_B)
    fee_A_hist.append(dex.fees_A)
    fee_B_hist.append(dex.fees_B)
    for lp in LP_NAMES:
        lp_hist[lp].append(dex.lp[lp])


snapshot()   # t = 0 (initial state)

# ──────────────────────────────────────────────────────────────────────────────
# Run N transactions
# ──────────────────────────────────────────────────────────────────────────────
for tx in range(N):
    user = random.choice(ALL_USERS)

    # Operation weights: LPs can also add/remove liquidity
    if user in LP_NAMES:
        op = random.choices(["swap", "add", "remove"], weights=[0.40, 0.35, 0.25])[0]
    else:
        op = "swap"

    # ── SWAP ─────────────────────────────────────────────────────────────────
    if op == "swap":
        direction = random.choice(["AtoB", "BtoA"])

        if direction == "AtoB" and balA[user] > 1e-6 and dex.reserveA > 0:
            max_amt = min(balA[user], 0.10 * dex.reserveA)
            if max_amt > 1e-9:
                amt_in        = random.uniform(1e-6, max_amt)
                expected_rate = dex.reserveB / dex.reserveA   # spot before swap
                amt_out       = dex.swap_A_for_B(amt_in)
                actual_rate   = amt_out / amt_in
                slip          = (actual_rate - expected_rate) / expected_rate * 100
                slip_indices.append(tx + 1)
                slip_vals.append(slip)
                balA[user] -= amt_in
                balB[user] += amt_out
                cum_vol_A  += amt_in

        elif direction == "BtoA" and balB[user] > 1e-6 and dex.reserveB > 0:
            max_amt = min(balB[user], 0.10 * dex.reserveB)
            if max_amt > 1e-9:
                amt_in        = random.uniform(1e-6, max_amt)
                expected_rate = dex.reserveA / dex.reserveB   # spot before swap (A per B)
                amt_out       = dex.swap_B_for_A(amt_in)
                actual_rate   = amt_out / amt_in
                slip          = (actual_rate - expected_rate) / expected_rate * 100
                slip_indices.append(tx + 1)
                slip_vals.append(slip)
                balB[user] -= amt_in
                balA[user] += amt_out
                cum_vol_B  += amt_in

    # ── ADD LIQUIDITY ─────────────────────────────────────────────────────────
    elif op == "add" and balA[user] > 0 and dex.reserveA > 0:
        max_A  = balA[user] * random.uniform(0.05, 0.40)
        if max_A > 1e-6:
            amt_A      = max_A
            amt_B_need = amt_A * dex.reserveB / dex.reserveA
            if balB[user] >= amt_B_need:
                a, b, _ = dex.add_liquidity(user, amt_A, amt_B_need)
                balA[user] -= a
                balB[user] -= b

    # ── REMOVE LIQUIDITY ──────────────────────────────────────────────────────
    elif op == "remove" and dex.lp[user] > 0:
        lp_amt = dex.lp[user] * random.uniform(0.05, 0.40)
        if lp_amt > 1e-9:
            a, b = dex.remove_liquidity(user, lp_amt)
            balA[user] += a
            balB[user] += b

    snapshot()   # record after every transaction

# ──────────────────────────────────────────────────────────────────────────────
# Print final state
# ──────────────────────────────────────────────────────────────────────────────
print("=" * 55)
print("  DEX SIMULATION  –  Final State  (N = 75)")
print("=" * 55)
print(f"  Reserve A      : {dex.reserveA:,.2f}")
print(f"  Reserve B      : {dex.reserveB:,.2f}")
print(f"  Spot Price     : {dex.spot_price():.4f} B/A")
print(f"  TVL (in A)     : {dex.tvl():,.2f}")
print(f"  Total LP supply: {dex.lp_supply:,.2f}")
print(f"  Fees collected : {dex.fees_A:.4f} A  |  {dex.fees_B:.4f} B")
print(f"  Total swaps    : {len(slip_vals)}")
print("-" * 55)
print("  LP Holdings:")
for lp in LP_NAMES:
    print(f"    {lp}: {dex.lp[lp]:,.4f} LPT")
print("=" * 55)

# ──────────────────────────────────────────────────────────────────────────────
# Plot all 7 metrics
# ──────────────────────────────────────────────────────────────────────────────
T = list(range(len(tvl_hist)))   # 0 .. N

fig = plt.figure(figsize=(18, 24))
gs  = gridspec.GridSpec(4, 2, figure=fig, hspace=0.50, wspace=0.35)
fig.patch.set_facecolor("#f8f9fa")

TITLE_FONT = dict(fontsize=12, fontweight="bold", pad=8)
LABEL_FONT = dict(fontsize=9)
GRID_KW    = dict(alpha=0.3, linestyle="--")


# 1. TVL ──────────────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.fill_between(T, tvl_hist, alpha=0.15, color="royalblue")
ax1.plot(T, tvl_hist, color="royalblue", linewidth=1.8)
ax1.set_title("① Total Value Locked (in TokenA)", **TITLE_FONT)
ax1.set_xlabel("Transaction #", **LABEL_FONT)
ax1.set_ylabel("TVL (TokenA units)", **LABEL_FONT)
ax1.grid(True, **GRID_KW)

# 2. Reserve Ratio ────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(T, ratio_hist, color="darkorange", linewidth=1.8)
ax2.set_title("② Reserve Ratio  (TokenA / TokenB)", **TITLE_FONT)
ax2.set_xlabel("Transaction #", **LABEL_FONT)
ax2.set_ylabel("A / B ratio", **LABEL_FONT)
ax2.grid(True, **GRID_KW)

# 3. Spot Price ───────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(T, spot_hist, color="seagreen", linewidth=1.8)
ax3.set_title("③ Spot Price  (TokenB per TokenA)", **TITLE_FONT)
ax3.set_xlabel("Transaction #", **LABEL_FONT)
ax3.set_ylabel("B / A price", **LABEL_FONT)
ax3.grid(True, **GRID_KW)

# 4. LP Token Distribution ────────────────────────────────────────────────────
LP_COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]
ax4 = fig.add_subplot(gs[1, 1])
for lp, col in zip(LP_NAMES, LP_COLORS):
    ax4.plot(T, lp_hist[lp], label=lp, color=col, linewidth=1.6)
ax4.set_title("④ LP Token Holdings", **TITLE_FONT)
ax4.set_xlabel("Transaction #", **LABEL_FONT)
ax4.set_ylabel("LP Tokens held", **LABEL_FONT)
ax4.legend(fontsize=8, loc="upper left")
ax4.grid(True, **GRID_KW)

# 5. Cumulative Swap Volume ───────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, 0])
ax5.plot(T, vol_A_hist, color="steelblue",  linewidth=1.8, label="TokenA swapped")
ax5.plot(T, vol_B_hist, color="tomato",     linewidth=1.8, label="TokenB swapped")
ax5.set_title("⑤ Cumulative Swap Volume", **TITLE_FONT)
ax5.set_xlabel("Transaction #", **LABEL_FONT)
ax5.set_ylabel("Cumulative tokens", **LABEL_FONT)
ax5.legend(fontsize=8)
ax5.grid(True, **GRID_KW)

# 6. Fee Accumulation ─────────────────────────────────────────────────────────
ax6 = fig.add_subplot(gs[2, 1])
ax6.plot(T, fee_A_hist, color="steelblue",  linewidth=1.8, label="Fees in TokenA")
ax6.plot(T, fee_B_hist, color="tomato",     linewidth=1.8, label="Fees in TokenB")
ax6.set_title("⑥ Cumulative Fee Accumulation (0.3%)", **TITLE_FONT)
ax6.set_xlabel("Transaction #", **LABEL_FONT)
ax6.set_ylabel("Fees collected", **LABEL_FONT)
ax6.legend(fontsize=8)
ax6.grid(True, **GRID_KW)

# 7. Slippage per swap ────────────────────────────────────────────────────────
ax7 = fig.add_subplot(gs[3, :])
ax7.scatter(slip_indices, slip_vals, color="mediumpurple", s=35,
            alpha=0.75, zorder=3, label="Slippage per swap")
ax7.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
ax7.axhline(-0.3, color="red", linewidth=0.8, linestyle=":",
            alpha=0.6, label="−0.3% (fee only, f→0)")
ax7.set_title(
    "⑦ Slippage per Swap\n"
    r"$S = \frac{\text{actual rate} - \text{spot rate}}{\text{spot rate}} \times 100\%$  "
    "(always negative: price impact + fee)",
    **TITLE_FONT
)
ax7.set_xlabel("Transaction #", **LABEL_FONT)
ax7.set_ylabel("Slippage (%)", **LABEL_FONT)
ax7.legend(fontsize=8)
ax7.grid(True, **GRID_KW)

plt.suptitle(
    "DEX Constant-Product AMM Simulation  –  N = 75 transactions\n"
    "(5 LPs · 8 Traders · 0.3% fee · seed = 42)",
    fontsize=15, fontweight="bold", y=1.005
)

out_path = "dex_simulation_metrics.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nPlot saved → {out_path}")
plt.show()
