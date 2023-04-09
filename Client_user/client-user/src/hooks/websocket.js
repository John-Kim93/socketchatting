const websocket = new WebSocket(String(process.env.REACT_APP_WS_HOST));

export default websocket

export const useWebsocket = () => {
  websocket.onopen = () => {
    console.log("WS Connexion start");
  };
  
  websocket.onclose = () => {
    console.log("WS Connexion closed");
  };

  websocket.onmessage = () => {
    console.log("Ready to listen messages from server")
  }

  return null;
}

export const send = (data) => {
  const isValid = send_data_protocol(data)
  if (isValid) {
    websocket.send(JSON.stringify(data))
    return true
  }
  return false
}

function send_data_protocol(data){
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
      if (Object.keys(data).toString === ['type', 'roomId'].toString
        && typeof(data.roomId) === "number") {
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