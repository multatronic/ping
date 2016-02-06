__author__ = 'revok'

import pygame, logging, math
from pygame import K_ESCAPE, QUIT
from ping.ecs import *
from ping.physics import *
from ping.graphics import *
from ping.objects import *
from ping.input import *


class Ping():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.clock = pygame.time.Clock()

        self.game_running = True
        self.fps = 60
        self.board_width = 800
        self.board_height = 600
        self.player_score = 0
        self.enemy_score = 0
        self.player_start_pos = [self.board_width / 2, 10]
        self.enemy_start_pos = [self.board_width / 2, self.board_height - 10]
        self.ball_position = [400, 300]

        self.systems = {
            'physics': PhysicsSystem(self.board_width, self.board_height, 10, 590),
            'graphics': GraphicsSystem(),
            'input': InputSystem()
        }

        pygame.init()
        self.font = pygame.font.Font(None, 36)
        self.display_surface = pygame.display.set_mode((self.board_width, self.board_height))
        pygame.display.set_caption('Oh, the excitement!')
        self.systems['input'].add_keyboard_input_handler(KEYDOWN, K_ESCAPE, self.quit_game)
        self.systems['input'].add_generic_event_handler(QUIT, self.quit_game)
        self.systems['input'].add_generic_event_handler(pygame.USEREVENT + 1, self.score_ball)

    def score_ball(self, event=None):
        self.reset_ball_position(event.ball)
        if event.player_point:
            self.player_score += 1
        else:
            self.enemy_score += 1

    def show_score(self):
        text = self.font.render(str(self.player_score), 0, (255, 255, 255))
        self.display_surface.blit(text, (0, 0))
        text = self.font.render(str(self.enemy_score), 0, (255, 255, 255))
        self.display_surface.blit(text, (self.board_width - text.get_rect().width, 0))

    def reset_ball_position(self, ball):
        physics_component = ball.get_component('physics')
        physics_component.sync_position(position=self.ball_position)
        physics_component.set_direction([0, 0])

    def quit_game(self, event=None):
        self.game_running = False

    def add_game_object(self, game_object):
        for name, system in self.systems.items():
            if game_object.get_component(name) is not None:
                system.add_object(game_object)

    def remove_game_object(self, game_object):
        for name, system in self.systems.items():
            if game_object.get_component(name) is not None:
                system.remove_object(game_object)

    def update_systems(self, delta_time):
        for name, system in self.systems.items():
            system.update(delta_time)

    def run_game_loop(self):
        'Main game loop'
        player_paddle = PlayerPaddle(self.player_start_pos, self.display_surface)
        self.add_game_object(player_paddle)

        # Add enemy paddle.
        self.add_game_object(Paddle(self.enemy_start_pos, self.display_surface))

        ball = Ball(list(self.ball_position), self.display_surface)
        self.add_game_object(ball)

        while self.game_running:
            self.clock.tick(self.fps)
            self.draw_board()
            self.update_systems(self.clock.get_time() / 1000)  # pass frame time in seconds
            self.show_score()
            pygame.display.update()

    def draw_board(self):
        self.display_surface.fill((0, 0, 0))


if __name__ == '__main__':
    Ping().run_game_loop()