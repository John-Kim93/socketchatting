import asyncio
import websockets
import json

SOCKETS: list = []


async def broadcast(data: str):
    await asyncio.gather(*[s.send(data) for s in SOCKETS])


async def echo(websocket):
    try:
        nickname = await websocket.recv()

        msg = dict(nickname=nickname, chat="님이 입장하셨습니다.")
        data = json.dumps(msg)
        await broadcast(data)

        SOCKETS.append(websocket)

        while chat := await websocket.recv():
            msg = dict(nickname=nickname, chat=chat)
            data = json.dumps(msg)
            await broadcast(data)

    except websockets.ConnectionClosedOK:
        SOCKETS.remove(websocket)

        msg = dict(nickname=nickname, chat="님이 퇴장하셨습니다.")
        data = json.dumps(msg)
        await broadcast(data)


async def main():
    async with websockets.serve(echo, "localhost", 8100):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
