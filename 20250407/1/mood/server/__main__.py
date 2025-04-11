import asyncio
from .. import common
import cowsay
import random
import shlex
import sys

SIZE = 10


class Player:
    def __init__(self):
        self.x = self.y = 0

    def moveHorizontally(self, flag):
        self.x = (self.x + flag) % SIZE

    def moveVertically(self, flag):
        self.y = (self.y + flag) % SIZE

    def printPosition(self):
        return 'Moved to ' + str(
            (self.x, self.y)) + '\n' + game.encounter(self.x, self.y)


class Monster:
    def __init__(self, name, hitpoints, x, y, speech):
        self.name = name
        self.hitpoints = hitpoints
        self.x = x
        self.y = y
        self.speech = speech

    def attacked(self, damage):
        damage = min(damage, self.hitpoints)
        self.hitpoints -= damage
        return self.hitpoints, damage


class MUD:
    def __init__(self):
        self.monsters = {}
        self.players = {}

    def move(self, player, x, y):
        if x:
            player.moveHorizontally(x)
        elif y:
            player.moveVertically(y)
        return player.printPosition()

    def encounter(self, x, y):
        if (x, y) not in self.monsters:
            return ''
        if self.monsters[(x, y)].name == 'jgsbat':
            return cowsay.cowsay(
                self.monsters[(x, y)].speech, cowfile=common.JGSBAT
            ) + '\n'
        if self.monsters[(x, y)].name:
            return cowsay.cowsay(
                self.monsters[(x, y)].speech, cow=self.monsters[(x, y)].name
            ) + '\n'
        return ''

    def addmon(self, name, hitpoints, x, y, speech):
        f = int((x, y) in self.monsters)
        self.monsters[(x, y)] = Monster(name, hitpoints, x, y, speech)
        return 'Added monster ' + name + ' to ' + str(
            (x, y)) + ' saying ' + speech + '\n' + (
                f * 'Replaced the old monster\n')

    def attack(self, player, name, damage):
        if (player.x, player.y) not in self.monsters or self.monsters[(
            player.x, player.y
        )].name != name:
            return 'invalid'
        hitpoints, damage = self.monsters[
            (player.x, player.y)].attacked(damage)
        if hitpoints == 0:
            del self.monsters[(player.x, player.y)]
        return 'Attacked ' + name + ', damage ' + str(
            damage) + ' hp\n' + name + (' now has ' + str(hitpoints) if int(
                hitpoints) else ' died') + '\n'

    async def wanderMonsters(self):
        direction = ['right', 'left', 'up', 'down']
        while True:
            print(self.monsters)
            await asyncio.sleep(30)
            if not self.monsters:
                continue
            while True:
                x, y = random.choice(list(self.monsters))
                monster = self.monsters[(x, y)]
                i = random.randint(0, 3)
                x = (x + (i < 2) * (-1) ** (i % 2)) % SIZE
                y = (y - (i > 1) * (-1)**(i % 2)) % SIZE
                if (x, y) not in self.monsters:
                    break
            del self.monsters[(monster.x, monster.y)]
            monster.x, monster.y = x, y
            self.monsters[(x, y)] = monster
            print(self.monsters)
            encounter = self.encounter(x, y)

            for user in self.players:
                _player, _buffer = self.players[user]
                await _buffer.put(
                    monster.name + ' moved one cell ' + direction[i] + '\n'
                    + ((_player.x, _player.y) == (x, y )) * encounter
                )


async def serve(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    async def cmdExec(data):

        if not data.strip():
            return None
        cmd, *args = shlex.split(data)
        match cmd:
            case 'move':
                await game.players[username][1].put(
                    game.move(player, *list(map(int, args)))
                )
            case 'addmon':
                result = game.addmon(
                    args[0], int(args[1]), int(args[2]), int(args[3]), args[4]
                )
                await game.players[username][1].put(result)
                for user in game.players:
                    if user != username:
                        await game.players[user][1].put(username + ': ' + result)
            case 'attack':
                result = game.attack(player, args[0], int(args[1]))
                if result == 'invalid':
                    await game.players[username][1].put(
                        'No ' + args[0] + ' here\n'
                    )
                else:
                    await game.players[username][1].put(result)
                    for user in game.players:
                        if user != username:
                            await game.players[user][1].put(
                                username + ': ' + result
                            )
            case 'sayall':
                result = args[0]
                for user in game.players:
                    if user != username:
                        await game.players[user][1].put(username + ': ' + result)

    addr = writer.get_extra_info("peername")
    print(f'Connected via {addr[0]}:{addr[1]}')

    username = (await reader.readline()).decode().strip()
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
        await game.players[user][1].put(username + ' joined the server\n')

    player = Player()
    game.players[username] = player, asyncio.Queue()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(game.players[username][1].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive], return_when=asyncio.FIRST_COMPLETED
        )
        for task in done:
            if task is send:
                send = asyncio.create_task(reader.readline())
                await cmdExec(task.result().decode())
            elif task is receive:
                receive = asyncio.create_task(game.players[username][1].get())
                writer.write(f"{task.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    del game.players[username]
    writer.close()
    await writer.wait_closed()
    for user in game.players:
        await game.players[user][1].put(username + ' left the server\n')
    print(f'Disconnected from {addr[0]}:{addr[1]}')


async def main():
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    print(f"Serving at {host}:{port}")

    server = await asyncio.start_server(serve, host, port)
    asyncio.create_task(game.wanderMonsters())
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    global game
    game = MUD()
    asyncio.run(main())
