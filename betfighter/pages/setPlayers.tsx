import { useContract, useContractWrite } from "@thirdweb-dev/react";
import type { NextPage } from "next";
import styles from "../styles/Home.module.css";

const Player: NextPage = () => {
  const { contract } = useContract("0x4FF933d0f791fFB0f30Bb5120aE62DaC5deeBEee");
  const { mutateAsync: setPlayers, isLoading } = useContractWrite(contract, "setPlayers")

  const call = async () => {
    try {
      const data = await setPlayers([ _player1, _player2 ]);
      console.info("contract call successs", data);
    } catch (err) {
      console.error("contract call failure", err);
    }
  }
}

export default function Player;