const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying tokens with account:", deployer.address);

  const Token = await ethers.getContractFactory("TestToken");

  // Deploy TokenA with 1 million initial supply
  const tokenA = await Token.deploy("Token A", "TKNA", ethers.utils.parseEther("1000000"));
  await tokenA.deployed();
  console.log("Token A deployed at:", tokenA.address);

  // You can deploy more tokens similarly here
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
