// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title LPToken
 * @notice Liquidity Provider token representing share of the DEX reserves.
 *
 * Security:  Only the DEX contract (set as owner at deployment) is permitted
 *            to mint or burn tokens.  This prevents unauthorised supply changes.
 *
 * Deployment: This contract is deployed *inside* the DEX constructor so that
 *             msg.sender (= the DEX) automatically becomes the Ownable owner.
 *             No separate ownership transfer is required.
 */
contract LPToken is ERC20, Ownable {
    constructor() ERC20("DEX LP Token", "LPT") Ownable(msg.sender) {}

    /// @notice Mint LP tokens to `to`. Callable only by the DEX contract.
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    /// @notice Burn LP tokens from `from`. Callable only by the DEX contract.
    function burn(address from, uint256 amount) external onlyOwner {
        _burn(from, amount);
    }
}
