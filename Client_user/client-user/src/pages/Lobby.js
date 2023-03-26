
import { useNavigate } from "react-router-dom";
import RoomCard from "../components/RoomCard";
import style from "./Lobby.module.css"

export default function Lobby() {
  let navigate = useNavigate();

  const roomList = [
    {
      roomID : 1,
      roomName : "1번방",
      host : "나는 방장!"
    },
    {
      roomID : 2,
      roomName : "2번방",
      host : "나는 방장!"
    },
    {
      roomID : 3,
      roomName : "3번방",
      host : "나는 방장!"
    },
    {
      roomID : 4,
      roomName : "4번방",
      host : "나는 방장!"
    },
    {
      roomID : 5,
      roomName : "5번방",
      host : "나는 방장!"
    },
  ]

  const enterRoom = (roomID) => {
    navigate(`/talk/${roomID}`)
  }
  
  return (
    <div className={style.container}>
      {roomList.map((room) => {
        return(
          <div onClick={()=>enterRoom(room.roomID)}>
            <RoomCard uid={room.roomID} title={room.roomName} host={room.host} />
          </div>
        )
      })}
    </div>
  )
}