# PixelDEX — Decentralized Exchange (HW3)

> Cryptocurrencies & Smart Contracts · IIT Bombay · HW3

---

## 🌐 Live UI

**[https://e-pgd-hw-3.vercel.app](https://e-pgd-hw-3.vercel.app)**
> *Deployed on Vercel — Connect your MetaMask to Sepolia testnet to interact with the DEX*

---

## 🔗 Testnet & Deployed Contracts

**Testnet:** Sepolia (Chain ID: 11155111)  
**Deployer Address:** `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9`

| Contract | Address | Etherscan |
|----------|---------|-----------|
| TokenA (TKA) | `0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD` | [View ↗](https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD#code) |
| TokenB (TKB) | `0x74166144500f75D6B5372543000c129100Da7A46` | [View ↗](https://sepolia.etherscan.io/address/0x74166144500f75D6B5372543000c129100Da7A46#code) |
| DEX1         | `0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3` | [View ↗](https://sepolia.etherscan.io/address/0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3#code) |
| LPToken      | `0x8990AEB55ea446418c68F995a180e9040A954A74` | [View ↗](https://sepolia.etherscan.io/address/0x8990AEB55ea446418c68F995a180e9040A954A74#code) |
| DEX2         | `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91` | [View ↗](https://sepolia.etherscan.io/address/0x27572fAB42CFFe8be595b5FF32a20094ccB95A91#code) |
| Arbitrage    | `0x7753c4E551cCa47E2b81b5559CfAA1558813a07e` | [View ↗](https://sepolia.etherscan.io/address/0x7753c4E551cCa47E2b81b5559CfAA1558813a07e#code) |

> All contracts are verified on Sepolia Etherscan and can be inspected and interacted with directly.

---

## 📜 Transaction Hashes

| Action | Tx Hash | Link |
|--------|---------|------|
| Liquidity addition + LP minting | `0x3343be47099f75ba0c7efff106a0d971c923aa89f0c37da0976d1159152b1178` | [View ↗](https://sepolia.etherscan.io/tx/0x3343be47099f75ba0c7efff106a0d971c923aa89f0c37da0976d1159152b1178) |
| Swap TokenA → TokenB            | `0xf765f0dd8bf4eb6824336721719d636570cb747e04cbfcd7ab2e463fde334720` | [View ↗](https://sepolia.etherscan.io/tx/0xf765f0dd8bf4eb6824336721719d636570cb747e04cbfcd7ab2e463fde334720) |
| Swap TokenB → TokenA            | `0x0e061b719c95412fb154da8115db2de5a3ecb492e1727b3783b51b2aa8993b90` | [View ↗](https://sepolia.etherscan.io/tx/0x0e061b719c95412fb154da8115db2de5a3ecb492e1727b3783b51b2aa8993b90) |
| Liquidity removal + LP burning  | `0xd6df9031992bf73eb5ad91b5d5dc0ec0aee85202af216e003f10d924e0b3a835` | [View ↗](https://sepolia.etherscan.io/tx/0xd6df9031992bf73eb5ad91b5d5dc0ec0aee85202af216e003f10d924e0b3a835) |
| Arbitrage execution (attempt 1) | `0xdf3cbc9cdf09da5371ccaf7caf736c7591e715c22b87f884d06b873f8289f767` | [View ↗](https://sepolia.etherscan.io/tx/0xdf3cbc9cdf09da5371ccaf7caf736c7591e715c22b87f884d06b873f8289f767) |
| Arbitrage execution (attempt 2 - failed) | `0xcf473855dd4f0c6a40446e6efcc345f6f7cd312e6247489d3b080da0fc9fe694` | [View ↗](https://sepolia.etherscan.io/tx/0xcf473855dd4f0c6a40446e6efcc345f6f7cd312e6247489d3b080da0fc9fe694) |

---

## 🎬 Video Demonstration

**[Watch on YouTube / Loom](https://link-to-your-video)**  
*(Max 5 minutes — shows UI, wallet connection, swaps, liquidity, arbitrage, on-chain confirmations)*

---

## 📁 Repository Structure

```
├── contracts/
│   ├── Token.sol          # Generic ERC-20 — deploy twice for TKA and TKB
│   ├── LPToken.sol        # LP share token, mintable/burnable only by DEX
│   ├── DEX.sol            # Core constant-product AMM (0.3% fee)
│   └── Arbitrage.sol      # Cross-DEX arbitrage executor
├── scripts/
│   └── deploy.js          # Hardhat deployment script
├── simulation/
│   └── simulation.py      # N=75 transaction simulation + 7 metric plots
├── theory/
│   ├── theory_answers.md  # Theory Q1–Q7 with code references
│   ├── theory.pdf         # PDF submission of theory answers
│   └── plot_slippage.py   # Theory Q7 slippage plot
├── ui/
│   └── index.html         # Frontend — deploy to Vercel
├── hardhat.config.js
├── package.json
└── README.md
```

---

## 🚀 Step-by-Step User Guide

### 1. Access the Deployed UI

Open **[https://your-project.vercel.app](https://your-project.vercel.app)** in a browser with MetaMask installed.

### 2. Connect Your Wallet

1. Click **"Connect Wallet"** in the top-right corner.
2. MetaMask will prompt you — click **Approve**.
3. Make sure you are on the **Sepolia testnet** (chain ID 11155111).
   - In MetaMask: Networks → Add Network → Sepolia.
   - Get Sepolia ETH from [https://sepoliafaucet.com](https://sepoliafaucet.com).

### 3. Obtain Test Tokens (TKA / TKB)

**Option A — Via Etherscan (easiest):**
1. Go to the [TokenA contract on Etherscan](https://sepolia.etherscan.io/address/0x...).
2. Click **Contract → Write Contract → Connect to Web3**.
3. Call `mint(yourAddress, 10000000000000000000000)` to mint 10 000 TKA.
4. Repeat for TokenB.

**Option B — Via the deployed UI (if minting is exposed):**
The UI will show your current TKA/TKB balance in the Swap and Liquidity panels.

### 4. Add Liquidity and Receive LP Tokens

1. Go to the **Liquidity** tab in the UI.
2. Under **"Add Liquidity"**, enter an amount of TokenA (e.g. `100`).
3. The TokenB amount auto-fills to preserve the current pool ratio.
4. Click **"Add Liquidity"** and confirm the two approval txs + one deposit tx in MetaMask.
5. Your LP Token balance (LPT) will appear in the **"Remove Liquidity"** section.

### 5. Perform a Swap

1. Go to the **Swap** tab.
2. Enter the amount of TokenA you want to sell.
3. The expected TokenB output and slippage estimate appear instantly.
4. Click **"Swap"** and confirm in MetaMask.
5. Use the **⇅ button** to swap in the reverse direction (TKB → TKA).

### 6. Remove Liquidity

1. Go to the **Liquidity** tab → **"Remove Liquidity"** section.
2. Enter the number of LP tokens to burn.
3. The expected TKA and TKB return amounts are shown.
4. Click **"Remove Liquidity"** and confirm in MetaMask.

### 7. View Pool Reserves and Spot Price

- The **stats bar** at the top always shows live Reserve A, Reserve B, Spot Price, and LP Supply.
- The **Pool Info** tab shows all metrics including your pool share and underlying value.

---

## 🔧 Local Development Setup

```bash
# 1. Install dependencies
npm install

# 2. Copy and fill in environment variables
cp .env.example .env
# PRIVATE_KEY=your_deployer_private_key
# SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
# ETHERSCAN_API_KEY=YOUR_KEY

# 3. Compile
npx hardhat compile

# 4. Deploy to Sepolia
npx hardhat run scripts/deploy.js --network sepolia

# 5. Verify on Etherscan (example)
npx hardhat verify --network sepolia <TOKENA_ADDR> "Token A" "TKA" 1000000
npx hardhat verify --network sepolia <TOKENB_ADDR> "Token B" "TKB" 1000000
npx hardhat verify --network sepolia <DEX1_ADDR> <TOKENA_ADDR> <TOKENB_ADDR>
npx hardhat verify --network sepolia <ARB_ADDR>

# 6. Run simulation
pip install matplotlib numpy
cd simulation && python simulation.py

# 7. Generate theory PDF
cd theory && python make_pdf.py
```

---

## 🌐 Deploying the UI to Vercel

1. Push this repository to GitHub.
2. Go to [vercel.com](https://vercel.com) → **New Project** → Import your repo.
3. Set **Root Directory** to `ui/`.
4. **No build step needed** — it is a static HTML file.
5. Click **Deploy**.
6. After deployment, open `ui/index.html` and replace the `CONFIG` object addresses with your deployed contract addresses, then push again.

---

## 📐 Contract Architecture

```
User ──► DEX.sol ──► LPToken.sol  (mint/burn, DEX is sole owner)
              │
              ├──► IERC20 TokenA
              └──► IERC20 TokenB

Arbitrageur ──► Arbitrage.sol ──► DEX1.sol
                              └──► DEX2.sol
```

**Security measures implemented:**
- `ReentrancyGuard` on all state-changing DEX functions
- Solidity 0.8+ checked arithmetic (no SafeMath needed)
- `immutable` token addresses (prevent post-deployment tampering)
- Checks-Effects-Interactions pattern throughout
- `onlyOwner` on LP mint/burn (DEX is the only owner)
- `require()` on all inputs, ratios, and transfer return values
- Off-chain simulation in Arbitrage before executing (saves gas on failed attempts)

---

## 📄 Theory

Theory answers (Q1–Q7) with code implementation references:
- Markdown: `theory/theory_answers.md`
- PDF: `theory/theory.pdf`
