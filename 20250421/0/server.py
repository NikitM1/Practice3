import asyncio
from prog import sqroots

async def echo(reader, writer):
    print(writer.get_extra_info('peername')
    while data := await reader.readline():
        try:
            res = prog.sqroots(data.strip().decode())
        except Exception:
            res=''
        writer.write(f"{res.swapcase()}\n".encode())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

def server():
    asyncio.run(main())