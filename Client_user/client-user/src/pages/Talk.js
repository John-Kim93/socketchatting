import { useState } from "react"
import style from "./Talk.module.css"
import websocket, { send } from "../hooks/websocket.js"
import { useEffect } from "react"
import { useNavigate } from "react-router-dom";


export default function Talk() {
  const [sendCount, setsendCount] = useState(0)
  const [typingText, setTypingText] = useState("")
  const [printedText, setPrintedText] = useState([])

  const navigate = useNavigate()

  useEffect(() => {
    websocket.onmessage = ({ data }) => {
      const msg = JSON.parse(data)
      if (msg.type === "BROAD_CHAT_SEND") {
        setPrintedText(prevPrintedText =>
          [...prevPrintedText, `${msg.nickName}: ${msg.message}`])
      } else if (msg.type === "SERVER_ROOM_EXIT" && msg.status) {
        navigate("/lobby")
      } else if (msg.type === "BROAD_ROOM_EXIT") {
        setPrintedText(prevPrintedText =>
          [...prevPrintedText, `${msg.nickName}님이 퇴장하셨습니다.`])
      }
    } 
  }, [navigate])

  const sendMessage = () => {
    send({
      type : "CLIENT_CHAT_SEND",
      message : typingText
    });
    setsendCount(sendCount + 1)
  }

  const handleChnage = (e) => {
    if (e.target.value.length > 128) return
    setTypingText(e.target.value)
  }

  const handleKeyDown = (e) => {
    switch (e.key) {
      case "Enter" :
        if (e.altKey) {
          if (e.target.value.length > 128) return
          setTypingText(`${typingText}\n`);
        } else {
          e.preventDefault();
          sendMessage()
        }
        break
      default :
        break
    }
  }

  const exitRoom = () => {
    send({
      type : "CLIENT_ROOM_EXIT",
    });
  }

  return (
    <div className={style.container}>
      <textarea
        name="typingText"
        value={typingText}
        onChange={handleChnage}
        onKeyDown={handleKeyDown}
        maxLength={128}
      />
      <button onClick={sendMessage} style={{"backgroundColor":"#6BBE92"}}>보내기</button>
      <button onClick={exitRoom} style={{"backgroundColor":"#ff0000"}}>방탈출</button>
      <p>보낸 메시지 횟수 : {sendCount}번</p>
      {printedText.map((message, idx) => <div className="message" key={idx}>{message}</div>)}
    </div>
  )
}