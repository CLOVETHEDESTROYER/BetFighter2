// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

import "@thirdweb-dev/contracts/extension/ContractMetadata.sol";
import "@thirdweb-dev/contracts/extension/Permissions.sol";

contract BetFighter2 is ContractMetadata {
    address public deployer;
    address payable public owner;
    address payable public player1;
    address payable public player2;
    uint256 public player1Bet;
    uint256 public player2Bet;
    uint public pot;
    mapping(address => uint) public totalBets;
    uint public ownerFee;

    event PlayerWon(address winner, uint payout);
    event Player1Set(address player);
    event Player2Set(address player);
    event GameCancelled(address player);

    constructor() {
        owner = payable(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier onlyOwnerOrWinner(uint _winner) {
        address payable winner = _winner == 1 ? player1 : player2;
        require(
            msg.sender == owner || msg.sender == winner,
            "Only owner or the winner can call this function"
        );
        _;
    }

    function setPlayer1(address payable _player1) public {
        require(_player1 != address(0), "Invalid address");
        player1 = _player1;
        player1Bet = 0;
        emit Player1Set(_player1);
    }

    function setPlayer2(address payable _player2) public {
        require(_player2 != address(0), "Invalid address");
        player2 = _player2;
        player2Bet = 0;
        emit Player2Set(_player2);
    }

    function placeBet() external payable {
        require(
            msg.sender == player1 || msg.sender == player2,
            "Only registered players can place bets"
        );
        require(msg.value >= 0.01 ether, "Minimum bet is 0.01 ether");

        if (msg.sender == player1) {
            require(player1Bet == 0, "Player1 already placed a bet");
            require(
                player2Bet == 0 || msg.value == player2Bet,
                "Bets must be equal"
            );
            player1Bet = msg.value;
        } else if (msg.sender == player2) {
            require(player2Bet == 0, "Player2 already placed a bet");
            require(
                player1Bet == 0 || msg.value == player1Bet,
                "Bets must be equal"
            );
            player2Bet = msg.value;
        }

        pot += msg.value;
    }

    function setResult(uint _winner) public onlyOwnerOrWinner(_winner) {
        require(_winner == 1 || _winner == 2, "Winner must be either 1 or 2");
        require(player1Bet == player2Bet, "Bets must be equal");

        address payable winner = _winner == 1 ? player1 : player2;

        uint payout = (pot * 95) / 100; // Winner gets 95%
        ownerFee = pot - payout; // Owner gets 5%
        // Resetting the state before transferring
        pot = 0;
        player1Bet = 0;
        player2Bet = 0;

        // Transferring the amounts
        (bool success, ) = winner.call{value: payout}("");
        require(success, "Transfer to winner failed");

        (success, ) = owner.call{value: ownerFee}("");
        require(success, "Transfer to owner failed");

        emit PlayerWon(winner, payout);
    }

    function cancelGame() public {
        require(
            msg.sender == player1 || msg.sender == player2,
            "Only a player can cancel the game"
        );

        if (msg.sender == player1 && player1Bet > 0) {
            uint bet = player1Bet;
            player1Bet = 0;
            pot -= bet;
            (bool success, ) = player1.call{value: bet}("");
            require(success, "Transfer to player1 failed");
        } else if (msg.sender == player2 && player2Bet > 0) {
            uint bet = player2Bet;
            player2Bet = 0;
            pot -= bet;
            (bool success, ) = player2.call{value: bet}("");
            require(success, "Transfer to player2 failed");
        }

        emit GameCancelled(msg.sender);
    }

    function playAgain() public {
        pot = 0;
        ownerFee = 0;
        player1Bet = 0;
        player2Bet = 0;
    }

    function _canSetContractURI()
        internal
        view
        virtual
        override
        returns (bool)
    {
        return msg.sender == deployer;
    }
}
