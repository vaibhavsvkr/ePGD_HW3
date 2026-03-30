// Test Arbitrage Script
const { ethers } = require("hardhat");

async function main() {
  const [signer] = await ethers.getSigners();
  console.log("Testing arbitrage with:", signer.address);

  const tokenA = "0xa3825a41bCE54C9ae19c36984Cf8a2f983da6ebD";
  const tokenB = "0x74166144500f75D6B5372543000c129100Da7A46";
  const dex1 = "0xd01a010F8A1e60D8D0e0Fe5890478fc24f79bCB3";
  const dex2 = "0x27572fAB42CFFe8be595b5FF32a20094ccB95A91";
  const arbAddress = "0x7753c4E551cCa47E2b81b5559CfAA1558813a07e";

  const Arbitrage = await ethers.getContractFactory("Arbitrage");
  const arb = Arbitrage.attach(arbAddress);

  console.log("\n1. Checking arbitrage opportunity...");
  try {
    const result = await arb.simulateArbitrage(
      dex1,
      dex2,
      tokenA,
      tokenB,
      ethers.parseEther("10"),
      true // A to B direction
    );
    console.log("Expected profit:", ethers.formatEther(result[0]), "tokens");
    console.log("Direction A→B:", result[1]);
  } catch (err) {
    console.log("Simulation failed:", err.message);
  }

  console.log("\n2. Attempting profitable arbitrage...");
  try {
    const tx = await arb.executeArbitrage(
      dex1,
      dex2,
      tokenA,
      tokenB,
      ethers.parseEther("10"),
      true,
      { gasLimit: 500000 }
    );
    console.log("✅ Transaction sent:", tx.hash);
    await tx.wait();
    console.log("✅ Arbitrage successful!");
  } catch (err) {
    console.log("❌ Arbitrage failed:", err.message);
    if (err.transaction) {
      console.log("Failed TX hash:", err.transaction.hash);
    }
  }

  console.log("\n3. Attempting failed arbitrage (opposite direction)...");
  try {
    const tx = await arb.executeArbitrage(
      dex1,
      dex2,
      tokenA,
      tokenB,
      ethers.parseEther("10"),
      false, // Opposite direction - likely to fail
      { gasLimit: 500000 }
    );
    console.log("Transaction sent:", tx.hash);
    await tx.wait();
    console.log("Unexpectedly succeeded!");
  } catch (err) {
    console.log("✅ Failed as expected:", err.message);
    if (err.transaction) {
      console.log("Failed TX hash:", err.transaction.hash);
    }
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
