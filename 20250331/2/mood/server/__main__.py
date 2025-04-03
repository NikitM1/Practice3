import asyncio
import cowsay
import shlex
import socket
import sys

JGSBAT=cowsay.read_dot_cow(open('jgsbat.cow'))
SIZE=10

class Player:
    def __init__(self):
        self.x=self.y=0
    
    def moveHorizontally(self,flag):
        self.x=(self.x+flag)%SIZE
    
    def moveVertically(self,flag):
        self.y=(self.y+flag)%SIZE
    
    def printPosition(self):
        if (self.x, self.y) in game.monsters:
            return 'Moved to '+str((self.x,self.y))+'\n'+game.encounter(self.x,self.y)
        return 'Moved to '+str((self.x,self.y))+'\n'

class Monster:
    def __init__(self,name,hitpoints,x,y,speech):
        self.name=name
        self.hitpoints=hitpoints
        self.x=x
        self.y=y
        self.speech=speech
    
    def attacked(self,damage):
        damage=min(damage,self.hitpoints)
        self.hitpoints-=damage
        return self.hitpoints,damage

class MUD:
    def __init__(self):
        self.monsters={}
        self.players={}
    
    def move(self,player,x,y):
        if x:
            player.moveHorizontally(x)
        elif y:
            player.moveVertically(y)
        return player.printPosition()
    
    def encounter(self,x,y):
        if self.monsters[(x,y)].name=='jgsbat':
            return cowsay.cowsay(self.monsters[(x,y)].speech,cowfile=JGSBAT)+'\n'
        elif self.monsters[(x,y)].name:
            return cowsay.cowsay(self.monsters[(x,y)].speech,cow=self.monsters[(x,y)].name)+'\n'
    
    def addmon(self,name,hitpoints,x,y,speech):
        f=int((x,y) in self.monsters)
        self.monsters[(x,y)]=Monster(name,hitpoints,x,y,speech)
        return 'Added monster '+name+' to '+str((x,y))+' saying '+speech+'\n'+(f*'Replaced the old monster\n')
    
    def attack(self,player,name,damage):
        if (player.x,player.y) not in self.monsters or self.monsters[(player.x,player.y)].name!=name:
            return 'invalid'
        hitpoints,damage=self.monsters[(player.x,player.y)].attacked(damage)
        if hitpoints==0:
            del self.monsters[(player.x,player.y)]
        return 'Attacked '+name+', damage '+str(damage)+' hp\n'+name+(' now has '+str(hitpoints) if int(hitpoints) else ' died')+'\n'

async def serve(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    async def cmdExec(data):
        nonlocal player, username
        
        if not data.strip(): return None
        cmd, *args=shlex.split(data)
        match cmd:
            case 'move':
                await game.players[username].put(game.move(player,*list(map(int,args))))
            case 'addmon':
                result=game.addmon(args[0],int(args[1]),int(args[2]),int(args[3]),args[4])
                await game.players[username].put(result)
                for user in game.players:
                    if user!=username:
                        await game.players[user].put(username+': '+result)
            case 'attack':
                result=game.attack(player,args[0],int(args[1]))
                if result=='invalid':
                    await game.players[username].put('No '+args[0]+' here\n')
                else:
                    await game.players[username].put(result)
                    for user in game.players:
                        if user!=username:
                            await game.players[user].put(username+': '+result)
            case 'sayall':
                result=args[0]
                for user in game.players:
                    if user!=username:
                        await game.players[user].put(username+': '+result)
    
    addr = writer.get_extra_info("peername")
    print(f'Connected via {addr[0]}:{addr[1]}')
    
    username=(await reader.readline()).decode().strip()
    if username in game.players:
        writer.write(b'0')
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print(f'Disconnected from {addr[0]}:{addr[1]}')
        return
    
    writer.write(b'1')
    await writer.drain()
    for user in game.players:
        await game.players[user].put(username+' joined the server\n')
    
    game.players[username]=asyncio.Queue()
    player=Player()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(game.players[username].get())
    
    while not reader.at_eof():
        done,pending=await asyncio.wait([send,receive],return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if task is send:
                send = asyncio.create_task(reader.readline())
                await cmdExec(task.result().decode())
            elif task is receive:
                receive = asyncio.create_task(game.players[username].get())
                writer.write(f"{task.result()}\n".encode())
                await writer.drain()
        
    send.cancel()
    receive.cancel()
    del game.players[username]
    writer.close()
    await writer.wait_closed()
    for user in game.players:
        await game.players[user].put(username+' left the server\n')
    print(f'Disconnected from {addr[0]}:{addr[1]}')
    

async def main():
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    print(f"Serving at {host}:{port}")
 

    server = await asyncio.start_server(serve, host, port)
    async with server:
        await server.serve_forever()

if __name__=='__main__':
    global game
    game=MUD()
    asyncio.run(main())