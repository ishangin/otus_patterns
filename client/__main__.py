import json
from multiprocessing.connection import Client
from struct import pack
from time import sleep

address = ('localhost', 5577)
password = "P@$$w0rd"


with Client(address, authkey=bytes(password, "UTF8")) as conn:
    conn.send("USER: user3")
    conn.send("PASSWORD: pass3")

    token = conn.recv()
    token = token.replace("TOKEN: ", "")

    # new game command
    new_game = pack("3i", -1, -1, 0) + bytes(
        json.dumps(
            {
                "players": [0, 3],
                "jwt": token
            }
        ),
        "UTF8"
    )
    conn.send(new_game)
    game_id = conn.recv()
    game_id = game_id.replace("GAME_ID: ", "")

    spaceship = pack("3i", int(game_id), -1, 14) + bytes(
        json.dumps(
            {
                "type": "SpaceShip",
                "position": (7, 7),
                "velocity": (5, 2),
                "radius": 5,
                "jwt": token
            }
        ),
        "UTF8"
    )
    conn.send(spaceship)
    spaceship_id = conn.recv()
    spaceship_id = spaceship_id.replace("OBJECT_ID: ", "")

    move = pack("3i", int(game_id), int(spaceship_id), 1) + bytes(
        json.dumps(
            {
                "jwt": token
            }
        ),
        "UTF8"
    )
    conn.send(move)
    spaceship_id = conn.recv()

    sleep(5)
    i = input()
