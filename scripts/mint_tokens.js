// scripts/mint_tokens.js
// Mint tokens to test users for the DEX

const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Minting tokens from:", deployer.address);

  const TOKEN_A = "0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD";
  const TOKEN_B = "0x74166144500f75D6B5372543000c129100Da7A46";

  const Token = await ethers.getContractFactory("Token");
  const tokenA = Token.attach(TOKEN_A);
  const tokenB = Token.attach(TOKEN_B);

  // Amount to mint (for testing)
  const MINT_AMOUNT = ethers.parseEther("10000"); // 10,000 tokens

  console.log("\nMinting 10,000 TokenA to:", deployer.address);
  const txA = await tokenA.mint(deployer.address, MINT_AMOUNT);
  await txA.wait();
  console.log("✓ TokenA minted. Tx:", txA.hash);

  console.log("\nMinting 10,000 TokenB to:", deployer.address);
  const txB = await tokenB.mint(deployer.address, MINT_AMOUNT);
  await txB.wait();
  console.log("✓ TokenB minted. Tx:", txB.hash);

  // Check balances
  const balA = await tokenA.balanceOf(deployer.address);
  const balB = await tokenB.balanceOf(deployer.address);
  
  console.log("\n──── Balances ────");
  console.log("TokenA:", ethers.formatEther(balA), "TKA");
  console.log("TokenB:", ethers.formatEther(balB), "TKB");
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
