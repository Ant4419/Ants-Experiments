const { ethers } = require("ethers");

async function main() {
  const provider = new ethers.JsonRpcProvider("http://localhost:8545");
  const wallet = new ethers.Wallet("YOUR_PRIVATE_KEY_HERE", provider);

  const abi = [
    "constructor(string memory name, string memory symbol, uint256 initialSupply)",
  ];

  const bytecode = "YOUR_COMPILED_BYTECODE_HERE";

  const factory = new ethers.ContractFactory(abi, bytecode, wallet);

  const token = await factory.deploy("MockBNB", "mBNB", ethers.parseEther("1000000"));
  await token.waitForDeployment();

  console.log("Mock token deployed at:", await token.getAddress());
}

main().catch(console.error);
