const ws = new WebSocket(process.env.WS_HOST);

ws.onopen = () => {
    console.log("WS connection sucess");
};

export const send = (type, data) => {
    // ws.send(JSON.stringify({
    //     type,
    //     data:{
    //         ...data
    //     }
    // }));
    ws.send({
      type,
      data:{
        ...data
      }
    })
}

export default ws;