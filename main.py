# Autobird
# Edwin Camuy, 30 - 6 - 2023
import pygame
import sys
from gamestate import GameState, SubState
from soundplayer import SoundPlayer
from world import World
from bird import Bird
from pipes import Pipes
from random import seed
from gameutil import *
from autoagent import AutoAgent
from controlledagent import ControlledAgent

SCALE = 920
DRAW_SPEED = 60
SPEED_FACTOR = 1
DEBUG = False


def pygame_setup():
    pygame.init()
    seed(1917)

    pygame.display.set_caption("Autobird")
    icon = pygame.image.load('assets/bird2.png')
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((SCALE, SCALE), flags=pygame.SCALED, vsync=1)

    clock = pygame.time.Clock()

    font1 = pygame.font.Font('assets/plasmati.ttf', 42)
    font2 = pygame.font.Font('assets/plasmati.ttf', 80)

    return GameState(screen, clock, font1, font2)


def tick(game: GameState, world: World, agent: AutoAgent = None):

    # Controls
    if agent is None or game.sub_state == SubState.POSTGAME:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.stop()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.sub_state == SubState.PREGAME:
                        game.start_game()
                        world.activate()
                        print("start")
                    elif game.sub_state == SubState.GAME:
                        world.jump()
                    elif game.sub_state == SubState.POSTGAME:
                        game.reset_score()
                        game.start_pre_game()
                        world.reset()

    else:
        # Agent control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.stop()

        if game.sub_state == SubState.PREGAME:
            game.start_game()
            world.activate()
        elif game.sub_state == SubState.GAME:
            s = world.get_state()
            # Agent returns true for jump
            if agent.get_action(s):
                world.jump()

    failed, scored = world.update()
    if failed:
        game.end_game()
    if scored:
        game.inc_score()
        print(game.score)


def draw(game: GameState, world: World, scale: int, agent: AutoAgent = None, debug=False):
    # flip() the display to put your work on screen
    pygame.display.flip()

    # fill the screen with a color to wipe away anything from last frame
    game.screen.fill("#111811")

    # RENDER YOUR GAME HERE
    world.draw(game.screen, scale)

    if game.sub_state == SubState.PREGAME:
        draw_text(game.font1, "Space to Jump", game.screen, 0.5, 0.5, SCALE)
    elif game.sub_state == SubState.GAME:
        score_str = '{:02d}'.format(game.score)
        draw_text(game.font1, score_str, game.screen, 0.5, 0.2, SCALE)
    elif game.sub_state == SubState.POSTGAME:
        score_str = '{:02d}'.format(game.score)
        draw_text(game.font2, score_str, game.screen, 0.5, 0.4, SCALE)
        draw_text(game.font2, "GAME OVER", game.screen, 0.5, 0.6, SCALE)

    if debug:
        world.draw_debug(game.screen, scale)
        if agent is not None:
            agent.draw_debug(game.screen, scale)


def start_game(game: GameState, world: World):
    game.start_game()
    world.activate()


def end_game(game: GameState, world: World):
    game.end_game()
    world.deactivate()


def main():
    game = pygame_setup()
    sound_player = SoundPlayer()

    bird = Bird()
    bird.initialize_sprite(SCALE)

    active_pipes = Pipes(0.7, 0.5)
    active_pipes.initialize_sprite(SCALE)

    inactive_pipes = Pipes(1.6, 0.5)
    inactive_pipes.initialize_sprite(SCALE)
    inactive_pipes.reset_pos(0.5)  # Randomizing the position for the second set of pipes

    world = World(bird, active_pipes, inactive_pipes, sound_player)

    agent = ControlledAgent(0.38)

    game.run()

    while game.is_running():
        for _ in range(SPEED_FACTOR):
            tick(game, world, agent)
        draw(game, world, SCALE, agent, DEBUG)
        game.clock.tick(DRAW_SPEED)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
