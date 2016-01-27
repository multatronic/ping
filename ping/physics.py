from ping.ecs import Component, System
import pygame


class PhysicsSystem(System):
    def __init__(self, board_width, board_height):
        super().__init__()
        self.board_width = board_width
        self.board_height = board_height
        self.checked_components = []

    def check_border_collisions(self, component):
        # check for border collisions
        border_hit = False
        if component.body.left < 0:
            component.body.left = 0
            border_hit = True
            if component.bounces:
                component.reverse_horizontal_direction()
        elif component.body.right > self.board_width:
            component.body.right = self.board_width
            border_hit = True
            if component.bounces:
                component.reverse_horizontal_direction()
        if component.body.top < 0:
            component.body.top = 0
            border_hit = True
            if component.bounces:
                component.reverse_vertical_direction()
        elif component.body.bottom > self.board_height:
            component.body.bottom = self.board_height
            border_hit = True
            if component.bounces:
                component.reverse_vertical_direction()
        if border_hit and not component.bounces:
            component.full_stop()

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

    def update(self, delta_time):
        self.checked_components.clear()
        for game_object in self.objects:
            component = game_object.get_component('physics')
            component.tick(delta_time)
            self.check_border_collisions(component)
            self.check_component_collisions(component)
            self.checked_components.append(component)


class PhysicsComponent(Component):
    'A physical object.'
    def __init__(self, position, width, height, direction=[0, 0], speed=0, bounces=False):
        'init object.'
        super().__init__('physics')
        half_width = width / 2
        half_height = height / 2
        self.bounces = bounces
        self.parent_object_position = position
        self.direction = direction
        self.speed = speed

        # keep float position to retain accuracy, and a rect for collision detection
        self.f_x = position[0]
        self.f_y = position[1]
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

    def sync_position(self, body_to_floats=False):
        if body_to_floats:
            self.f_x = self.body.centerx
            self.f_y = self.body.centery
        else:
            self.parent_object_position[:] = [int(self.f_x), int(self.f_y)]

    def full_stop(self):
        self.direction = [0, 0]
        self.sync_position(True) # sync body position to floats

    def tick(self, delta_time):
        # update float positions
        self.f_x += self.direction[0] * self.speed * delta_time
        self.f_y += self.direction[1] * self.speed * delta_time

        # convert to int for body Rect
        self.body.center = [int(self.f_x), int(self.f_y)]

        # sync rect center to parent object for use in other components
        self.sync_position()




