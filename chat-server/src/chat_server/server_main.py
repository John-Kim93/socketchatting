import asyncio
import websockets
from dataclasses import dataclass
from .sess_manager import SessManager


@dataclass
class ServerMain:
    host: str = "localhost"
    port: int = 8100
    sess_mgr: SessManager = SessManager()

    def start(self):
        try:
            asyncio.run(self.listen())
        except KeyboardInterrupt:
            pass

    async def listen(self):
        server = await websockets.serve(
            self.on_connect, self.host, self.port)
        print("Listening.....")
        await server.serve_forever()

    async def on_connect(self, websocket):
        await self.sess_mgr.generate(websocket)
