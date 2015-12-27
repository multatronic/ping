from ping_na.component import *
from ping_na.physics import *
from ping_na.graphics import *


class Ball(GameObject):
    'A ball.'
    def __init__(self, position, display_surface):
        'init ball.'
        super().__init__(position)
        ball_radius = 9
        physics_margin = 1
        body_width = (ball_radius - physics_margin) * 2
        self.add_component(PhysicsComponent(self.position, body_width, body_width))
        self.add_component(GraphicsComponent('circle', display_surface, body_width, body_width, self.position))

    # def check_collision(self, other_rect):
    #     if self.body.colliderect(other_rect):
    #         delta = [other_rect.centerx - self.body.centerx, other_rect.centery - self.body.centery]
    #
    #         if delta[0] <= PADDLE_WIDTH:
    #             self.reverse_horizontal_velocity()
    #         elif delta[1] <= PADDLE_HEIGHT:
    #             self.reverse_vertical_velocity()
    #         else:
    #             self.reverse_horizontal_velocity()
    #             self.reverse_vertical_velocity()
    #     else:
    #         return None
    #
    # def move(self):
    #     super().move()
    #     # bounce the ball if necessary
    #     if self.body.left == 0 or self.body.right == BOARD_WIDTH:
    #         self.reverse_horizontal_velocity()
    #     if self.body.top == 0 or self.body.bottom == BOARD_HEIGHT:
    #         self.reverse_vertical_velocity()

    # def draw(self):
    #     global DISPLAY_SURFACE
    #     pygame.draw.circle(DISPLAY_SURFACE, (255, 0, 0), self.body.center, BALL_RADIUS)
        # super().draw()


class Paddle(GameObject):
    'A paddle.'
    def __init__(self, position, display_surface):
        'init paddle'
        super().__init__(position)
        paddle_width = 60
        paddle_height = 20
        self.add_component(PhysicsComponent(self.position, paddle_width, paddle_height))
        self.add_component(GraphicsComponent('rectangle', display_surface, paddle_width, paddle_height, self.position))

    # def draw(self):
    #     pygame.draw.rect(DISPLAY_SURFACE, (255, 0, 0), self.body)