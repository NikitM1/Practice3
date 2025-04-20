"""
MOOD server module.

Handle commands and store game parameters.
"""

import asyncio
from .. import common
import cowsay
import gettext
import random
import shlex
import sys

SIZE = 10
DOMAINS={
    'ru_RU.UTF8': gettext.translation('serverLocales','po',fallback=True),
    'en_US.UTF8': gettext.NullTranslations()
}


class Player:
    """A class stores player information and handle their movements."""

    def __init__(self):
        """Initialize a player with position (0, 0)"""
        self.x = self.y = 0
        self.locale='en_US.UTF8'

    def moveHorizontally(self, flag):
        """
        Move the player horizontally.

        :param flag: player's movement direction.
        """
        self.x = (self.x + flag) % SIZE

    def moveVertically(self, flag):
        """
        Move the player vertically.

        :param flag: players movement firection.
        """
        self.y = (self.y + flag) % SIZE

    def printPosition(self):
        """
        Create a message with a new player's position and monster message.

        :return: string to be printed to the player.
        """
        return (self.x, self.y), game.encounter(self.x, self.y)


class Monster:
    """A class stores monster information and handle attacks on it."""

    def __init__(self, name, hitpoints, x, y, speech):
        """
        Initialize a monster.

        :param name: the monster's name.
        :param hitpoints: the monster's hitpoints.
        :param x: monster's position on the X-axis.
        :param y: monster's position on the Y-axis.
        :param speech: the monster's speech.
        """
        self.name = name
        self.hitpoints = hitpoints
        self.x = x
        self.y = y
        self.speech = speech

    def attacked(self, damage):
        """
        Attack the monster.

        :param damage: the maximum damage that can be dealt to a monster.
        :return: a tuple with the damage dealt and remaining hitpoints.
        """
        damage = min(damage, self.hitpoints)
        self.hitpoints -= damage
        return self.hitpoints, damage


class MUD:
    """A key class for the game, storing all information about players and \
monsters."""

    def __init__(self):
        """Initislize a game lists of players and monsters."""
        self.monsters = {}
        self.players = {}
        self.wandering = asyncio.create_task(self.wanderMonsters())

    async def wanderMonsters(self):
        """Handle the functionality of wandering monsters. \
Move a random monster one cell in random direction."""
        direction = ['right', 'left', 'up', 'down']
        while True:
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
            encounter = self.encounter(x, y)

            for user in self.players:
                _player, _buffer = self.players[user]
                encounterResult=((_player.x, _player.y) == (x, y)) * encounter
                result='{} moved one cell {}\n{}'.format(monster.name, direction[i], encounterResult)
                await _buffer.put(result)

    def move(self, player, x, y):
        """
        Handle move command and call player.move...() function.

        :param player: player to be moved.
        :param x: player's bias along X-axis.
        :param y: player's bias along Y-axis.
        :return: string to be printed to the player after moving.
        """
        if x:
            player.moveHorizontally(x)
        elif y:
            player.moveVertically(y)
        return player.printPosition()

    def encounter(self, x, y):
        """
        Create monster's message.

        :param x: X-coordinate.
        :param y: Y-coordinate.
        :return: monster's message.
        """
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
        """
        Add a new monster to a game monsters list.

        :param name: the monster's name.
        :param hitpoints: the monster's hitpoints.
        :param x: monster's position on the X-axis.
        :param y: monster's position on the Y-axis.
        :param speech: the monster's speech.
        :return: string to be printed to the player after creation.
        """
        f = int((x, y) in self.monsters)
        self.monsters[(x, y)] = Monster(name, hitpoints, x, y, speech)
        return name, (x,y), speech, f

    def attack(self, player, name, damage):
        """
        Handle the attack on the monster.

        :param player: player attacking a monster.
        :param name: the monster's name.
        :param damage: the maximum damage that can be dealt to a monster.
        :return: string to be printed to a player after the attack.
        """
        if (player.x, player.y) not in self.monsters or self.monsters[(
            player.x, player.y
        )].name != name:
            return 'invalid'
        hitpoints, damage = self.monsters[
            (player.x, player.y)].attacked(damage)
        if hitpoints == 0:
            del self.monsters[(player.x, player.y)]
        return name, damage, name, hitpoints

    def sayall(self, message):
        return message

    def movemonsters(self, mode):
        """
        Handle wanderMonsters on and off.
        
        :param mode: function work move (on or off).
        :return: string to be printed to the players.
        """
        if mode == 'on' and not self.wandering:
            self.wandering = asyncio.create_task(wanderMonsters())
        elif mode == 'off' and self.wandering:
            self.wandering.cancel()
            self.wandering = None

        return mode
    
    def locale(self, player, locale):
        """
        Handle locale command and set up new locale.

        :param player: player who entered command.
        :param locale: new locale.
        """
        player.locale=locale
        return locale


async def serve(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """
    Create client-server interaction.

    :param reader: reading stream.
    :param writer: writing stream.
    """
    async def cmdExec(data):
        """
        Execute a command.

        :param data: command string.
        """
        if not data.strip():
            return None
        cmd, *args = shlex.split(data)
        match cmd:
            case 'move':
                result=game.move(player, *list(map(int, args)))
                await game.players[username][1].put(
                    'Moved to {}\n{}'.format(*result)
                )
            case 'addmon':
                *result,f = game.addmon(
                    args[0], int(args[1]), int(args[2]), int(args[3]), args[4]
                )
                for user in game.players:
                    await game.players[user][1].put(
                        'Added monster {} to {} saying {}\n'.format(*result)+f*'Replaced the old monster\n'
                    )
            case 'attack':
                result = game.attack(player, args[0], int(args[1]))
                if result == 'invalid':
                    await game.players[username][1].put(
                        'No {} here\n'.format(args[0])
                    )
                else:
                    *result, hitpoints=result
                    for user in game.players:
                        await game.players[user][1].put(
                            'Attacked {}, damage {} hp\n{}'.format(*result)+(' now has {}\n'.format(hitpoints) if hitpoints else ' died\n')
                        )
            case 'sayall':
                result = game.sayall(args[0])
                for user in game.players:
                    if user != username:
                        await game.players[user][1].put(
                            username + ': ' + result
                        )
            case 'movemonsters':
                result = game.movemonsters(args[0])              
                for user in game.players:
                    await game.players[user][1].put('Moving monsters: {}'.format(result))
            case 'locale':
                result=game.locale(player, args[0])
                await game.players[username][1].put(
                    'Set up locale: {}\n'.format(result)
                )

    addr = writer.get_extra_info("peername")
    print('Connected via {}:{}'.format(addr[0],addr[1]))

    username = (await reader.readline()).decode().strip()
    if username in game.players:
        writer.write(b'0')
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        print('Disconnected from {}:{}'.format(addr[0],addr[1]))
        return

    writer.write(b'1')
    await writer.drain()
    for user in game.players:
        await game.players[user][1].put('{} joined the server\n'.format(username))

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
                writer.write(f'{task.result()}\n'.encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    del game.players[username]
    writer.close()
    await writer.wait_closed()
    for user in game.players:
        await game.players[user][1].put('{} left the server\n'.format(username))
    print('Disconnected from {}:{}'.format(addr[0],addr[1]))


async def main():
    """Run a game."""
    global game
    game = MUD()
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    print('Serving at {}:{}'.format(host, port))

    server = await asyncio.start_server(serve, host, port)
    async with server:
        await server.serve_forever()
