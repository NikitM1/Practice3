import asyncio

async def echo(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)    
    while data := await reader.readline():
        command = data.decode().strip() 
        if command.startswith("print "):
            response = command[6:] 
            writer.write(response.encode() + b'\n')
        elif command.startswith("info "):
            param = command[5:] 
            peername = writer.get_extra_info('peername')
            if param=='host':
                response = f"Host: {peername[0]}"
            elif param=='port':
                response = f"Port: {peername[1]}"
            writer.write(response.encode() + b'\n')
        else:
            writer.write(b"Unknown command\n")
        
        await writer.drain() 

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())