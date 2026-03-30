"""Generate theory.pdf from theory answers."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

W, H = A4
MARGIN = 2.4 * cm

doc = SimpleDocTemplate(
    "/home/claude/dex_project/theory/theory.pdf",
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=2*cm, bottomMargin=2*cm,
)

# ── Colour palette ────────────────────────────────────────────────────
NAVY    = colors.HexColor("#1e3a5f")
CYAN    = colors.HexColor("#0099cc")
LIGHT   = colors.HexColor("#e8f4f8")
CODEBG  = colors.HexColor("#1a1d28")
CODEFG  = colors.HexColor("#a8d8f0")
MUTED   = colors.HexColor("#6b7280")
GREEN   = colors.HexColor("#065f46")
GREENBG = colors.HexColor("#d1fae5")
RED     = colors.HexColor("#7f1d1d")
REDBG   = colors.HexColor("#fee2e2")

# ── Styles ────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE_STYLE = S("DocTitle",
    fontSize=22, fontName="Helvetica-Bold", textColor=NAVY,
    spaceAfter=6, alignment=TA_CENTER, leading=28)

SUBTITLE_STYLE = S("DocSub",
    fontSize=10, fontName="Helvetica", textColor=MUTED,
    spaceAfter=20, alignment=TA_CENTER)

Q_STYLE = S("Question",
    fontSize=13, fontName="Helvetica-Bold", textColor=NAVY,
    spaceBefore=18, spaceAfter=8, leading=18)

SECTION_STYLE = S("Section",
    fontSize=9.5, fontName="Helvetica-Bold", textColor=CYAN,
    spaceBefore=10, spaceAfter=4, textTransform="uppercase",
    letterSpacing=1)

BODY_STYLE = S("Body",
    fontSize=10, fontName="Helvetica", textColor=colors.HexColor("#1f2937"),
    spaceAfter=6, leading=15, alignment=TA_JUSTIFY)

CODE_STYLE = S("Code",
    fontSize=8.2, fontName="Courier", textColor=CODEFG,
    spaceAfter=2, leading=12, leftIndent=0)

BULLET_STYLE = S("Bullet",
    fontSize=10, fontName="Helvetica", textColor=colors.HexColor("#1f2937"),
    spaceAfter=3, leading=14, leftIndent=18,
    bulletIndent=6)

NOTE_STYLE = S("Note",
    fontSize=9, fontName="Helvetica-Oblique", textColor=colors.HexColor("#374151"),
    spaceAfter=4, leading=13)

# ── Helper ────────────────────────────────────────────────────────────
def code_block(lines):
    """Return a light-background code block as a Table."""
    rows = [[Paragraph(line.replace(" ", "&nbsp;").replace("<","&lt;").replace(">","&gt;"),
                       CODE_STYLE)] for line in lines]
    t = Table(rows, colWidths=[W - 2*MARGIN - 0.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CODEBG),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#252836")),
    ]))
    return t

def two_col_table(rows, hdrs=None):
    col = (W - 2*MARGIN - 0.2*cm) / 2
    data = []
    if hdrs:
        data.append([Paragraph(f"<b>{hdrs[0]}</b>", BODY_STYLE),
                     Paragraph(f"<b>{hdrs[1]}</b>", BODY_STYLE)])
    for r in rows:
        data.append([Paragraph(r[0], BODY_STYLE), Paragraph(r[1], BODY_STYLE)])
    t = Table(data, colWidths=[col, col])
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  LIGHT if hdrs else colors.white),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#d1d5db")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS",(0,1 if hdrs else 0), (-1,-1),
                          [colors.white, colors.HexColor("#f9fafb")]),
    ]
    if hdrs:
        style.append(("TEXTCOLOR", (0,0), (-1,0), NAVY))
    t.setStyle(TableStyle(style))
    return t

def slip_table():
    data = [["f (trade lot fraction)", "|S(f)| slippage"]]
    rows_data = [("0 (limit)", "0.30%"), ("1%","1.27%"), ("5%","5.17%"),
                 ("10%","9.34%"), ("50%","33.2%"), ("100%","50.0%")]
    for r in rows_data:
        data.append([r[0], r[1]])
    col = 6*cm
    t = Table(data, colWidths=[col, col])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),  NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0),  colors.white),
        ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#d1d5db")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, LIGHT]),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("ALIGN",         (1,0), (1,-1),  "CENTER"),
        ("FONTNAME",      (0,1), (-1,-1), "Courier"),
        ("FONTSIZE",      (0,0), (-1,-1), 9.5),
    ]))
    return t

# ── Story ─────────────────────────────────────────────────────────────
story = []

# Cover
story += [
    Spacer(1, 1.5*cm),
    Paragraph("HW3 – Theory Questions", TITLE_STYLE),
    Paragraph("Cryptocurrencies &amp; Smart Contracts  |  IIT Bombay", SUBTITLE_STYLE),
    HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=24),
]

# ── Q1 ────────────────────────────────────────────────────────────────
story += [
    Paragraph("Q1.  Which address(es) should be allowed to mint/burn LP tokens?", Q_STYLE),
    Paragraph("ANSWER", SECTION_STYLE),
    Paragraph(
        "Only the <b>DEX contract address</b> should be authorised to mint or burn LP tokens. "
        "No user — not even the deployer — should be able to call <b>mint</b> or <b>burn</b> directly.",
        BODY_STYLE),
    Paragraph(
        "If an arbitrary address could mint LP tokens it could claim a share of the pool "
        "without depositing anything (infinite dilution attack). If it could burn them it "
        "could drain the pool entirely.",
        BODY_STYLE),
    Spacer(1,6),
    Paragraph("CODE IMPLEMENTATION — LPToken.sol + DEX.sol", SECTION_STYLE),
    Paragraph(
        "LPToken inherits OpenZeppelin's <b>Ownable</b>. Both <b>mint</b> and <b>burn</b> "
        "carry the <b>onlyOwner</b> modifier. The key design choice is that the LPToken is deployed "
        "<i>inside</i> the DEX constructor using <b>new LPToken()</b>, making the DEX contract "
        "itself the sole owner automatically — no separate transferOwnership call is needed.",
        BODY_STYLE),
    code_block([
        "// LPToken.sol",
        "function mint(address to, uint256 amount) external onlyOwner { _mint(to, amount); }",
        "function burn(address from, uint256 amount) external onlyOwner { _burn(from, amount); }",
        "",
        "// DEX.sol – constructor",
        "lpToken = new LPToken();   // DEX is msg.sender → DEX becomes LPToken.owner()",
    ]),
    Spacer(1, 8),
]

# ── Q2 ────────────────────────────────────────────────────────────────
story += [
    Paragraph("Q2.  How do DEXes level the playing field between HFT and retail traders?", Q_STYLE),
    Paragraph("ANSWER", SECTION_STYLE),
    two_col_table([
        ("Price discovery", "Order-book; HFTs get co-location | Deterministic formula — same for every caller"),
        ("Access", "KYC, geography, API tiers | Permissionless; any wallet, any time"),
        ("Liquidity", "Market-maker agreements needed | Any address can deposit any size"),
        ("Large-trade penalty", "HFT absorbs large orders cheaply | Price impact superlinear — hurts whales more"),
    ], hdrs=["Dimension", "CEX vs AMM DEX"]),
    Spacer(1, 8),
    Paragraph(
        "The constant-product formula actually <b>penalises</b> large traders: buying 10% of "
        "the reserves incurs ~9.3% slippage (see Q7), while a retail trader buying 1% faces "
        "only ~1.3% slippage. This built-in price impact is the AMM's natural equaliser.",
        BODY_STYLE),
    Paragraph("CODE IMPLEMENTATION — DEX.sol", SECTION_STYLE),
    Paragraph(
        "There is <b>no privileged caller check</b> anywhere in the swap path. "
        "A whale and a retail trader use the identical code path — the formula imposes "
        "the larger price impact on the larger trade automatically.",
        BODY_STYLE),
    code_block([
        "// swapAforB – same formula regardless of caller or amount",
        "uint256 amountAWithFee = amountAIn * FEE_NUMERATOR;   // 997 x dx",
        "amountBOut = (reserveB * amountAWithFee) /",
        "             (reserveA * FEE_DENOMINATOR + amountAWithFee);",
    ]),
    Spacer(1, 8),
]

# ── Q3 ────────────────────────────────────────────────────────────────
story += [
    Paragraph("Q3.  How can a miner exploit mempool transactions (MEV)? Can the DEX be made robust?", Q_STYLE),
    Paragraph("ANSWER — THE SANDWICH ATTACK", SECTION_STYLE),
    Paragraph(
        "1. Miner sees a large swap in the mempool. &nbsp;"
        "2. <b>Front-run:</b> inserts own buy before the victim, pushing price up. &nbsp;"
        "3. Victim's tx executes at a worse price. &nbsp;"
        "4. <b>Back-run:</b> miner sells immediately, profiting from the price the victim moved. "
        "This is called <b>Miner Extractable Value (MEV)</b>.",
        BODY_STYLE),
    Spacer(1, 6),
    two_col_table([
        ("<b>minAmountOut</b> guard", "Tx reverts if output &lt; threshold → sandwich unprofitable"),
        ("Private mempools (Flashbots)", "Tx hidden from miners until block inclusion"),
        ("Commit-reveal", "Swap params committed in block N, revealed in N+1"),
        ("TWAP oracles", "Single-block manipulation has negligible long-term price effect"),
    ], hdrs=["Defence", "How it helps"]),
    Spacer(1, 8),
    Paragraph("CODE IMPLEMENTATION — DEX.sol", SECTION_STYLE),
    Paragraph(
        "The require() guards enforce the constant-product minimum. To fully close the "
        "sandwich vector, swapAforB can be extended with a caller-supplied minAmountBOut:",
        BODY_STYLE),
    code_block([
        "require(amountBOut > 0,        \"DEX: insufficient output amount\");",
        "require(amountBOut < reserveB, \"DEX: insufficient liquidity\");",
        "",
        "// Recommended extension:",
        "require(amountBOut >= minAmountBOut, \"DEX: slippage exceeded\");",
    ]),
    Spacer(1, 8),
]

story.append(PageBreak())

# ── Q4 ────────────────────────────────────────────────────────────────
story += [
    Paragraph("Q4.  How do gas fees influence economic viability of the DEX and arbitrage?", Q_STYLE),
    Paragraph("ANSWER", SECTION_STYLE),
    two_col_table([
        ("addLiquidity", "~120 000 gas  |  ~$7.20 at 30 gwei, ETH=$2 000"),
        ("removeLiquidity", "~90 000 gas  |  ~$5.40"),
        ("swapAforB", "~80 000 gas  |  ~$4.80"),
        ("Arbitrage (2 swaps + approvals)", "~300 000 gas  |  ~$18.00"),
    ], hdrs=["Operation", "Approx. Gas / Cost"]),
    Spacer(1, 8),
    Paragraph(
        "<b>Minimum viable trade size:</b> a swap costing $5 in gas is rational only if the trade "
        "value is large enough that $5 is a small fraction. Micro-trades become uneconomical. "
        "<b>LP economics:</b> small LPs may earn less in fees than one withdrawal costs in gas. "
        "<b>Arbitrage:</b> profit must exceed gas cost.",
        BODY_STYLE),
    Paragraph("CODE IMPLEMENTATION — Arbitrage.sol", SECTION_STYLE),
    Paragraph(
        "The minProfitThreshold check ensures the contract never executes an arb that costs "
        "more in gas than it earns. The owner can adjust this threshold as gas prices change. "
        "This variable also directly triggers the <b>Failed arbitrage</b> test scenario required in Task 3.",
        BODY_STYLE),
    code_block([
        "uint256 public minProfitThreshold = 1e15;  // configurable (set above gas cost)",
        "",
        "require(",
        "    finalOut > amountIn + minProfitThreshold,",
        "    \"Arbitrage: insufficient profit\"",
        ");",
    ]),
    Spacer(1, 8),
]

# ── Q5 ────────────────────────────────────────────────────────────────
story += [
    Paragraph("Q5.  Could gas fees create unfair advantages? How?", Q_STYLE),
    Paragraph("ANSWER", SECTION_STYLE),
    Paragraph("<b>Yes — in three key ways:</b>", BODY_STYLE),
    Paragraph(
        "<b>1. Gas auction front-running:</b> Anyone can pay a higher maxPriorityFeePerGas "
        "to jump ahead of a pending tx. MEV bots routinely outbid retail users.",
        BULLET_STYLE),
    Paragraph(
        "<b>2. Validator self-dealing:</b> Block proposers can include their own transactions "
        "at zero gas cost and in any position, extracting MEV without auction overhead.",
        BULLET_STYLE),
    Paragraph(
        "<b>3. Asymmetric optimisation:</b> Sophisticated actors use highly-optimised assembly "
        "contracts (lower gas per operation) giving them cheaper execution than standard Solidity.",
        BULLET_STYLE),
    Spacer(1, 6),
    Paragraph("CODE IMPLEMENTATION — DEX.sol + Arbitrage.sol", SECTION_STYLE),
    Paragraph(
        "We minimise gas per call using immutable and constant declarations. Each SLOAD costs "
        "2 100 gas; constants and immutables cost only 3 gas per read. The checkArbitrage "
        "view function lets any user verify profitability at zero gas before committing to a tx.",
        BODY_STYLE),
    code_block([
        "// immutable: read from bytecode, not storage (~2 100 gas saved per read)",
        "IERC20  public immutable tokenA;",
        "LPToken public immutable lpToken;",
        "",
        "// constant: no SLOAD at all (3 gas vs 2 100 gas)",
        "uint256 public constant FEE_NUMERATOR = 997;",
        "",
        "// view function — zero gas to check profitability before committing",
        "function checkArbitrage(...) external view returns (bool, uint256) { ... }",
    ]),
    Spacer(1, 8),
]

# ── Q6 ────────────────────────────────────────────────────────────────
story += [
    Paragraph("Q6.  What are the various ways to minimise slippage in a swap?", Q_STYLE),
    Paragraph("ANSWER", SECTION_STYLE),
    two_col_table([
        ("Trade smaller amounts",          "Slippage ∝ f; halving dx roughly halves price impact"),
        ("Increase pool TVL",              "Larger reserves → smaller f for the same dx"),
        ("Concentrated liquidity (v3)",    "Deploy liquidity in a narrow price band, multiplying depth"),
        ("Multi-pool routing",             "Aggregators split a large order across several pools"),
        ("High-liquidity pairs",           "Stablecoin or blue-chip pairs have deep pools by default"),
        ("Set minAmountOut",               "Prevents accepting worse-than-expected rates if pool changes"),
    ], hdrs=["Method", "Mechanism"]),
    Spacer(1, 8),
    Paragraph("CODE IMPLEMENTATION — DEX.sol", SECTION_STYLE),
    Paragraph(
        "The getAmountOut() view function lets the front-end show real-time slippage "
        "estimates before a tx is submitted, directly enabling the 'trade smaller amounts' "
        "mitigation by letting users see the cost of larger trades.",
        BODY_STYLE),
    code_block([
        "/// @notice Simulate output for a given TokenA input (no state change).",
        "function getAmountOut(uint256 amountAIn) external view returns (uint256 amountBOut) {",
        "    require(amountAIn > 0 && reserveA > 0 && reserveB > 0, \"DEX: invalid input\");",
        "    uint256 aWithFee = amountAIn * FEE_NUMERATOR;",
        "    amountBOut = (reserveB * aWithFee) / (reserveA * FEE_DENOMINATOR + aWithFee);",
        "}",
    ]),
    Spacer(1, 8),
]

story.append(PageBreak())

# ── Q7 ────────────────────────────────────────────────────────────────
story += [
    Paragraph("Q7.  Plot slippage vs trade lot fraction for a constant-product AMM", Q_STYLE),
    Paragraph("DERIVATION", SECTION_STYLE),
    Paragraph(
        "Let x = reserveA, y = reserveB, dx = TokenA input, <b>f = dx / x</b> (trade lot fraction). "
        "With the 0.3% fee (997 / 1000):",
        BODY_STYLE),
    code_block([
        "dy = (y * 997 * dx) / (1000*x + 997*dx)",
        "",
        "Actual rate  = dy/dx  = 997*(y/x) / (1000 + 997*f)",
        "Spot rate    = y / x",
        "",
        "S(f) = (Actual rate - Spot rate) / Spot rate * 100%",
        "     = [ 997 / (1000 + 997f) - 1 ] * 100%",
        "     = (-3 - 997f) / (1000 + 997f)  * 100%",
    ]),
    Spacer(1, 8),
    Paragraph(
        "S(f) is always <b>negative</b> — you receive less than spot implies. "
        "At f → 0: S → −0.3% (pure fee floor). At f = 1: S = −50%.",
        BODY_STYLE),
    Spacer(1, 8),
    slip_table(),
    Spacer(1, 10),
    Paragraph(
        "<b>Key insight:</b> For small trades (f &lt; 5%), the 0.3% fee dominates. "
        "As f grows, price impact dominates and slippage approaches 50% at f = 1. "
        "This is the mathematical reason large traders always get worse execution in an AMM.",
        BODY_STYLE),
    Spacer(1, 8),
    Paragraph("CODE IMPLEMENTATION — simulation.py + theory/plot_slippage.py", SECTION_STYLE),
    Paragraph(
        "The simulation computes per-swap slippage using equation (2) from the assignment. "
        "The closed-form expression is plotted in plot_slippage.py.",
        BODY_STYLE),
    code_block([
        "# simulation.py – equation (2) applied per swap",
        "expected_rate = dex.reserveB / dex.reserveA",
        "amt_out       = dex.swap_A_for_B(amt_in)",
        "actual_rate   = amt_out / amt_in",
        "slip = (actual_rate - expected_rate) / expected_rate * 100",
        "",
        "# plot_slippage.py – closed-form S(f)",
        "f = np.linspace(0, 1, 500)",
        "S_with_fee = ((-3 - 997*f) / (1000 + 997*f)) * 100",
    ]),
    Spacer(1, 16),
    HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#d1d5db")),
    Spacer(1, 8),
    Paragraph(
        "See <b>slippage_vs_lot_fraction.png</b> in the theory/ folder for the full plot. "
        "The two curves (with fee vs without fee) diverge at small f, converging at large f "
        "where price impact dominates both.",
        NOTE_STYLE),
]

# ── Build ─────────────────────────────────────────────────────────────
doc.build(story)
print("theory.pdf generated successfully.")
