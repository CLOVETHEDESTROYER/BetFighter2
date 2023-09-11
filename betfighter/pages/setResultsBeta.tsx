import { Web3Button, useContract, useContractWrite } from "@thirdweb-dev/react";
import React, { useEffect, useState } from "react";
import { winnerResponse } from "./api/openBet";

interface SetResultProps {
  contractAddress: string;
}

const SetResultsBeta: React.FC<SetResultProps> = ({ contractAddress }) => {
  const { contract } = useContract(contractAddress);
  const { mutateAsync: setResult, isLoading } = useContractWrite(contract, "setResult");
  const [winner, setWinner] = useState<number | null>(null);

  useEffect(() => {
    // Fetch the winner from the backend
    winnerResponse()
      .then((data) => {
        // Assuming the winner data is in the format: { winner: 1 } or { winner: 2 }
        const parsedWinner = Number(data) || null; // Convert the winner value to a number
        setWinner(parsedWinner);
      })
      .catch((error) => {
        console.error("Failed to fetch winner from backend:", error);
      });
  }, []);

  const handleSetResult = async () => {
    if (isLoading || winner === null) {
      return;
    }

    try {
      const result = await setResult({ args: [winner] });
      console.info("Contract call success", result);
    } catch (err) {
      console.error("Failed to set result:", err);
    }
  };

  return (
    <div>
      {winner !== null ? (
        <div>
          <h1>Winner: {winner}</h1>
          <Web3Button
            contractAddress={contractAddress}
            action={async (contract) => {
              try {
                await contract.call("setResult", [winner]);
              } catch (error) {
                console.error("Failed to set result:", error);
              }
            }}
          >
            Set Result
          </Web3Button>

          
        </div>
      ) : (
        <p>Loading winner data...</p>
      )}
    </div>
  );
};

export default SetResultsBeta;
