import logging, pygame

class Component:
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(__name__)


class GameObject:
    def __init__(self, position = [0, 0]):
        self.position = position
        self.components = {}

    def add_component(self, component):
        self.components[component.name] = component

    def get_component(self, name):
        if name in self.components:
            return self.components[name]
        else:
            return None


class System:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.objects = []

    def add_object(self, game_object):
        self.objects.append(game_object)

    def remove_object(self, game_object):
        if game_object in self.objects:
            self.objects.remove(game_object)

    def update(self, delta_time):
        raise NotImplementedError
