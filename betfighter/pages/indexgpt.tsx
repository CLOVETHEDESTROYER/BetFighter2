import React, { useState, useEffect } from "react";
import { ThirdwebSDK, ThirdwebProvider, metamaskWallet } from "@thirdweb-dev/react";
import { getData } from "/";
import axios from "axios";
import Image from "next/image";
import parseWinnerData from "../pages/setWinner";

const Home = () => {
  const sdk = new ThirdwebSDK("goerli");

  // Connect Wallet
  const { wallet, status } = useWallet(sdk);

  // While isLoading is true, contract is undefined.
  const { contract, isLoading, error } = useContract("0x54446a5Ed73AFD2F8b64F9b0BdA4dd156b619233");

  const [player1, setPlayer1] = useState("");
  const [player2, setPlayer2] = useState("");
  const [bets, setBets] = useState({});

  const handleSetPlayer1 = async () => {
    if (isLoading) {
      return;
    }

    try {
      const result = await contract.call("setPlayer1", [wallet?.address || ""]);
      setPlayer1(wallet?.address || "");
    } catch (err) {
      console.error("Failed to set Player 1:", err);
    }
  };

  const handleSetPlayer2 = async () => {
    if (isLoading) {
      return;
    }

    try {
      const result = await contract.call("setPlayer2", [wallet?.address || ""]);
      setPlayer2(wallet?.address || "");
    } catch (err) {
      console.error("Failed to set Player 2:", err);
    }
  };

  const handlePlaceBet = async () => {
    if (isLoading) {
      return;
    }

    try {
      const result = await contract.call("placeBet", [wallet?.address || ""]);
      setBets(bets || {});
      bets[wallet?.address] += 1;
    } catch (err) {
      console.error("Failed to place bet:", err);
    }
  };

  const getWinner = async () => {
    const winner = await contract.call("getWinner");
    return winner;
  };

  const payOut = async () => {
    await contract.call("payOut");
  };

  useEffect(() => {
    getData().then((data) => {
      setWinner(data.winner);
    });
  }, []);

  return (
    <div>
      <h1>BETfighter</h1>
      <p>The worlds first computer vision betting app for AAA fighting games.</p>
      <div>
        <h2>Select Your Game</h2>
        <select name="Choose Game" value={player1} onChange={(e) => setPlayer1(e.target.value)}>
          <option value="MK11">Mortal Kombat 11</option>
          <option value="SF">Street Fighter</option>
          <option value="Tekken">Tekken</option>
        </select>
      </div>
      <div>
        <h2>Set Player 1</h2>
        <button onClick={handleSetPlayer1}>Set Player 1</button>
      </div>
      <div>
        <h2>Set Player 2</h2>
        <button onClick={handleSetPlayer2}>Set Player 2</button>
      </div>
      <div>
        <h2>Place Bet</h2>
        <input type="number" name="Bet" value={bets[wallet?.address] || "0"} onChange={(e) => setBets(bets || {}, { [wallet?.address]: e.target.value })} />
      </div>
      <div>
        <h2>Winner</h2>
        {getWinner() ? (
          <p>{getWinner()}</p>
                  ) : (
          <p>No winner yet.</p>
        )}
      </div>
      <div>
        <h2>Payout</h2>
        <button onClick={payOut}>Payout</button>
      </div>
    </div>
  );
};

export default Home;