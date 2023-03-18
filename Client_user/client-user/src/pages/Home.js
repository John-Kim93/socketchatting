import { useState } from "react"
import { useNavigate } from "react-router-dom";
import "./Home.css"

export default function Home() {
  let navigate = useNavigate();

  const [userName, setUserName] = useState("")
  const [waring, setWarning] = useState(false)
  const enterName = () => {
    if (userName) {
      sessionStorage.setItem('userName', userName)
      navigate("/talk")
    } else {
      setWarning(true)
    }
  }
  
  return(
    <>
      <div className="container"> 
        <input
          name="userName"
          value={userName}
          onChange={(e) => {
            setUserName(e.target.value)
            setWarning(false)
          }}
          placeholder="이름을 입력하세요."
        />
        <button onClick={enterName}>Enter</button>
        {waring && <p>이름을 입력하세요!</p>}
      </div>
    </>
  )
}