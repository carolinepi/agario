import math
import operator
import pickle
import random
from _thread import start_new_thread

import socket
import time
from typing import List

from models.ball import Ball
from conts import WIDTH, HEIGHT, PORT, ROUND_TIME, Color, COMMANDS
from models.player import Player
from models.position import Position
from utils import get_distance, get_random_color


class Server:
    MASS_LOSS_TIME = 20
    BALL_RADIUS = 5
    START_RADIUS = 8

    def __init__(self):
        self.socket = None
        self.id = 0
        self.start = False
        self.players = {}
        self.balls = []
        self.start_time = None
        self.next_round = 1
        self.game_time = 0

    def setup_sockets(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            host_name = socket.gethostname()
            server_ip = socket.gethostbyname(host_name)

            self.socket.bind((server_ip, PORT))
        except socket.error:
            print('[SERVER] Server could not start')
            quit()
            return

        self.socket.listen()
        print(f'[SERVER] Server Started with local ip {server_ip}')

    def release_player_mass(self) -> None:
        for player in self.players.values():
            if player.score > 8:
                player.score = math.floor(player.score * 0.95)

    def get_player_start_location(self) -> Position:
        stop = True
        while True:
            x = random.randrange(0, WIDTH)
            y = random.randrange(0, HEIGHT)
            for player in self.players.values():
                dis = get_distance(
                    random.randrange(0, WIDTH), player.position.x,
                    random.randrange(0, HEIGHT), player.position.y
                )
                if dis <= player.START_RADIUS + player.score:
                    stop = False
                    break
            if stop:
                break
        return Position(x, y)

    def check_collision(self) -> None:
        sort_players = sorted(
            self.players.values(),
            key=operator.attrgetter('score'),
        )
        for x, player in enumerate(sort_players):
            self.balls_collision(player)
            self.player_collision(player, sort_players[x + 1:])

    def balls_collision(self, player: Player) -> None:
        for ball in self.balls:
            dis = get_distance(
                player.position.x, ball.position.x,
                player.position.y, ball.position.y
            )
            if dis <= player.START_RADIUS + player.score:
                player.score = player.score + 0.5
                self.balls.remove(ball)

    def player_collision(self, player: Player, sort_players: List[Player]):
        for next_player in sort_players:
            dis = get_distance(
                player.position.x, next_player.position.x,
                player.position.y, next_player.position.y
            )
            if dis < next_player.score - player.score * 0.85:
                next_player.score = math.sqrt(
                    next_player.score ** 2 + player.score ** 2
                )
                start_position = self.get_player_start_location()
                player.recreate(start_position)
                print(f'[GAME] {next_player.name} ATE {player.name}')

    def create_balls(self) -> None:
        if len(self.balls) < 50:
            n = random.randrange(100, 120)
        else:
            n = random.randrange(40, 80)
        stop = True
        for i in range(n):
            while True:
                x = random.randrange(0, WIDTH)
                y = random.randrange(0, HEIGHT)
                for player in self.players.values():
                    dis = get_distance(
                        x, player.position.x,
                        y, player.position.y
                    )
                    if dis <= player.START_RADIUS + player.score:
                        stop = False
                if stop:
                    break
            self.balls.append(
                Ball(position=Position(x, y), color=Color.RED.value)
            )

    def recreate(self):
        for player in self.players.values():
            player.recreate(self.get_player_start_location())

    def threaded_client(self, conn: socket.socket, current_id: int) -> None:
        data = conn.recv(16)
        name = data.decode('utf-8')
        print('[LOG]', name, 'connected to the server.')

        start_position = self.get_player_start_location()
        player = Player(
            id=current_id,
            position=start_position,
            name=name,
            color=get_random_color()

        )
        self.players[current_id] = player

        conn.send(str.encode(str(current_id)))

        while True:
            if self.start:
                self.game_time = round(time.time() - self.start_time)
                if self.game_time >= ROUND_TIME:
                    self.start = False
                else:
                    if self.game_time // self.MASS_LOSS_TIME == self.next_round:
                        self.next_round += 1
                        self.release_player_mass()
                        print(f'[GAME] {name}`s Mass depleting')

            try:
                data = conn.recv(32)
                if not data:
                    break

                data = data.decode('utf-8')

                if data.split(' ')[0] == COMMANDS.move.value:
                    split_data = data.split(' ')
                    x = int(split_data[1])
                    y = int(split_data[2])
                    player.position = Position(x, y)

                    if self.start:
                        self.check_collision()

                    if len(self.balls) < 100:
                        self.create_balls()
                        print('[GAME] Generating more balls')
                    send_data = pickle.dumps(
                        (self.balls, self.players, self.game_time)
                    )

                elif data.split(' ')[0] == COMMANDS.jump.value:
                    player.generate_player_addition(data.split(' ')[1])
                    send_data = pickle.dumps(
                        (self.balls, self.players, self.game_time)
                    )

                elif data.split(' ')[0] == COMMANDS.id.value:
                    send_data = str.encode(str(current_id))

                elif data.split(' ')[0] == COMMANDS.get.value:
                    send_data = pickle.dumps(
                        (self.balls, self.players, self.game_time)
                    )

                elif data.split(' ')[0] == COMMANDS.replay.value:
                    self.start = True
                    self.start_time = time.time()
                    self.recreate()
                    send_data = pickle.dumps(
                        (self.balls, self.players, self.game_time)
                    )
                conn.send(send_data)

            except Exception as e:
                print(e)
                break
            time.sleep(0.001)

        print('[DISCONNECT] Name:', name, ', Client Id:', current_id,
              'disconnected')

        del self.players[current_id]
        conn.close()

    def main(self):
        print('[GAME] Setting up level')
        print('[SERVER] Waiting for connections')
        while True:
            host, addr = self.socket.accept()
            print('[CONNECTION] Connected to:', addr)

            if not self.start:
                self.start = True
                self.start_time = time.time()
                print('[STARTED] Game Started')

            start_new_thread(self.threaded_client, (host, self.id))
            self.id += 1
