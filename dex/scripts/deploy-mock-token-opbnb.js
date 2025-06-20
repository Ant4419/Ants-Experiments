const { ethers } = require("ethers");
const fs = require("fs");

async function main() {
  const provider = new ethers.JsonRpcProvider("https://sepolia.infura.io/v3/aad532756b6e44b6a10d9922a151240e");

  // Use your real testnet private key
  const PRIVATE_KEY = "62d97175c44bebee30b1f2f4b032567303ba1b0e0ab750cff682b1712e0fced1";
  const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

  // Load ABI and bytecode from compiled JSON (from Foundry or Hardhat)
  const artifact = JSON.parse(fs.readFileSync("./out/TestToken.sol/TestToken.json", "utf8"));
  const abi = artifact.abi;
  const bytecode = artifact.bytecode.object;

  const factory = new ethers.ContractFactory(abi, bytecode, wallet);

  // Deploy multiple tokens
  const tokens = [
    { name: "TestTokenA", symbol: "TKA", supply: ethers.parseEther("1000000") },
    { name: "TestTokenB", symbol: "TKB", supply: ethers.parseEther("500000") },
    { name: "TestTokenC", symbol: "TKC", supply: ethers.parseEther("250000") },
    { name: "TestTokenD", symbol: "TKD", supply: ethers.parseEther("750000") },
  ];

  for (const t of tokens) {
    const token = await factory.deploy(t.name, t.symbol, t.supply);
    await token.waitForDeployment();
    console.log(`✅ Deployed ${t.name} (${t.symbol}) at:`, await token.getAddress());
  }
}

main().catch(console.error);
