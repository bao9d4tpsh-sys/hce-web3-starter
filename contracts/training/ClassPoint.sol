// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ClassPoint is ERC20, Ownable {
    address public classFund;
    uint256 public feeBps = 100;
    uint256 public maxHolding;

    event FeeCollected(address indexed from, uint256 amount);
    error ExceedsMaxHolding(uint256 balance, uint256 maximum);

    constructor(address fund) ERC20("Class Point", "CLP") Ownable(msg.sender) {
        classFund = fund;
        _mint(msg.sender, 1_000_000 * 10 ** decimals());
        maxHolding = totalSupply() * 200 / 10_000;
    }

    function _update(address from, address to, uint256 value) internal override {
        if (from != address(0) && to != address(0) && from != owner()) {
            uint256 fee = value * feeBps / 10_000;
            if (fee > 0) {
                super._update(from, classFund, fee);
                emit FeeCollected(from, fee);
                value -= fee;
            }
        }
        super._update(from, to, value);
        if (to != address(0) && to != classFund && to != owner()) {
            uint256 balance = balanceOf(to);
            if (balance > maxHolding) revert ExceedsMaxHolding(balance, maxHolding);
        }
    }
}
