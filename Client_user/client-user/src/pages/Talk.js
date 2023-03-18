import { useState } from "react"
import "./Talk.css"

export default function Talk() {
  const [sendCount, setsendCount] = useState(0)
  const [typingText, setTypingText] = useState("")
  const [printedText, setPrintedText] = useState([])
  const user = sessionStorage.getItem("userName")
  const sendMessage = () => {
    if (typingText) {
      setsendCount(sendCount + 1)
      setPrintedText([...printedText, `${user} : ${typingText}`])
      setTypingText("")
    }
  }
  return(
    <div className="container">
      <textarea
        name="typingText"
        value={typingText}
        onChange={(e) => {setTypingText(e.target.value)}}
      />
      <button onClick={sendMessage}>보내기</button>
      <p>보낸 메시지 횟수 : {sendCount}번</p>
      {printedText.map((message, idx) => <div className="message" key={idx}>{message}</div>)}
    </div>
  )
}