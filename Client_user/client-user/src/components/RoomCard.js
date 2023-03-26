import style from "./RoomCard.module.css"

export default function RoomCard({ uid, title, host }) {
  return (
    <div className={style.hover_wrap}>
      <div className={style.effect}>
        <figure className={style.front}>
          {/* <img src="#" alt="게임 타입"/> */}
          <figcaption>
            <h3>{uid}. {title}</h3>
            <p>방장 : {host}</p>
          </figcaption>
        </figure>
        <figure className={style.back}>
          <figcaption>
            <h3>현재 인원 (n명)</h3>
            <p>유저유저유저</p>
          </figcaption>
        </figure>
      </div>
    </div>
  )
}