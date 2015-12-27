from ping_na.component import Component, System
import pygame


class PhysicsSystem(System):
    def __init__(self, clock, board_width, board_height):
        super().__init__(clock)
        self.board_width = board_width
        self.board_height = board_height

    def update(self):
        for game_object in self.objects:
            component = game_object.get_component('physics')
            component.move()
            if component.body.left < 0:
                component.body.left = 0
            elif component.body.right > self.board_width:
                component.body.right = self.board_width
            if component.body.top < 0:
                component.body.top = 0
            elif component.body.bottom > self.board_height:
                component.body.bottom = self.board_height
            component.sync_position()


class PhysicsComponent(Component):
    'A physical object.'
    def __init__(self, position, width, height):
        'init object.'
        super().__init__('physics')
        half_width = width / 2
        half_height = height / 2
        self.parent_object_position = position
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

    def sync_position(self):
        self.parent_object_position[:] = self.body.center

    def move(self):
        self.body.move_ip(self.velocity[0], self.velocity[1])


