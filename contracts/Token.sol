// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title Token
 * @notice Generic ERC-20 token. Deploy twice to get TokenA and TokenB.
 *         The owner (deployer) can mint additional tokens - useful for
 *         distributing test tokens to users on a testnet.
 */
contract Token is ERC20, Ownable {
    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply   // in whole tokens (NOT wei)
    ) ERC20(name, symbol) Ownable(msg.sender) {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }

    /// @notice Mint new tokens. Only the contract owner can call this.
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
