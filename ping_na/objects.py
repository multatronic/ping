from ping_na.ecs import *
from ping_na.input import *
from ping_na.physics import *
from ping_na.graphics import *
from pygame import KEYDOWN, K_LEFT, K_RIGHT


class Ball(GameObject):
    'A ball.'
    def __init__(self, position, display_surface):
        'init ball.'
        super().__init__(position)
        ball_speed = 100
        ball_radius = 9
        physics_margin = 1
        body_width = (ball_radius - physics_margin) * 2
        self.add_component(PhysicsComponent(self.position, body_width, body_width, [0, 0], 0, ball_speed, True))
        self.add_component(GraphicsComponent('circle', display_surface, body_width, body_width, self.position))
        self.add_component(InputComponent({
            KEYDOWN: {
                K_LEFT: lambda: self.kick_off_ball([-1, -0.5], ball_speed),
                K_RIGHT: lambda: self.kick_off_ball([1, 0.5], ball_speed)
            }
        }))

    def kick_off_ball(self, direction, ball_speed):
        ball_stationary = self.get_component('physics').get_direction() == [0, 0]
        if ball_stationary:
            self.get_component('physics').set_direction(direction)
            self.get_component('physics').speed = ball_speed


class Paddle(GameObject):
    'A paddle.'
    def __init__(self, position, display_surface):
        'init paddle'
        super().__init__(position)
        paddle_width = 60
        paddle_height = 20
        paddle_acceleration = 100
        paddle_max_speed = 300
        self.add_component(PhysicsComponent(self.position, paddle_width, paddle_height, [0, 0], paddle_acceleration,
                                            paddle_max_speed, False))
        self.add_component(GraphicsComponent('rectangle', display_surface, paddle_width, paddle_height, self.position))


class PlayerPaddle(Paddle):
    'A paddle.'
    def __init__(self, position, display_surface):
        'init paddle'
        super().__init__(position, display_surface)
        self.add_component(InputComponent({
            KEYDOWN: {
                K_LEFT: lambda: self.move_left(),
                K_RIGHT: lambda: self.move_right()
            }
        }))

    def move_left(self):
        self.get_component('physics').set_direction([-1, 0])

    def move_right(self):
        self.get_component('physics').set_direction([1, 0])