# Deployed Contract Addresses on Sepolia

## Network: Sepolia Testnet
**Deployer Address:** `0x4696D77bc398580e5F9ec095ba2F9c78419eb6B9`

## Contract Addresses

| Contract | Address | Etherscan Link |
|----------|---------|----------------|
| TokenA | `0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD` | [View on Etherscan](https://sepolia.etherscan.io/address/0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD) |
| TokenB | `0x74166144500f75D6B5372543000c129100Da7A46` | [View on Etherscan](https://sepolia.etherscan.io/address/0x74166144500f75D6B5372543000c129100Da7A46) |
| DEX1 | `0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3` | [View on Etherscan](https://sepolia.etherscan.io/address/0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3) |
| LPToken | `0x8990AEB55ea446418c68F995a180e9040A954A74` | [View on Etherscan](https://sepolia.etherscan.io/address/0x8990AEB55ea446418c68F995a180e9040A954A74) |
| DEX2 | `0x27572fAB42CFFe8be595b5FF32a20094ccB95A91` | [View on Etherscan](https://sepolia.etherscan.io/address/0x27572fAB42CFFe8be595b5FF32a20094ccB95A91) |
| Arbitrage | `0x7753c4E551cCa47E2b81b5559CfAA1558813a07e` | [View on Etherscan](https://sepolia.etherscan.io/address/0x7753c4E551cCa47E2b81b5559CfAA1558813a07e) |

## Next Steps

### 1. Verify Contracts on Etherscan
```bash
npx hardhat verify --network sepolia 0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD "Token A" "TKA" 1000000
npx hardhat verify --network sepolia 0x74166144500f75D6B5372543000c129100Da7A46 "Token B" "TKB" 1000000
npx hardhat verify --network sepolia 0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3 0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD 0x74166144500f75D6B5372543000c129100Da7A46
npx hardhat verify --network sepolia 0x27572fAB42CFFe8be595b5FF32a20094ccB95A91 0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD 0x74166144500f75D6B5372543000c129100Da7A46
npx hardhat verify --network sepolia 0x7753c4E551cCa47E2b81b5559CfAA1558813a07e
```

### 2. Update UI Config
Edit `ui/index.html` and update the CONFIG object:
```javascript
const CONFIG = {
  TOKEN_A:   "0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD",
  TOKEN_B:   "0x74166144500f75D6B5372543000c129100Da7A46",
  DEX1:      "0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3",
  DEX2:      "0x27572fAB42CFFe8be595b5FF32a20094ccB95A91",
  LP_TOKEN:  "0x8990AEB55ea446418c68F995a180e9040A954A74",
  ARBITRAGE: "0x7753c4E551cCa47E2b81b5559CfAA1558813a07e",
};
```
