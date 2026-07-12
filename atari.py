import asyncio # Python is cool!
from core.game import Game

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
