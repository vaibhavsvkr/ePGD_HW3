"""
Theory Q7 – Slippage vs Trade Lot Fraction
==========================================
Derives and plots the closed-form slippage formula for a constant-product AMM
with 0.3% fee.

Let:
  f = Δx / x   (trade lot fraction, i.e. fraction of reserve spent as input)

With fee (997/1000):
  Actual rate  = Δy / Δx = 997·(y/x) / (1000 + 997·f)
  Spot rate    = y / x

  S(f) = (actual - spot) / spot × 100 %
       = [997 / (1000 + 997·f)  - 1] × 100 %
       = (- 3 - 997·f) / (1000 + 997·f) × 100 %

|S(f)| increases from 0.3 % (at f=0) to ~50 % (at f=1).
"""

import numpy as np
import matplotlib.pyplot as plt

f = np.linspace(0, 1, 500)

# With fee (0.3%):
S_with_fee    = ((-3 - 997 * f) / (1000 + 997 * f)) * 100

# Without fee (ideal constant-product, for comparison):
#   actual = Δy/Δx = y/(x + Δx) = (y/x) / (1 + f)
#   S_nofee = (1/(1+f) - 1) × 100 = -f/(1+f) × 100
S_without_fee = (-f / (1 + f)) * 100

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("#f8f9fa")

ax.plot(f * 100, -S_with_fee,    color="royalblue", linewidth=2.0,
        label=r"$|S(f)|$ with 0.3 % fee")
ax.plot(f * 100, -S_without_fee, color="tomato",    linewidth=2.0,
        linestyle="--", label=r"$|S(f)|$ no fee (pure price impact)")

# Annotations
ax.axhline(0.3, color="gray", linewidth=0.8, linestyle=":", alpha=0.7,
           label="0.3 % baseline (fee only, f→0)")
ax.axvline(10,  color="green", linewidth=0.8, linestyle=":", alpha=0.7)
ax.annotate(f"f=10 %\n|S|≈{(-S_with_fee[50]):.1f} %",
            xy=(10, -S_with_fee[50]), xytext=(14, -S_with_fee[50] + 2),
            fontsize=9, arrowprops=dict(arrowstyle="->", color="green"),
            color="green")

ax.set_title(
    "Theory Q7 — Slippage |S| vs Trade Lot Fraction  f = Δx / x\n"
    r"Constant-Product AMM,  $|S(f)| = \frac{3 + 997f}{1000 + 997f} \times 100\,\%$",
    fontsize=11, fontweight="bold"
)
ax.set_xlabel("Trade Lot Fraction  f  (%)", fontsize=10)
ax.set_ylabel("Slippage  |S|  (%)", fontsize=10)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_xlim(0, 100)
ax.set_ylim(0, 55)

plt.tight_layout()
plt.savefig("slippage_vs_lot_fraction.png", dpi=150, bbox_inches="tight")
print("Slippage plot saved → slippage_vs_lot_fraction.png")
plt.show()
