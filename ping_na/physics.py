from ping_na.component import Component, System
import pygame


class PhysicsSystem(System):
    def __init__(self, clock, board_width, board_height):
        super().__init__(clock)
        self.board_width = board_width
        self.board_height = board_height
        self.checked_components = []

    def check_border_collisions(self, component):
        # check for border collisions
        if component.body.left < 0:
            component.body.left = 0
            if component.bounces:
                component.reverse_horizontal_direction()
        elif component.body.right > self.board_width:
            component.body.right = self.board_width
            if component.bounces:
                component.reverse_horizontal_direction()
        if component.body.top < 0:
            component.body.top = 0
            if component.bounces:
                component.reverse_vertical_direction()
        elif component.body.bottom > self.board_height:
            component.body.bottom = self.board_height
            if component.bounces:
                component.reverse_vertical_direction()

    def check_component_collisions(self, component):
        for game_object in self.objects:
            current_component = game_object.get_component('physics')
            if current_component not in self.checked_components and current_component != component \
                    and self.are_rects_colliding(component.body, current_component.body):
                    if component.bounces:
                        component.reverse_direction()
                    if current_component.bounces:
                        current_component.reverse_vertical_direction()

    def are_rects_colliding(self, from_rect, to_rect):
        # use pygame builtin
        if from_rect.colliderect(to_rect):
            return True
        # check other cases
        in_horizontal_margin = False
        in_vertical_margin = False
        if (to_rect.left <= from_rect.left <= to_rect.right) or (to_rect.left <= from_rect.right <= to_rect.right):
            in_horizontal_margin = True
        if (to_rect.top <= from_rect.top <= to_rect.bottom) or (to_rect.top <= from_rect.bottom <= to_rect.bottom):
            in_vertical_margin = True
        return in_horizontal_margin and in_vertical_margin


    def update(self):
        self.checked_components.clear()
        for game_object in self.objects:
            component = game_object.get_component('physics')
            component.accelerate()
            component.move()
            self.check_border_collisions(component)
            self.check_component_collisions(component)
            component.sync_position()
            self.checked_components.append(component)


class PhysicsComponent(Component):
    'A physical object.'
    def __init__(self, position, width, height, direction=[0, 0], acceleration=None, max_speed=1, bounces=False):
        'init object.'
        super().__init__('physics')
        half_width = width / 2
        half_height = height / 2
        self.bounces = bounces
        self.parent_object_position = position
        self.direction = direction
        self.acceleration = acceleration
        self.speed = 0
        self.max_speed = max_speed
        if self.acceleration is None:
            self.speed = max_speed
        # self.velocity = [0, 0]
        self.body = pygame.Rect((position[0] - half_width), (position[1] - half_height), width, height)

    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def reverse_direction(self):
        self.reverse_horizontal_direction()
        self.reverse_vertical_direction()

    def reverse_horizontal_direction(self):
        self.direction[0] *= -1

    def reverse_vertical_direction(self):
        self.direction[1] *= -1

    def sync_position(self):
        self.parent_object_position[:] = list(self.body.center)

    def decelerate(self):
        if self.acceleration is not None:
            self.speed -= self.acceleration
            if self.speed <= 0:
                self.speed = 0

    def accelerate(self):
        if self.acceleration is not None:
            self.speed += self.acceleration
            if self.speed >= self.max_speed:
                self.speed = self.max_speed

    def move(self):
        self.body.move_ip(self.direction[0] * self.speed, self.direction[1] * self.speed)


