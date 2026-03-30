# Complete Homework Submission Guide

## 📋 What You Need to Complete

Your GitHub Repo: https://github.com/vaibhavsvkr/ePGD_HW3  
Your Live UI: https://e-pgd-hw-3.vercel.app  
Your Wallet: `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9`

---

## ✅ Already Completed

- ✅ All contracts deployed and verified on Sepolia
- ✅ UI deployed to Vercel
- ✅ Simulation completed (Task 2)
- ✅ Theory questions answered (Task 6)
- ✅ Slippage plots generated (Task 6, Q7)

---

## 📝 Still Need to Complete

### **Task 1**: Get Transaction Hashes (15 min)
### **Task 2**: Test Arbitrage Scenarios (10 min)
### **Task 3**: Record Video Demo (5 min)
### **Task 4**: Update README with all links (5 min)

---

# STEP-BY-STEP INSTRUCTIONS

## 🎯 STEP 1: Mint Test Tokens (5 min)

### 1.1 Go to TokenA Contract on Etherscan
**URL:** https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD#writeContract

### 1.2 Connect Your Wallet
- Click **"Connect to Web3"**
- Connect MetaMask (make sure you're on Sepolia)

### 1.3 Mint TokenA
- Find function **#2 `mint`**
- **to (address):** `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9` (your wallet)
- **amount (uint256):** `100000000000000000000000` (100,000 tokens with 18 decimals)
- Click **"Write"** → Confirm in MetaMask
- **Copy the transaction hash** → Save it as "Mint TokenA"

### 1.4 Mint TokenB
**URL:** https://sepolia.etherscan.io/address/0x74166144500f75D6B5372543000c129100Da7A46#writeContract

- Repeat the same process:
- Connect wallet
- Function **#2 `mint`**
- **to:** `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9`
- **amount:** `100000000000000000000000`
- Click **"Write"** → Confirm
- **Copy the transaction hash** → Save it as "Mint TokenB"

---

## 🎯 STEP 2: Test DEX Functions & Get Transaction Hashes (20 min)

### 2.1 Open Your UI
**URL:** https://e-pgd-hw-3.vercel.app

### 2.2 Connect Wallet
- Click **"Connect Wallet"**
- Approve MetaMask connection
- Make sure you're on **Sepolia** network

---

### 2.3 ADD LIQUIDITY (Get TX Hash #1)

1. **Go to "Add Liquidity" tab**
2. **Enter amounts:**
   - TokenA: `1000`
   - TokenB: `2000`
   - (This is the initial ratio: 1:2)
3. **Click "Approve TokenA"** → Confirm in MetaMask
4. **Click "Approve TokenB"** → Confirm in MetaMask
5. **Click "Add Liquidity"** → Confirm in MetaMask
6. **Wait for confirmation**
7. **Copy the transaction hash from MetaMask or the UI**

**Save as:** "Add Liquidity TX Hash"

---

### 2.4 SWAP TokenA → TokenB (Get TX Hash #2)

1. **Go to "Swap" tab**
2. **Select:** TokenA → TokenB
3. **Enter amount:** `100` TokenA
4. **Click "Approve TokenA"** (if not already approved)
5. **Click "Swap"** → Confirm in MetaMask
6. **Copy the transaction hash**

**Save as:** "Swap A→B TX Hash"

---

### 2.5 SWAP TokenB → TokenA (Get TX Hash #3)

1. **Switch direction:** TokenB → TokenA
2. **Enter amount:** `100` TokenB
3. **Click "Approve TokenB"** (if not already approved)
4. **Click "Swap"** → Confirm in MetaMask
5. **Copy the transaction hash**

**Save as:** "Swap B→A TX Hash"

---

### 2.6 REMOVE LIQUIDITY (Get TX Hash #4)

1. **Go to "Remove Liquidity" tab**
2. **Check your LP Token balance** (should show on the page)
3. **Enter amount to remove:** e.g., `500` LP tokens (or half of what you have)
4. **Click "Approve LP Token"** → Confirm
5. **Click "Remove Liquidity"** → Confirm in MetaMask
6. **Copy the transaction hash**

**Save as:** "Remove Liquidity TX Hash"

---

## 🎯 STEP 3: Test Arbitrage via Etherscan (15 min)

### 3.1 Add Liquidity to DEX2 (Create Price Difference)

**DEX2 Contract:** https://sepolia.etherscan.io/address/0x27572fAB42CFFe8be595b5FF32a20094ccB95A91#writeContract

1. **Connect wallet**
2. **First, approve tokens for DEX2:**

**Approve TokenA:**
- Go to TokenA contract: https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD#writeContract
- Function **#1 `approve`**
- **spender:** `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91` (DEX2)
- **amount:** `10000000000000000000000` (10,000 tokens)
- Click "Write" → Confirm

**Approve TokenB:**
- Go to TokenB contract: https://sepolia.etherscan.io/address/0x74166144500f75D6B5372543000c129100Da7A46#writeContract
- Function **#1 `approve`**
- **spender:** `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91` (DEX2)
- **amount:** `10000000000000000000000` (10,000 tokens)
- Click "Write" → Confirm

3. **Add liquidity to DEX2 with DIFFERENT ratio:**
- Go back to DEX2: https://sepolia.etherscan.io/address/0x27572fAB42CFFe8be595b5FF32a20094ccB95A91#writeContract
- Function **#1 `addLiquidity`**
- **amountA:** `1000000000000000000000` (1,000 TokenA)
- **amountB:** `2200000000000000000000` (2,200 TokenB) ← **Different ratio!**
- Click "Write" → Confirm

---

### 3.2 Fund Arbitrage Contract with Tokens

**Give TokenA to Arbitrage contract:**
- Go to TokenA: https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD#writeContract
- Function **#3 `transfer`**
- **to:** `0x7753c4E551cCa47E2b81b5559CfAA1558813a07e` (Arbitrage contract)
- **amount:** `1000000000000000000000` (1,000 tokens)
- Click "Write" → Confirm

---

### 3.3 Execute PROFITABLE Arbitrage

**Arbitrage Contract:** https://sepolia.etherscan.io/address/0x7753c4E551cCa47E2b81b5559CfAA1558813a07e#writeContract

1. **Connect wallet**
2. **Function #2 `executeArbitrage`**
   - **dex1:** `0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3` (DEX1)
   - **dex2:** `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91` (DEX2)
   - **amountIn:** `10000000000000000000` (10 TokenA)
   - **minProfitThreshold:** `0`
3. **Click "Write"** → Confirm in MetaMask
4. **Copy the transaction hash**

**Save as:** "Profitable Arbitrage TX Hash"

---

### 3.4 Execute FAILED Arbitrage

**Make DEX prices similar (reduce arbitrage opportunity):**

1. Do a few swaps on DEX2 to balance prices
2. Then try arbitrage again:

**Arbitrage Contract:** https://sepolia.etherscan.io/address/0x7753c4E551cCa47E2b81b5559CfAA1558813a07e#writeContract

- Function **#2 `executeArbitrage`**
- **dex1:** `0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3`
- **dex2:** `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91`
- **amountIn:** `10000000000000000000`
- **minProfitThreshold:** `10000000000000000000` ← **High threshold = will fail**
- Click "Write" → **This should FAIL/REVERT**
- **Copy the transaction hash** (even failed transactions have hashes)

**Save as:** "Failed Arbitrage TX Hash"

---

## 🎯 STEP 4: Record Video Demo (5 min max)

### 4.1 Use Screen Recording Tool
**Options:**
- **Mac:** QuickTime Player (File → New Screen Recording)
- **Windows:** Xbox Game Bar (Win + G)
- **Browser Extension:** Loom (https://loom.com)
- **OBS Studio** (free, all platforms)

### 4.2 What to Show in Video (Max 5 minutes!)

**Script:**

1. **Introduction (30 sec)**
   - "This is my DEX project deployed on Sepolia testnet"
   - Show GitHub repo: https://github.com/vaibhavsvkr/ePGD_HW3
   - Show live UI: https://e-pgd-hw-3.vercel.app

2. **Contract Verification (30 sec)**
   - Open one contract on Etherscan (e.g., DEX1)
   - Show it's verified (green checkmark)
   - Briefly show the code tab

3. **UI Interaction (2 min)**
   - Connect MetaMask
   - Show token balances
   - Perform a swap (any direction)
   - Wait for confirmation
   - Show transaction on Etherscan

4. **Add/Remove Liquidity (1 min)**
   - Add small amount of liquidity
   - Show LP tokens minted
   - Or remove liquidity (show LP tokens burned)

5. **Show All Deployed Contracts (30 sec)**
   - Briefly click through the Etherscan links for all 6 contracts
   - Show they're all verified

6. **Conclusion (30 sec)**
   - "All transaction hashes are documented in the README"
   - "Theory questions answered in theory.pdf"
   - "Simulation results in simulation/ folder"

### 4.3 Upload Video
**Options:**
- **YouTube:** Upload as unlisted (get shareable link)
- **Loom:** Automatically gives you a link
- **Google Drive:** Upload, make it "Anyone with link can view"
- **Dropbox:** Share link

**Copy the video link** → You'll add this to README

---

## 🎯 STEP 5: Update README with All Transaction Hashes

### 5.1 Edit README.md
Add your transaction hashes to the README:

```markdown
## 📜 Transaction Hashes

| Action | Tx Hash | Link |
|--------|---------|------|
| Liquidity addition + LP minting | `0xYOUR_TX_HASH` | [View ↗](https://sepolia.etherscan.io/tx/0xYOUR_TX_HASH) |
| Liquidity removal + LP burning  | `0xYOUR_TX_HASH` | [View ↗](https://sepolia.etherscan.io/tx/0xYOUR_TX_HASH) |
| Swap TokenA → TokenB            | `0xYOUR_TX_HASH` | [View ↗](https://sepolia.etherscan.io/tx/0xYOUR_TX_HASH) |
| Swap TokenB → TokenA            | `0xYOUR_TX_HASH` | [View ↗](https://sepolia.etherscan.io/tx/0xYOUR_TX_HASH) |
| Profitable arbitrage            | `0xYOUR_TX_HASH` | [View ↗](https://sepolia.etherscan.io/tx/0xYOUR_TX_HASH) |
| Failed arbitrage (low profit)   | `0xYOUR_TX_HASH` | [View ↗](https://sepolia.etherscan.io/tx/0xYOUR_TX_HASH) |

## 🎬 Video Demonstration

**[Watch Demo Video](YOUR_VIDEO_LINK_HERE)**  
*(5 minute walkthrough showing UI interaction, wallet connection, swaps, liquidity operations, and on-chain confirmations)*
```

### 5.2 Push Changes to GitHub
```bash
cd /path/to/dex_project
git add README.md
git commit -m "Add transaction hashes and video demo"
git push
```

---

## 🎯 STEP 6: Final Submission Checklist

Before submitting, verify:

### Files in Repository
- ✅ `contracts/` - All Solidity contracts (Token.sol, DEX.sol, LPToken.sol, Arbitrage.sol)
- ✅ `scripts/deploy.js` - Deployment script
- ✅ `ui/index.html` - Frontend UI
- ✅ `simulation/simulation.py` - Simulation script
- ✅ `simulation/dex_simulation_metrics.png` - Simulation plots
- ✅ `theory/theory.pdf` or `theory_answers.md` - Theory answers
- ✅ `theory/slippage_vs_lot_fraction.png` - Slippage plot
- ✅ `README.md` - Complete with all addresses, TX hashes, video link

### README Must Include
- ✅ Live UI URL (Vercel)
- ✅ Testnet name (Sepolia)
- ✅ All 6 contract addresses with Etherscan verification links
- ✅ 6 transaction hashes with links
- ✅ Video demonstration link
- ✅ Instructions for using the DEX

### Contracts on Etherscan
- ✅ All contracts verified (green checkmark)
- ✅ Can interact with contracts via "Read/Write Contract" tabs

### UI on Vercel
- ✅ Loads without errors
- ✅ Can connect MetaMask
- ✅ Shows correct contract addresses in network requests
- ✅ Swap functionality works
- ✅ Add/remove liquidity works

### Video Demo
- ✅ Max 5 minutes
- ✅ Shows wallet connection
- ✅ Shows at least one swap
- ✅ Shows liquidity operation
- ✅ Shows Etherscan confirmation
- ✅ Publicly accessible link

---

## 📝 Summary of What You Need to Do

1. **Mint tokens** (2 transactions via Etherscan)
2. **Test UI:**
   - Add liquidity (1 TX)
   - Swap A→B (1 TX)
   - Swap B→A (1 TX)
   - Remove liquidity (1 TX)
3. **Test Arbitrage:**
   - Set up DEX2 with different price (3 TXs: 2 approvals + add liquidity)
   - Fund arbitrage contract (1 TX)
   - Execute profitable arbitrage (1 TX)
   - Execute failed arbitrage (1 TX)
4. **Record 5-min video** showing UI interactions
5. **Update README** with all TX hashes and video link
6. **Push to GitHub**

---

## 🆘 Quick Reference

**Your Addresses:**
- Wallet: `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9`
- TokenA: `0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD`
- TokenB: `0x74166144500f75D6B5372543000c129100Da7A46`
- DEX1: `0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3`
- DEX2: `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91`
- LPToken: `0x8990AEB55ea446418c68F995a180e9040A954A74`
- Arbitrage: `0x7753c4E551cCa47E2b81b5559CfAA1558813a07e`

**Your Links:**
- GitHub: https://github.com/vaibhavsvkr/ePGD_HW3
- Live UI: https://e-pgd-hw-3.vercel.app

Good luck! 🚀
