const ws = new WebSocket(String(process.env.REACT_APP_WS_HOST));

ws.onopen = () => {
    console.log("WS connection sucess");
};

export const send = (data) => {
    const isValid = send_data_protocol(data)
    if (isValid) {
      ws.send(data)
    }
}

function send_data_protocol(data) :boolean{
  let result = false
  switch(data.type){
    case 'CLIENT_NAME_SET':
      if (Object.keys(data).toString === ['type', 'userName'].toString
        && typeof(data.userName) === "string") {
        result = true
      } else {
        invalid_key_found()
      }
      break
    case 'CLIENT_ROOM_CREATE':
      if (Object.keys(data).toString === ['type', 'roomName'].toString
        && typeof(data.roomName) === "string") {
        result = true
      } else {
        invalid_key_found()
      }
      break
    case 'CLIENT_ROOM_GET':
      if (Object.keys(data).toString === ['type'].toString) {
        result = true
      }
      break
    case 'CLIENT_ROOM_JOIN':
      if (Object.keys(data).toString === ['type', 'roomID'].toString
        && typeof(data.roomID) === "number") {
        result = true
      } else {
        invalid_key_found()
      }
      break
    case 'CLIENT_ROOM_EXIT':
      if (Object.keys(data).toString === ['type'].toString) {
        result = true
      } else {
        invalid_key_found()
      }
    break
    case 'CLIENT_CHAT_SEND':
      if (Object.keys(data).toString === ['type', 'message'].toString
        && typeof(data.message) === "string") {
        result = true
      } else {
        invalid_key_found()
      }
      break
    default:
      console.log('no matching type key word')
    }
  return result
}

const invalid_key_found = () => {
  console.log("Invalid key is in data")
}

export default ws;