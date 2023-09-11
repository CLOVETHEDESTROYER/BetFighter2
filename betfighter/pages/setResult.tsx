import { useContract, useContractWrite } from "@thirdweb-dev/react";
import React from "react";


interface SetResultProps {
  contractAddress: string;
  winner: number;
}

const SetResult: React.FC<SetResultProps> = ({ contractAddress, winner }) => {
  const { contract } = useContract(contractAddress);
  const { mutateAsync: setResult, isLoading } = useContractWrite(contract, "setResult");

  const call = async () => {
    try {
      const data = await setResult({ args: [winner] });
      console.info("contract call success", data);
    } catch (err) {
      console.error("contract call failure", err);
    }
  };

  return (
    <div>
      <button onClick={call} disabled={isLoading}>
        Set Result
      </button>
    </div>
  );
};

export default SetResult;
