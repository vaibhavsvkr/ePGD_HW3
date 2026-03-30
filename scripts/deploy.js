// scripts/deploy.js
// Run: npx hardhat run scripts/deploy.js --network sepolia

const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  const INITIAL_SUPPLY = 1_000_000n; // 1 million tokens each

  // ── 1. Deploy TokenA ────────────────────────────────────────────────
  const Token = await ethers.getContractFactory("Token");
  const tokenA = await Token.deploy("Token A", "TKA", INITIAL_SUPPLY);
  await tokenA.waitForDeployment();
  console.log("TokenA deployed to:", await tokenA.getAddress());

  // ── 2. Deploy TokenB ────────────────────────────────────────────────
  const tokenB = await Token.deploy("Token B", "TKB", INITIAL_SUPPLY);
  await tokenB.waitForDeployment();
  console.log("TokenB deployed to:", await tokenB.getAddress());

  // ── 3. Deploy DEX (also deploys LPToken internally) ─────────────────
  const DEX = await ethers.getContractFactory("DEX");
  const dex = await DEX.deploy(
    await tokenA.getAddress(),
    await tokenB.getAddress()
  );
  await dex.waitForDeployment();
  const dexAddr = await dex.getAddress();
  console.log("DEX deployed to:", dexAddr);

  const lpTokenAddr = await dex.lpToken();
  console.log("LPToken deployed to (via DEX):", lpTokenAddr);

  // ── 4. Deploy a second DEX instance (for arbitrage) ─────────────────
  const dex2 = await DEX.deploy(
    await tokenA.getAddress(),
    await tokenB.getAddress()
  );
  await dex2.waitForDeployment();
  const dex2Addr = await dex2.getAddress();
  console.log("DEX2 deployed to:", dex2Addr);

  // ── 5. Deploy Arbitrage contract ─────────────────────────────────────
  const Arbitrage = await ethers.getContractFactory("Arbitrage");
  const arb = await Arbitrage.deploy();
  await arb.waitForDeployment();
  console.log("Arbitrage deployed to:", await arb.getAddress());

  // ── 6. Seed DEX1 with initial liquidity ──────────────────────────────
  const AMOUNT_A = ethers.parseEther("1000");
  const AMOUNT_B = ethers.parseEther("2000");

  await tokenA.approve(dexAddr, AMOUNT_A);
  await tokenB.approve(dexAddr, AMOUNT_B);
  await dex.addLiquidity(AMOUNT_A, AMOUNT_B);
  console.log("Initial liquidity added to DEX1: 1000 TKA / 2000 TKB");

  // ── 7. Seed DEX2 with different ratio (creates arbitrage opportunity) ─
  const AMOUNT_A2 = ethers.parseEther("1000");
  const AMOUNT_B2 = ethers.parseEther("2100"); // different ratio!
  await tokenA.approve(dex2Addr, AMOUNT_A2);
  await tokenB.approve(dex2Addr, AMOUNT_B2);
  await dex2.addLiquidity(AMOUNT_A2, AMOUNT_B2);
  console.log("Initial liquidity added to DEX2: 1000 TKA / 2100 TKB");

  console.log("\n──── Deployment Summary ────");
  console.log("TokenA:    ", await tokenA.getAddress());
  console.log("TokenB:    ", await tokenB.getAddress());
  console.log("DEX1:      ", dexAddr);
  console.log("LPToken:   ", lpTokenAddr);
  console.log("DEX2:      ", dex2Addr);
  console.log("Arbitrage: ", await arb.getAddress());
  console.log("────────────────────────────");
  console.log("\nNext: verify contracts on Etherscan using:");
  console.log(`  npx hardhat verify --network sepolia ${await tokenA.getAddress()} "Token A" "TKA" 1000000`);
  console.log(`  npx hardhat verify --network sepolia ${dexAddr} ${await tokenA.getAddress()} ${await tokenB.getAddress()}`);
}

main().catch((err) => { console.error(err); process.exitCode = 1; });
