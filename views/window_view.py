import contextlib
import operator

from conts import WIDTH, Color, BALL_RADIUS, PLAYER_RADIUS
from utils import convert_time

with contextlib.redirect_stdout(None):
    import pygame

pygame.font.init()


NAME_FONT = pygame.font.SysFont('comicsans', 20)
TIME_FONT = pygame.font.SysFont('comicsans', 30)
SCORE_FONT = pygame.font.SysFont('comicsans', 26)


def redraw_window(
    players, balls, game_time, score, window
):
    window.fill(Color.WHITE.value)

    for ball in balls:
        pygame.draw.circle(
            window, ball.color,
            (ball.position.x, ball.position.y),
            BALL_RADIUS
        )

    sort_players = sorted(
        players.values(),
        key=operator.attrgetter('score'),
        reverse=True
    )
    for player in sort_players:
        size = (
            PLAYER_RADIUS + round(player.score)
            if len(player.addition) == 0
            else PLAYER_RADIUS + round(player.score // 2)
        )
        pygame.draw.circle(
            window, player.color.value,
            (player.position.x, player.position.y),
            size
        )
        for player_add in player.addition:
            pygame.draw.circle(
                window, player.color.value,
                (player_add.position.x, player_add.position.y),
                round(player.score // 2)
            )

        text = NAME_FONT.render(player.name, 1, (0, 0, 0))
        window.blit(text, (
            player.position.x - text.get_width() / 2,
            player.position.y - text.get_height() / 2
        ))

    sort_players = list(
        reversed(sorted(players, key=lambda x: players[x].score))
    )
    title = TIME_FONT.render('Scoreboard', 1, (0, 0, 0))
    start_y = 25
    x = WIDTH - title.get_width() - 10
    window.blit(title, (x, 5))

    ran = min(len(players), 3)
    for count, i in enumerate(sort_players[:ran]):
        text = SCORE_FONT.render(
            str(count + 1) + '. ' + str(players[i].name), 1, (0, 0, 0)
        )
        window.blit(text, (x, start_y + count * 20))

    text = TIME_FONT.render('Time: ' + convert_time(game_time), 1, (0, 0, 0))
    window.blit(text, (10, 10))

    text = TIME_FONT.render('Score: ' + str(round(score)), 1, (0, 0, 0))
    window.blit(text, (10, 15 + text.get_height()))
