// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// CANH BAO: Tep nay co loi co y. Khong dung lai trong bai lam.
contract VaultBuggy {
    address public owner;
    uint256 public unlockTime;
    uint256 private emergencyPin;

    constructor(uint256 lockSeconds, uint256 pin) {
        owner = msg.sender;
        unlockTime = block.timestamp + lockSeconds;
        emergencyPin = pin;
    }

    function deposit() external payable {}

    function withdraw() external {
        require(block.timestamp <= unlockTime, "Chua den han rut tien");
        payable(msg.sender).transfer(address(this).balance);
    }
}

