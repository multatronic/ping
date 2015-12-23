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

        self.systems = {
            'physics': PhysicsSystem(self.clock),
            'graphics': GraphicsSystem(self.clock),
            'input': InputSystem(self.clock)
        }

        self.game_running = True
        self.fps = 30
        self.board_width = 800
        self.board_height = 600
        self.player_start_pos = [self.board_width / 2, 20]
        self.enemy_start_pos = [self.board_width / 2, self.board_height - 20]
        self.ball_position = (400, 300)

        pygame.init()
        self.display_surface = pygame.display.set_mode((800, 600))

    def add_game_object(self, object):
        for name, system in self.systems.items():
            if object.get_component(name) is not None:
                system.add_object(object)

    def update_systems(self):
        for name, system in self.systems.items():
            system.update()

    def run_game_loop(self):
        'Main game loop'
        # global CLOCK, ENEMY_PADDLE, PLAYER_PADDLE, BALL

        # PHYSICS_MANAGER = PhysicsManager()
        player_paddle = Paddle(self.player_start_pos, self.display_surface)
        player_paddle.add_component(InputComponent())
        self.add_game_object(player_paddle)

        # Add enemy paddle.
        self.add_game_object(Paddle(self.enemy_start_pos, self.display_surface))
        self.add_game_object(Ball(self.ball_position, self.display_surface))

        #CLOCK = pygame.time.Clock()

        while self.game_running:
            self.clock.tick(self.fps)
            self.draw_board()
            self.update_systems()
            self.handle_input()
            pygame.display.update()

    def handle_input(self):
        # global GAME_RUNNING, HORIZONTAL_SPEED
        for event in pygame.event.get():
            # quit the game if necessary
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                self.game_running = False
            # # else handle input
            # elif event.type == KEYDOWN:
            #     player_moved = False
            #     ball_stationary = BALL.get_velocity() == [0, 0]
            #
            #     if event.key == K_LEFT:
            #         # do stuff
            #         player_moved = True
            #         PLAYER_PADDLE.set_velocity((-5, 0))
            #     elif event.key == K_RIGHT:
            #         # do stuff
            #         player_moved = True
            #         PLAYER_PADDLE.set_velocity((5, 0))
            #
            #     if ball_stationary and player_moved:
            #         ball_velocity = [PLAYER_PADDLE.get_velocity()[0], BALL_SPEED]
            #         BALL.set_velocity(ball_velocity)



    def draw_board(self):
        self.display_surface.fill((0, 0, 0))
        # PLAYER_PADDLE.move()
        # PLAYER_PADDLE.draw()
        # ENEMY_PADDLE.draw()
        # BALL.move()
        # BALL.check_collision(PLAYER_PADDLE.body)
        # BALL.check_collision(ENEMY_PADDLE.body)
        # BALL.draw()


        #
        # class Ball(GameObject):
        #     'A ball.'
        #     def __init__(self, position, display_surface):
        #         'init ball.'
        #         physics_margin = 1
        #         body_width = (BALL_RADIUS - physics_margin) * 2
        #         self.add_component(PhysicsComponent(position, body_width, body_width))
        #         self.add_component(GraphicsComponent('circle', display_surface, body_width, body_width, position))
        #
        #     def check_collision(self, other_rect):
        #         if self.body.colliderect(other_rect):
        #             delta = [other_rect.centerx - self.body.centerx, other_rect.centery - self.body.centery]
        #
        #             if delta[0] <= PADDLE_WIDTH:
        #                 self.reverse_horizontal_velocity()
        #             elif delta[1] <= PADDLE_HEIGHT:
        #                 self.reverse_vertical_velocity()
        #             else:
        #                 self.reverse_horizontal_velocity()
        #                 self.reverse_vertical_velocity()
        #         else:
        #             return None
        #
        #     def move(self):
        #         super().move()
        #         # bounce the ball if necessary
        #         if self.body.left == 0 or self.body.right == BOARD_WIDTH:
        #             self.reverse_horizontal_velocity()
        #         if self.body.top == 0 or self.body.bottom == BOARD_HEIGHT:
        #             self.reverse_vertical_velocity()
        #
        #     # def draw(self):
        #     #     global DISPLAY_SURFACE
        #     #     pygame.draw.circle(DISPLAY_SURFACE, (255, 0, 0), self.body.center, BALL_RADIUS)
        #         # super().draw()
        #
        #
        # class Paddle(GameObject):
        #     'A paddle.'
        #     def __init__(self, position, display_surface):
        #         'init paddle'
        #         self.add_component(PhysicsComponent(position, PADDLE_WIDTH, PADDLE_HEIGHT))
        #         self.add_component(GraphicsComponent('rectangle', display_surface, PADDLE_WIDTH, PADDLE_HEIGHT, position))

        # def draw(self):
        #     pygame.draw.rect(DISPLAY_SURFACE, (255, 0, 0), self.body)

if __name__ == '__main__':
    Ping().run_game_loop()