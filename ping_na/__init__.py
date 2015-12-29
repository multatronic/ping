__author__ = 'revok'

import pygame, logging, math

from ping_na.component import *
from ping_na.physics import *
from ping_na.graphics import *
from ping_na.objects import *
from ping_na.input import *


class Ping():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.clock = pygame.time.Clock()

        self.game_running = True
        self.fps = 60
        self.board_width = 800
        self.board_height = 600
        self.player_start_pos = [self.board_width / 2, 20]
        self.enemy_start_pos = [self.board_width / 2, self.board_height - 20]
        self.ball_position = [400, 300]

        self.systems = {
            'physics': PhysicsSystem(self.clock, self.board_width, self.board_height),
            'graphics': GraphicsSystem(self.clock),
            'input': InputSystem(self.clock)
        }

        pygame.init()
        self.display_surface = pygame.display.set_mode((self.board_width, self.board_height))
        self.systems['input'].add_keyboard_input_handler(KEYDOWN, K_ESCAPE, self.quit_game)
        self.systems['input'].add_generic_event_handler(QUIT, self.quit_game)

    def quit_game(self):
        self.game_running = False

    def add_game_object(self, game_object):
        for name, system in self.systems.items():
            if game_object.get_component(name) is not None:
                system.add_object(game_object)

    def update_systems(self):
        for name, system in self.systems.items():
            system.update()

    def run_game_loop(self):
        'Main game loop'
        player_paddle = Paddle(self.player_start_pos, self.display_surface)
        player_paddle.add_component(InputComponent({
            KEYDOWN: {
                K_LEFT: lambda: player_paddle.get_component('physics').set_velocity((-5, 0)),
                K_RIGHT: lambda: player_paddle.get_component('physics').set_velocity((5, 0))
            }
        }))
        self.add_game_object(player_paddle)

        # Add enemy paddle.
        self.add_game_object(Paddle(self.enemy_start_pos, self.display_surface))

        ball = Ball(self.ball_position, self.display_surface)
        self.add_game_object(ball)

        while self.game_running:
            self.clock.tick(self.fps)
            self.draw_board()
            self.update_systems()
            pygame.display.update()

    def draw_board(self):
        self.display_surface.fill((0, 0, 0))


if __name__ == '__main__':
    Ping().run_game_loop()