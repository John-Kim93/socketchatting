var WebSocketServer = require('ws').Server;
var wss = new WebSocketServer( { port: 8100 } );

wss.on( 'connection', function(ws){
 console.log("connected");

 // 클라이언트가 전송한 메시지가 수신되면 클라이언트로 다시 전송한다.
 ws.on( 'message', function(msg){
  console.log("msg[" + msg + "]" );
  ws.send( msg );
  });
});