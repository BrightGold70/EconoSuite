import asyncio
from notebooklm import NotebookLMClient

async def check():
    async with await NotebookLMClient.from_storage() as client:
        print("Notebooks methods:", dir(client.notebooks))
        print("Sources methods:", dir(client.sources))

if __name__ == "__main__":
    try:
        asyncio.run(check())
    except Exception as e:
        print("Not logged in, but here is the exception:", e)
        # Even without from_storage working properly, we can inspect the class
        from notebooklm.client import NotebookLMClient
        print(dir(NotebookLMClient))
