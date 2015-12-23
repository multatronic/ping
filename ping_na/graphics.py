from ping_na.component import Component, System
import pygame


class GraphicsSystem(System):
    def __init__(self, clock):
        super().__init__(clock)

    def update(self):
        for game_object in self.objects:
            game_object.get_component('graphics').draw()


class GraphicsComponent(Component):
    def __init__(self, body_type, display_surface, width, height, position, color=[255, 0, 0]):
        super().__init__('graphics')
        self.body_type = body_type
        self.display_surface = display_surface
        self.color = color
        self.shape = pygame.Rect(position[0] - width / 2, position[1] - height / 2, width, height)

    def update_position(self, position):
        self.shape.center = position

    def draw(self):
        if self.body_type == 'circle':
            pygame.draw.circle(self.display_surface, self.color, self.shape.center, self.shape.width // 2)
        if self.body_type == 'rectangle':
            pygame.draw.rect(self.display_surface, (255, 0, 0), self.shape)