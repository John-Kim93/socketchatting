import { useState } from "react"
import { useNavigate } from "react-router-dom";
import style from "./Home.module.css"
import websocket, { send } from '../hooks/websocket.js';
import { useEffect } from "react";

export default function Home() {
  let navigate = useNavigate();

  const [userName, setUserName] = useState("")
  const [warning, setWarning] = useState(false)

  useEffect(() => {
    websocket.onmessage = ({ data }) => {
      const res = JSON.parse(data)
      if (res?.status) {
        if (res.type === "SERVER_NAME_SET") {
          navigate("/lobby")
        }
      }
    }
  }, [navigate])
  

  const enterName = () => {
    const name = userName.trim() 
    if (name) {
      const res = send({
        type: "CLIENT_NAME_SET",
        userName: name
      })
      if (res) {
        sessionStorage.setItem('userName', name)
      } else {
        console.log("이름 설정 실패!")
      }
    } else {
      setWarning(true)
    }
  }
  
  return(
    <>
      <div className={style.container}> 
        <input
          name="userName"
          value={userName}
          onChange={(e) => {
            setUserName(e.target.value)
            setWarning(false)
          }}
          placeholder="이름을 입력하세요."
          maxLength={10}
        />
        <button onClick={enterName}>Enter</button>
        {warning && <p>이름을 입력하세요!</p>}
      </div>
    </>
  )
}