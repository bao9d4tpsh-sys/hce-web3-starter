// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TimeLockVault {
    address public immutable owner;
    uint256 public immutable unlockTime;

    event Deposited(address indexed from, uint256 amount);
    event Withdrawn(address indexed to, uint256 amount);

    error NotOwner();
    error StillLocked(uint256 unlockAt, uint256 currentTime);
    error NothingToWithdraw();
    error ZeroAmount();
    error TransferFailed();

    constructor(uint256 lockDurationSeconds) {
        owner = msg.sender;
        unlockTime = block.timestamp + lockDurationSeconds;
    }

    function deposit() external payable {
        if (msg.value == 0) revert ZeroAmount();
        emit Deposited(msg.sender, msg.value);
    }

    function withdraw() external {
        if (msg.sender != owner) revert NotOwner();
        if (block.timestamp < unlockTime) revert StillLocked(unlockTime, block.timestamp);
        uint256 amount = address(this).balance;
        if (amount == 0) revert NothingToWithdraw();
        emit Withdrawn(owner, amount);
        (bool ok, ) = payable(owner).call{value: amount}("");
        if (!ok) revert TransferFailed();
    }
}

