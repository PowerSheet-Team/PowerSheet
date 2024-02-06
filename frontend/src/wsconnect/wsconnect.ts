import { io } from "socket.io-client";

const makeSocket = () => {
  const URL = "http://localhost:5000";
  const socket = io(URL);
  return socket;
};

export default makeSocket;
