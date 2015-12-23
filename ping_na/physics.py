from ping_na.component import Component, System
import pygame


class PhysicsSystem(System):
    def __init__(self, clock):
        super().__init__(clock)

    def update(self):
        self.move_objects()

    def move_objects(self):
        for game_object in self.objects:
            game_object.get_component('physics').move()


class PhysicsComponent(Component):
    'A physical object.'
    def __init__(self, position, width, height):
        'init object.'
        super().__init__('physics')
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

    # def draw(self):
    #     pygame.draw.rect(DISPLAY_SURFACE, (0, 255, 0), self.body, 3)

    def move(self):
        self.body.move_ip(self.velocity[0], self.velocity[1])
        # if self.body.left < 0:
        #     self.body.left = 0
        # elif self.body.right > BOARD_WIDTH:
        #     self.body.right = BOARD_WIDTH
        # if self.body.top < 0:
        #     self.body.top = 0
        # elif self.body.bottom > BOARD_HEIGHT:
        #     self.body.bottom = BOARD_HEIGHT

