from ping_na.component import *
from ping_na.input import *
from ping_na.physics import *
from ping_na.graphics import *
from pygame import KEYDOWN, K_LEFT, K_RIGHT


class Ball(GameObject):
    'A ball.'
    def __init__(self, position, display_surface):
        'init ball.'
        super().__init__(position)
        ball_speed = 6
        ball_radius = 9
        physics_margin = 1
        body_width = (ball_radius - physics_margin) * 2
        self.add_component(PhysicsComponent(self.position, body_width, body_width, True))
        self.add_component(GraphicsComponent('circle', display_surface, body_width, body_width, self.position))
        self.add_component(InputComponent({
            KEYDOWN: {
                K_LEFT: lambda: self.kick_off_ball([-5, ball_speed]),
                K_RIGHT: lambda: self.kick_off_ball([5, ball_speed])
            }
        }))

    def kick_off_ball(self, velocity):
        ball_stationary = self.get_component('physics').get_velocity() == [0, 0]
        if ball_stationary:
            self.get_component('physics').set_velocity(velocity)


class Paddle(GameObject):
    'A paddle.'
    def __init__(self, position, display_surface):
        'init paddle'
        super().__init__(position)
        paddle_width = 60
        paddle_height = 20
        self.add_component(PhysicsComponent(self.position, paddle_width, paddle_height))
        self.add_component(GraphicsComponent('rectangle', display_surface, paddle_width, paddle_height, self.position))
