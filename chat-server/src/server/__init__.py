import asyncio
from .server_main import ServerMain


def main():
    try:
        asyncio.run(ServerMain().start())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
