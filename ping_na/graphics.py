from ping_na.ecs import Component, System
import pygame


class GraphicsSystem(System):
    def __init__(self):
        super().__init__()

    def update(self, delta_time):
        for game_object in self.objects:
            game_object.get_component('graphics').draw()


class GraphicsComponent(Component):
    def __init__(self, body_type, display_surface, width, height, position, color=[255, 0, 0]):
        super().__init__('graphics')
        self.body_type = body_type
        self.display_surface = display_surface
        self.color = color
        self.width = width
        self.height = height
        self.parent_object_position = position

    def draw(self):
        # self.logger.info('drawing at position %s', self.parent_object_position)
        if self.body_type == 'circle':
            pygame.draw.circle(self.display_surface, self.color, self.parent_object_position, self.width // 2)
        if self.body_type == 'rectangle':
            pygame.draw.rect(self.display_surface, (255, 0, 0), \
                             pygame.Rect(self.parent_object_position[0] - self.width // 2, \
                                                                            self.parent_object_position[1] - self.height // 2, \
                                                                            self.width, self.height))
