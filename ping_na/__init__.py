__author__ = 'revok'

import pygame, logging
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_DOWN

LAST_UPDATE_TIME = 0
GAME_RUNNING = True
DISPLAY_SURFACE = None
CLOCK = None
FPS = 60
HORIZONTAL_SPEED = 50
PLAYER_PADDLE = None
ENEMY_PADDLE = None
BALL = None
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 20
BOARD_WIDTH = 800
BOARD_HEIGHT = 600
BALL_RADIUS = 9
BALL_SPEED = 3
PLAYER_START_POS = [BOARD_WIDTH / 2, 20]
ENEMY_START_POS = [BOARD_WIDTH / 2, BOARD_HEIGHT - 20]







def main():
    'Main game loop'
    global DISPLAY_SURFACE, CLOCK, ENEMY_PADDLE, PLAYER_PADDLE, BALL

    PLAYER_PADDLE = Paddle(PLAYER_START_POS)
    ENEMY_PADDLE = Paddle(ENEMY_START_POS)
    BALL = Ball((BOARD_WIDTH / 2, BOARD_HEIGHT / 2))

    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    DISPLAY_SURFACE = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    CLOCK = pygame.time.Clock()

    while GAME_RUNNING:
        CLOCK.tick(FPS)
        handle_input()
        draw_board()
        pygame.display.update()


def handle_input():
    global GAME_RUNNING, HORIZONTAL_SPEED
    for event in pygame.event.get():
        # quit the game if necessary
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            GAME_RUNNING = False
        # else handle input
        elif event.type == KEYDOWN:
            player_moved = False
            ball_stationary = BALL.get_velocity() == [0, 0]

            if event.key == K_LEFT:
                # do stuff
                player_moved = True
                PLAYER_PADDLE.set_velocity((-5, 0))
            elif event.key == K_RIGHT:
                # do stuff
                player_moved = True
                PLAYER_PADDLE.set_velocity((5, 0))

            if ball_stationary and player_moved:
                ball_velocity = [PLAYER_PADDLE.get_velocity()[0], BALL_SPEED]
                BALL.set_velocity(ball_velocity)



def draw_board():
    DISPLAY_SURFACE.fill((0, 0, 0))
    PLAYER_PADDLE.move()
    PLAYER_PADDLE.draw()
    ENEMY_PADDLE.draw()
    BALL.move()
    BALL.check_collision(PLAYER_PADDLE.body)
    BALL.check_collision(ENEMY_PADDLE.body)
    BALL.draw()


class PhysicalObject:
    'A physical object.'
    def __init__(self, position, width, height):
        'init object.'
        half_width = width / 2
        half_height = height / 2
        self.velocity = [0, 0]
        self.body = pygame.Rect((position[0] - half_width), (position[1] - half_height), width, height)

    def set_velocity(self, velocity):
        self.velocity = velocity
    def get_velocity(self):
        return self.velocity

    def reverse_velocity(self):
        self.reverse_horizontal_velocity()
        self.reverse_vertical_velocity()

    def reverse_horizontal_velocity(self):
        self.velocity[0] *= -1

    def reverse_vertical_velocity(self):
        self.velocity[1] *= -1

    def draw(self):
        pygame.draw.rect(DISPLAY_SURFACE, (0, 255, 0), self.body, 3)

    def move(self):
        self.body.move_ip(self.velocity[0], self.velocity[1])
        if self.body.left < 0:
            self.body.left = 0
        elif self.body.right > BOARD_WIDTH:
            self.body.right = BOARD_WIDTH
        if self.body.top < 0:
            self.body.top = 0
        elif self.body.bottom > BOARD_HEIGHT:
            self.body.bottom = BOARD_HEIGHT

class Ball(PhysicalObject):
    'A ball.'
    def __init__(self, position):
        'init ball.'
        physics_margin = 1
        body_width = (BALL_RADIUS - physics_margin) * 2
        super().__init__(position, body_width, body_width)

    def check_collision(self, other_rect):
        if self.body.colliderect(other_rect):
            self.reverse_vertical_velocity()
        else:
            return None

    def move(self):
        super().move()
        # bounce the ball if necessary
        if self.body.left == 0 or self.body.right == BOARD_WIDTH:
            self.reverse_horizontal_velocity()
        if self.body.top == 0 or self.body.bottom == BOARD_HEIGHT:
            self.reverse_vertical_velocity()

    def draw(self):
        global DISPLAY_SURFACE
        pygame.draw.circle(DISPLAY_SURFACE, (255, 0, 0), self.body.center, BALL_RADIUS)
        # super().draw()


class Paddle(PhysicalObject):
    'A paddle.'
    def __init__(self, position):
        'init paddle'
        super().__init__(position, PADDLE_WIDTH, PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(DISPLAY_SURFACE, (255, 0, 0), self.body)

if __name__ == '__main__':
    main()



