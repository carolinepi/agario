import contextlib

with contextlib.redirect_stdout(None):
    import pygame

from sockets.client import ClientSocket
from conts import WIDTH, HEIGHT, START_VEL, PLAYER_RADIUS
from models.position import Position
from views.window_view import redraw_window


class ClientView:
    def __init__(self, player_name: str) -> None:
        self.server = ClientSocket()
        self.current_id = self.server.connect(player_name)
        self.start = True
        self.window = None

    def main(self) -> None:
        balls, players, game_time = self.server.send('get')

        clock = pygame.time.Clock()

        while self.start:
            player = players[self.current_id]
            clock.tick(30)
            if player.addition:
                vel = START_VEL - round(player.score // 2 / 14)
            else:
                vel = START_VEL - round(player.score / 14)
            if vel <= 1:
                vel = 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if player.position.x - vel - PLAYER_RADIUS - player.score >= 0:
                    player.position = Position(
                        x=player.position.x - vel,
                        y=player.position.y
                    )

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if player.position.x + vel + PLAYER_RADIUS + player.score <= WIDTH:
                    player.position = Position(
                        x=player.position.x + vel,
                        y=player.position.y
                    )

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if player.position.y - vel - PLAYER_RADIUS - player.score >= 0:
                    player.position = Position(
                        x=player.position.x,
                        y=player.position.y - vel
                    )

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if player.position.y + vel + PLAYER_RADIUS + player.score <= HEIGHT:
                    player.position = Position(
                        x=player.position.x,
                        y=player.position.y + vel
                    )

            data = f'move {player.position.x} {player.position.y}'

            if keys[pygame.K_SPACE]:
                if player.score > 35 and len(player.addition) == 0:
                    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        data = f'jump down'
                    if keys[pygame.K_UP] or keys[pygame.K_w]:
                        data = f'jump up'
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        data = 'jump right'
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        data = 'jump left'

            balls, players, game_time = self.server.send(data)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.start = False

            redraw_window(
                players, balls, game_time, player.score, self.window
            )
            pygame.display.update()

        self.server.disconnect()
        pygame.quit()
        quit()

    def set_client_window(self, window):
        self.window = window
