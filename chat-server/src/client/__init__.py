import asyncio
from .client_main import ClientMain


def main():
    try:
        asyncio.run(ClientMain().start())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
