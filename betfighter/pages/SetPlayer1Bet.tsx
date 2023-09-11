import React, { useState, useEffect } from "react";
import { useContractWrite, useContract, useContractRead, Web3Button } from "@thirdweb-dev/react";
import { ethers } from "ethers";

const SetPlayer1Bet: React.FC = () => {
const { contract } = useContract("0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee");
const { mutateAsync: placeBet, isLoading } = useContractWrite(contract, "placeBet");
const { data: player1Bet, isLoading: isReadingBet } = useContractRead(contract, "player1Bet", []);
const [betValue, setBetValue] = useState("");
  console.log("betvalue", betValue);

  useEffect(() => {
    console.log("Player1's Bet: ", player1Bet);
  }, [player1Bet]);

  const handlePlaceBet = async () => {
    if (isLoading) {
      return;
    }

    // Validate the input value
    if (!betValue || Number(betValue) < 0.01) {
      console.error("Invalid bet amount");
      return;
    }

    try {
      const parsedBetValue = ethers.utils.parseEther(betValue); // Convert to valid BigNumber string
      console.log("Parsed bet value:", parsedBetValue);
      console.log("parsedBetValue", parsedBetValue)
      const result = await placeBet({ args:[], overrides: {value: parsedBetValue} });
      console.log(result);
      console.info("Bet placed successfully");
      setBetValue(""); // Reset the input field
    } catch (err) {
      console.error("Failed to place bet:", err);
    }
  };

  return (
    <div>
      <h2>Player 1 (Left Side) place your bet here &rarr;</h2>
      <input type="text" value={betValue} onChange={(e) => setBetValue(e.target.value)} />
      <button onClick={handlePlaceBet} disabled={isLoading}>
        Place Bet
      </button>

      <Web3Button
      contractAddress="0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee"
      action={(contract) => {
        contract.call("placeBet", [])
      }}
    >
      placeBet
    </Web3Button>
    </div>
  );
};

export default SetPlayer1Bet;
