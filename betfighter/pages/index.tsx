import { ConnectWallet, Web3Button, ThirdwebProvider, metamaskWallet, useWallet, walletConnect, coinbaseWallet } from "@thirdweb-dev/react";
import type { NextPage } from "next";
import styles from "../styles/Home.module.css";
import { getData } from '/';
import axios from 'axios';
import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import { useContract, useContractWrite, useContractRead, useContractEvents } from "@thirdweb-dev/react";
import { winnerResponse } from "./api/openBet";
import Image from 'next/image';
import { ethers } from "ethers";
import parseWinnerData from "../pages/setWinner";
import ConnectWalletButton from "./ConnectWalletButton";
import SetPlayer1Button from "./SetPlayer1Button";
import SetPlayer2Button from "./SetPlayer2Button";
import SetPlayer1Bet from "./SetPlayer1Bet";
import SetPlayer2Bet from "./SetPlayer2Bet";
import SetResult from "./setResult";
import SetResultsBeta from "./setResultsBeta";




interface WinnerData {
  winner: string;  // assuming the 'winner' field is a string; change as needed
}

const Home: NextPage = () => {


  // While isLoading is true, contract is undefined.
  const { contract, isLoading } = useContract("0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee");
  // Now you can use the contract in the rest of the component
  console.log(contract)

//Set Players
  const [_player1, setPlayer1] = useState("");
  const [_player2, setPlayer2] = useState("");
  
//Player 1 event listeners
const { data: player1EventData } = useContractEvents(contract, "Player1Set", {
  fromBlock: "latest - 1000",
  toBlock: "latest",
})
const { data: player1Data } = useContractRead(contract, "player1", []);
const { data: player1BetData, isLoading: player1BetLoading } = useContractRead(contract, "player1Bet", []);
// Convert player2BetData to a string for rendering
const player1BetDataString = player1BetData && ethers.utils.formatEther(player1BetData.toString());



 // Update the event arguments if needed
const { data: player1Won } = useContractEvents(contract, "PlayerWon")

  useEffect(() => {
    if (player1EventData) {
      console.log("Player 1 event data:", player1EventData);
    }
    if (player1Data) {
      console.log("Player 1 data:", player1Data);
    }
  }, [player1EventData, player1Data, player1BetData]);

//Player2 event listeners

const { data: player2EventData } = useContractEvents(contract, "Player2Set", {
  fromBlock: "latest - 1000",
  toBlock: "latest",
});
const { data: player2Data } = useContractRead(contract, "player2", []); // Update the event arguments if needed
const { data: player2BetData, isLoading: player2BetLoading } = useContractRead(contract, "player2Bet", []);
// Convert player2BetData to a string for rendering
const player2BetDataString = player2BetData && ethers.utils.formatEther(player2BetData.toString());


useEffect(() => {
  if (player2EventData) {
    console.log("Player 2 event data:", player2EventData);
  }
  if (player2Data) {
    console.log("Player 2 data:", player2Data);
  }
}, [player2EventData, player2Data]);




// You can get a specific event
  const { data: Winner } = useContractEvents(contract, "PlayerWon")
  // All events
  const { data: allEvents } = useContractEvents(contract)
  // By default, you set up a listener for all events, but you can disable it
  const { data: eventWithoutListener } = useContractEvents(contract, undefined, { subscribe: false })
  
//MoneyPOT event listener
const { data: potData, isLoading: isPotLoading } = useContractRead(contract, "pot", [/* args here if needed */]);
// Convert potData to a string for rendering
const potDataString = potData && ethers.utils.formatEther(potData.toString());

  

    //Place a bet component
    const { mutateAsync: placeBet } = useContractWrite(contract, "placeBet")

    const handlePlaceBet = async () => {
      if (isLoading) {
        return;
      }

      try {
        const result = await contract.call("placeBet", [wallet?.address || ""]);
        console.log(result);
        console.info("Bet placed successfully");
      } catch (err) {
      console.error("Failed to place bet:", err);
     }
        
    }

  //const [id, setID] = useState("");
  const [player1, player1Bet] = useState("");
  const [player2, player2Bet] = useState("");
  //const [playerId, setPlayerId] = useState("")
  //const [placeBet, setPlaceBet] = useState("")
  
 
//Components for connect Flask/NExt
  const [data, setData] = useState({});

  useEffect(() => {
    winnerResponse().then((test:any) => {
      console.log("a response test", test)
      setData(test)
    })
    .catch((error) => {
      console.error("Failed to fetch winner from backend", error);
    });
  }, []);



  //Sending the JSON to Smart Contract
  const { mutateAsync: myFunctionAsync } = useContractWrite(contract, "setResult");
  const tx = async () => await myFunctionAsync(["left", "right"]) // Call the function

  const setWinner = async (data: any) => {
  try {
    // Parse the winner data
    const { _player1Won } = parseWinnerData(data);

    // Determine the winner
    const winner = _player1Won ? 1 : 2;

    // Call the setResult function with the winner
    await myFunctionAsync([winner]);
  } catch (error) {
    console.error("Failed to set the winner:", error);
  }
}





  

  // Declare a new state for the selected game
const [selectedGame, setSelectedGame] = useState("MK11");





  

  return (
    <div className={styles.container}>
      <div className={styles.backgroundVideo}>
        <video autoPlay muted loop className={styles.backgroundVideo}>
  <source src="/arcadeVideo.mp4" type="video/mp4" />
</video>
      </div>
      
      <div className={styles.main}>
        
        <h1 className={styles.title}>
          Welcome to <a href="/">BETfighter</a>!
        </h1>

        <p className={styles.description}>
          The worlds first computer vision betting app for AAA fighting games.
        
        </p>

      
        

       
        
        <a href="" className={styles.card}>

          


       <h2>Select Your Game</h2>
    
      <p>
        <input
          type="text"
          name="Choose Game"
          value={"MK11", "SF", "Tekken"}
          onChange={(e) => setPlayer1(e.target.value)}
        />
  We currently only support MK11.  Tekken and Street Fighter Coming S.  Each game has different ways of interacting with our program so select the exact game.

    </p>
      </a>
       
        <div className={styles.grid}>
          <a className={styles.card}>
   
    <div>
      
      <ThirdwebProvider supportedWallets={[ metamaskWallet(), coinbaseWallet()]}>
      <ConnectWallet theme="light" />
      </ThirdwebProvider>

    
    
      <h1>Set Player 1 (Left)</h1>
      <SetPlayer1Button />

    {/* Render the event data if available */}
        {player1EventData && player1EventData.args && player1EventData.args.Player1Set && (
          <p>Player 1: {player1EventData.args.Player1Set}</p>
          
        )}
        {player1 && (
          <p>Player 1: {player1}</p>
          
        )}
        {/* Render player1Bet if available and not loading */}
      

     
        

        

        
        
              

    
    </div>
      <SetPlayer1Bet contract={contract} player1Bet={player1Bet} />

      { player1BetLoading ? (
        <p>Loading player 1 bet amount...</p>
      ) : (
        <p>Player 1 bet amount: {player1BetDataString} ETH</p>
      )}

    
    
           
          </a>
          {/* Render player1Bet if available and not loading */}

          
          <div className={styles.card}>
            <h2>Versus</h2>
             <div>
            <Image src="/retroArcade.png" alt="Retro Arcade Cabinet" width={500} height={500} />
            </div>
            <div>
              { isPotLoading ? (
        <p>Loading pot amount...</p>
      ) : (
        <p>Pot amount: {potDataString} ETH</p>
      )}
            </div>
           
          </div>
          

          <a className={styles.card}>
            <ThirdwebProvider supportedWallets={[ metamaskWallet(), coinbaseWallet()]}>
      <ConnectWallet theme="light" />
    </ThirdwebProvider>
            <h1>Set Player 2 (Right)</h1>
                  <SetPlayer2Button contract={contract} player2={player2} setPlayer2={setPlayer2}/>
            {player1 && (
          <p>Player 1: {player1}</p>
        )}

        
         

         

            
    <div>
      <SetPlayer2Bet contract={contract} player2Bet={player2Bet} />

        { player2BetLoading ? (
        <p>Loading player 2 bet amount...</p>
      ) : (
        <p>Player 2 bet amount: {player2BetDataString} ETH</p>
      )}
    </div>
            
          </a>
          

        </div>
    
        
     <div>
      {data ? (
  <>
    <h1>WINNER:</h1>
     <pre>{JSON.stringify(data, null, 2)}</pre>
    <Web3Button
    contractAddress="0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee"
    action={(contract) => {
      console.log("number data", data); // log the data object
      if (data) {  // check if data is not null
        const winnerNumber = Number(data);
        console.log("data")
        if (!isNaN(winnerNumber)) {
          contract.call("setResult", [winnerNumber]);  // pass data.winner as a number
        } else {
          console.error("data.winner cannot be converted to a number:", data);
        }
      }
    }}
  >
    setResult
  </Web3Button>
  </>
) : (
  <p>Loading winner data...</p>
)}

<div>
  <SetResult contractAddress="0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee" winner={Number(data.winner)} />

      

 
        
    </div>

    <div> {
  data && data ? (
    <p> {data.winner}</p>
  ) : (
    <p>Loading winner data...</p>
  )
}</div>


  
    <Web3Button
      contractAddress="0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee"
      action={(contract) => {
        contract.call("cancelGame", [])
      }}
    >
      cancelGame
    </Web3Button>

        

      </div>   
      </div>
      
    </div>

    
    
    
  );
 
  
};

const App = () => {
  return (
    <ThirdwebProvider 
    activeChain="goerli"
    clientId= "6fd2705ab9b6ff896b2f658d2c183913">
      <Home />
    </ThirdwebProvider>
  );
};


export default Home;
