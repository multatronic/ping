from ping_na.component import Component, System
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_DOWN
import pygame


class InputSystem(System):
    def __init__(self, clock):
        super().__init__(clock)

    def update(self):
        for game_object in self.objects:
            for event in pygame.event.get():
                # quit the game if necessary
                if event.type == KEYDOWN:
                    # player_moved = False
                    # ball_stationary = BALL.get_velocity() == [0, 0]

                    if event.key == K_LEFT:
                        # do stuff
                        # player_moved = True
                        game_object.get_component('physics').set_velocity((-5, 0))
                    elif event.key == K_RIGHT:
                        # do stuff
                        # player_moved = True
                        game_object.get_component('physics').set_velocity((5, 0))
                    #
                    # if ball_stationary and player_moved:
                    #     ball_velocity = [PLAYER_PADDLE.get_velocity()[0], BALL_SPEED]
                    #     BALL.set_velocity(ball_velocity)


class InputComponent(Component):
    'An object which respons to player input.'
    def __init__(self):
        'init object.'
        super().__init__('input')
