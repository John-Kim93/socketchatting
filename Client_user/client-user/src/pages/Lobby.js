
import { useNavigate } from "react-router-dom";
import RoomCard from "../components/RoomCard";
import style from "./Lobby.module.css"
import websocket, { send } from "../hooks/websocket";
import { useState } from "react";
import { useEffect } from "react";

export default function Lobby() {
  let navigate = useNavigate()

  const [roomList, setRoomList] = useState([]) 
  const [roomName, setRoomName] = useState("") 
  const [warning, setWarning] = useState("")

  
  useEffect(() => {
    send({
      type : "CLIENT_ROOM_GET",
    })
    websocket.onmessage = ({ data }) => {
      const res = JSON.parse(data)
      if (res?.status) {
        switch (res.type) {
          case "SERVER_ROOM_GET":
            setRoomList(res.roomList)
            break
          case "SERVER_ROOM_CREATE":
            navigate(`/talk/${res.roomId}`, {state: { roomID: res.roomId }})
            break
          case "SERVER_ROOM_JOIN":
            console.log('test', res)
            navigate(`/talk/${res.roomId}`, {state: { roomID: res.roomId }})
            break
          default:
            break
        }
      }
    }
  }, [navigate])

  const enterRoom = (roomID) => {
    send({
      type : "CLIENT_ROOM_JOIN",
      roomId  : roomID
    })
  }

  const createRoom = () => {
    const name = roomName.trim()
    if (name) {
      send({
        type : "CLIENT_ROOM_CREATE",
        roomName : name
      })
    } else {
      setWarning("방 제목을 입력하세요!!!")
    }
  }

  return (
    <>
      <input
        className={style.input}
        name="roomName"
        value={roomName}
        onChange={(e) => {
          setRoomName(e.target.value)
          setWarning("")
        }}
        placeholder="방 제목을 입력하세요."
        maxLength={30}></input>
      <button onClick={createRoom} className={style.button}>방 만들기</button>
      <div className={style.container}>
        <div className={style.warningMessage}>{warning}</div>
        {roomList.map((room) => {
          return(
            <div key={room.room_id} onClick={()=>enterRoom(room.room_id)}>
              <RoomCard uid={room.room_id} title={room.room_name} host={room.host} />
            </div>
          )
        })}
      </div>
    </>
  )
}