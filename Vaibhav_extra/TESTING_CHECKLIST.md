# Testing Checklist & Transaction Tracker

**Date:** March 30, 2026  
**Wallet:** `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9`  
**UI:** https://e-pgd-hw-3.vercel.app

---

## ✅ Pre-Flight Checklist

- [ ] Brave browser installed
- [ ] MetaMask installed and wallet imported
- [ ] Switched to Sepolia network
- [ ] Have ~0.2 Sepolia ETH for gas

---

## 📝 STEP 1: Mint Test Tokens

### Mint TokenA
- [ ] Go to: https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD#writeContract
- [ ] Connect wallet
- [ ] Function #2 `mint`
  - to: `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9`
  - amount: `100000000000000000000000`
- [ ] Click Write → Confirm
- **TX Hash:** `_________________________________`

### Mint TokenB
- [ ] Go to: https://sepolia.etherscan.io/address/0x74166144500f75D6B5372543000c129100Da7A46#writeContract
- [ ] Function #2 `mint`
  - to: `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9`
  - amount: `100000000000000000000000`
- [ ] Click Write → Confirm
- **TX Hash:** `_________________________________`

---

## 📝 STEP 2: Test DEX via UI

### 2.1 Add Liquidity
- [ ] Open: https://e-pgd-hw-3.vercel.app
- [ ] Connect wallet
- [ ] Go to "Add Liquidity" tab
- [ ] Enter: TokenA = 1000, TokenB = 2000
- [ ] Approve TokenA
- [ ] Approve TokenB
- [ ] Click "Add Liquidity"
- **TX Hash:** `_________________________________`

### 2.2 Swap TokenA → TokenB
- [ ] Go to "Swap" tab
- [ ] Select: TokenA → TokenB
- [ ] Amount: 100 TokenA
- [ ] Click "Swap"
- **TX Hash:** `_________________________________`

### 2.3 Swap TokenB → TokenA
- [ ] Switch: TokenB → TokenA
- [ ] Amount: 100 TokenB
- [ ] Click "Swap"
- **TX Hash:** `_________________________________`

### 2.4 Remove Liquidity
- [ ] Go to "Remove Liquidity" tab
- [ ] Amount: 500 LP tokens (or half)
- [ ] Approve LP Token
- [ ] Click "Remove Liquidity"
- **TX Hash:** `_________________________________`

---

## 📝 STEP 3: Test Arbitrage (Etherscan)

### 3.1 Setup DEX2 with Different Price
- [ ] Approve TokenA for DEX2:
  - Go to: https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD#writeContract
  - Function #1 `approve`
  - spender: `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91`
  - amount: `10000000000000000000000`
  
- [ ] Approve TokenB for DEX2:
  - Go to: https://sepolia.etherscan.io/address/0x74166144500f75D6B5372543000c129100Da7A46#writeContract
  - Function #1 `approve`
  - spender: `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91`
  - amount: `10000000000000000000000`

- [ ] Add liquidity to DEX2:
  - Go to: https://sepolia.etherscan.io/address/0x27572fAB42CFFe8be595b5FF32a20094ccB95A91#writeContract
  - Function #1 `addLiquidity`
  - amountA: `1000000000000000000000` (1000 TokenA)
  - amountB: `2200000000000000000000` (2200 TokenB - different ratio!)

### 3.2 Fund Arbitrage Contract
- [ ] Transfer TokenA to Arbitrage:
  - Go to: https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD#writeContract
  - Function #3 `transfer`
  - to: `0x7753c4E551cCa47E2b81b5559CfAA1558813a07e`
  - amount: `1000000000000000000000`

### 3.3 Profitable Arbitrage
- [ ] Go to: https://sepolia.etherscan.io/address/0x7753c4E551cCa47E2b81b5559CfAA1558813a07e#writeContract
- [ ] Function #2 `executeArbitrage`
  - dex1: `0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3`
  - dex2: `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91`
  - amountIn: `10000000000000000000`
  - minProfitThreshold: `0`
- **TX Hash:** `_________________________________`

### 3.4 Failed Arbitrage
- [ ] Function #2 `executeArbitrage`
  - dex1: `0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3`
  - dex2: `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91`
  - amountIn: `10000000000000000000`
  - minProfitThreshold: `10000000000000000000` (high threshold = will fail)
- **TX Hash (Failed):** `_________________________________`

---

## 📝 STEP 4: Record Video

- [ ] Screen recording tool ready
- [ ] Record 5-minute demo showing:
  - [ ] GitHub repo
  - [ ] Verified contracts on Etherscan
  - [ ] UI interaction (connect wallet, swap)
  - [ ] Transaction confirmation
  - [ ] LP operations
- **Video Link:** `_________________________________`

---

## 📝 STEP 5: Update README

- [ ] Copy all transaction hashes above
- [ ] Update README.md with TX hashes
- [ ] Add video link
- [ ] Push to GitHub:
  ```bash
  git add README.md
  git commit -m "Add transaction hashes and video demo"
  git push
  ```

---

## ✅ Final Checklist

- [ ] All 6 transaction hashes recorded
- [ ] Video uploaded and link added
- [ ] README updated on GitHub
- [ ] All contracts verified (already done ✅)
- [ ] UI working (already done ✅)
- [ ] Simulation complete (already done ✅)
- [ ] Theory answered (already done ✅)

---

## 🆘 Quick Links

- GitHub: https://github.com/vaibhavsvkr/ePGD_HW3
- Live UI: https://e-pgd-hw-3.vercel.app
- TokenA: https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD
- TokenB: https://sepolia.etherscan.io/address/0x74166144500f75D6B5372543000c129100Da7A46
- DEX1: https://sepolia.etherscan.io/address/0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3
- DEX2: https://sepolia.etherscan.io/address/0x27572fAB42CFFe8be595b5FF32a20094ccB95A91
- Arbitrage: https://sepolia.etherscan.io/address/0x7753c4E551cCa47E2b81b5559CfAA1558813a07e

Good luck! 🚀
