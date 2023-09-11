import { useContract, useContractWrite, Web3Button } from "@thirdweb-dev/react";
import { useEffect, useState } from "react";

const SetPlayer1Button = () => {
  const { contract } = useContract("0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee");
  const { mutateAsync: setPlayer1, isLoading } = useContractWrite(contract, "setPlayer1");
  const [player1Address, setPlayer1Address] = useState("");

  useEffect(() => {
    const getWalletAddress = async () => {
      const provider = await window.ethereum;
      if (provider) {
        const accounts = await provider.request({ method: "eth_accounts" });
        if (accounts.length > 0) {
          setPlayer1Address(accounts[0]);
        }
      }
    };

    getWalletAddress();
  }, []);

  const handleSetPlayer1 = async () => {
    try {
      const data = await setPlayer1({ args: [player1Address] });
      console.info("Contract call success:", data);
    } catch (err) {
      console.error("Contract call failure:", err);
    }
  };

  return (
    <div>
      <input type="text" value={player1Address} onChange={(e) => setPlayer1Address(e.target.value)} disabled />
      <button onClick={handleSetPlayer1} disabled={!player1Address || isLoading}>
        Set Player 1
      </button>
      <Web3Button
      contractAddress="0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee"
      action={ async (contract) => {
        await contract.call("setPlayer1", [player1Address])
      }}
    >
      setPlayer1
    </Web3Button>
    <h2>Player 1 Data</h2>
      {isLoading ? (
        <p>Loading player1 data...</p>
      ) : (
        <p>Player 1: {player1Address}</p>
      )}
    </div>
  );
};

export default SetPlayer1Button;
