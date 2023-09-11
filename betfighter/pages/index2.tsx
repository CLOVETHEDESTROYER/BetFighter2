import { ConnectWallet, Web3Button } from "@thirdweb-dev/react";
import type { NextPage } from "next";
import styles from "../styles/Home.module.css";
import { getData } from '/';
import axios from 'axios';
import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import { useContract, useContractWrite, useContractRead } from "@thirdweb-dev/react";
import { winnerResponse } from "./api/openBet";




const Home: NextPage = () => {

  // While isLoading is true, contract is undefined.
  const { contract, isLoading, error } = useContract("0x665ad964552493601c5EC81Bc12389a68D00f98A");
  // Now you can use the contract in the rest of the component
  console.log(contract)

    //Place a bet component
    const { mutateAsync: placeBet } = useContractWrite(contract, "placeBet")

    const call = async () => {
      try {
        const contractData = await placeBet([ _player1 ]);
        console.info("contract call successs", contractData);
      } catch (err) {
        console.error("contract call failure", err);
      }
    }

  //const [id, setID] = useState("");
  const [_player1, setPlayer] = useState("");
  const [player1, player1Bet] = useState("");
  const [player2, player2Bet] = useState("");
  //const [playerId, setPlayerId] = useState("")
  //const [placeBet, setPlaceBet] = useState("")
  
//Components for connect Flask/NExt
  const [data, setData] = useState({})

  useEffect(() => {
    winnerResponse().then((test:any) => {
      console.log("a response test", test)
      setData(test)
    })
  }, [])
  

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <a href="/">BETfighter</a>!
        </h1>

        <p className={styles.description}>
          The worlds first computer vision betting app for AAA fighting games.
        
        </p>

        <div className={styles.connect}>
          <ConnectWallet accentColor="#27cc53" />
        </div>

        <div className={styles.grid}>
          <a className={styles.card}>
            <h2>Place your Bet Here &rarr;</h2>
            <Web3Button
      contractAddress="0x665ad964552493601c5EC81Bc12389a68D00f98A"
      action={(contract) => {
        contract.call("placeBet", _player1)
      }}
    >
      placeBet
    </Web3Button>
            <p>
              This is where you will place your initial Bet.
              <input
                type="number"
                name="player1"
                value={_player1}
                onChange={(e) => setPlayer(e.target.value)}
              />
            </p>
          </a>

          <a href="" className={styles.card}>


            <h2>Choose Your Game &rarr;</h2>
            <Web3Button
      contractAddress="0x665ad964552493601c5EC81Bc12389a68D00f98A"
      action={(contract) => {
        contract.call("setPlayers", _player1, _player2)
      }}
    >
      setPlayers
    </Web3Button>
            <p>
            <input
                type="text"
                name="player2"
                value={player2}
                onChange={(e) => setPlayer(e.target.value)}
              />
              We currently only support MK11.  Tekken and Street Fighter Coming S
            </p>
          </a>

          <a
            href="https://thirdweb.com/dashboard"
            className={styles.card}
          >
            <h2>Fighter 2 &rarr;</h2>
            <p>
See if your opponent is ready for battle.            </p>
          </a>
        </div>
        <div>
        {data ? (
          <>
            <h1>Data from Flask backend:</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </>
        ) : (
          <p>Loading data...</p>
        )}
      </div>
      </main>
    </div>
  );
 
  
};


export default Home;
