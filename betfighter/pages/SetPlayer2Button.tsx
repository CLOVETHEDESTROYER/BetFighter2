import { Web3Button, useContract, useContractWrite, ConnectWallet } from "@thirdweb-dev/react";
import { useEffect, useState } from "react";

const SetPlayer2Button = () => {
  const { contract } = useContract("0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee");
  const { mutateAsync: setPlayer2, isLoading } = useContractWrite(contract, "setPlayer2");
  const [player2Address, setPlayer2Address] = useState("");

 useEffect(() => {
    const getWalletAddress = async () => {
      const provider = await window.ethereum;
      if (provider) {
        const accounts = await provider.request({ method: "eth_accounts" });
        if (accounts.length > 0) {
          setPlayer2Address(accounts[0]);
        }
      }
    };

    getWalletAddress();
  }, []);

  const handleSetPlayer2 = async () => {
    try {
      const data = await setPlayer2({ args: [player2Address] });
      console.info("Contract call success", data);
    } catch (err) {
      console.error("Contract call failure", err);
    }
  };

  return (
    <div>
      <ConnectWallet theme="light" />
      <h2>Player 2 Wallet Address</h2>
      <input type="text" value={player2Address} onChange={(e) => setPlayer2Address(e.target.value)} disabled />
      <button onClick={handleSetPlayer2} disabled={isLoading}>
        Set Player 2
      </button>
      <Web3Button
        contractAddress="0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee"
        action={async (contract) => {
          await contract.call("setPlayer2", [player2Address]);
        }}
      >
        setPlayer2
      </Web3Button>
      <h2>Player 2 Data</h2>
      {isLoading ? (
        <p>Loading player2 data...</p>
      ) : (
        <p>Player 2: {player2Address}</p>
      )}
    </div>
  );
};

export default SetPlayer2Button;


