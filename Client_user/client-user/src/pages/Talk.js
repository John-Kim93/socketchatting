import { useEffect, useRef, useState } from "react"
import style from "./Talk.module.css"

export default function Talk() {
  const [sendCount, setsendCount] = useState(0)
  const [typingText, setTypingText] = useState("")
  const [printedText, setPrintedText] = useState([])

  const user = sessionStorage.getItem("userName")
  const wsRef = useRef(null);

  useEffect(() => {
    wsRef.current = new WebSocket("ws://localhost:8100")

    wsRef.current.onopen = () => {
      wsRef.current.send(user)
      console.log("web socket 연결!!!")
    };

    wsRef.current.onmessage = ({ data }) => {
      const msg = JSON.parse(data)
      setPrintedText(prevPrintedText =>
        [...prevPrintedText, `${msg.nickname}: ${msg.chat}`])
    };

    return () => {
      console.log("web socket 연결 끝!!!")
      wsRef.current.close()
    };
  }, [user])


  const sendMessage = () => {
    if (typingText) {
      setsendCount(sendCount + 1)
      setTypingText("")
      wsRef.current.send(typingText)
    }
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
          sendMessage();
        }
        break
      default :
        break
    }
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
      <button onClick={sendMessage}>보내기</button>
      <p>보낸 메시지 횟수 : {sendCount}번</p>
      {printedText.map((message, idx) => <div className="message" key={idx}>{message}</div>)}
    </div>
  )
}