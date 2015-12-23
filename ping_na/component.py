class Component:
    def __init__(self, name):
        self.name = name


class GameObject:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[component.name] = component

    def get_component(self, name):
        if name in self.components:
            return self.components[name]
        else:
            return None


class System:
    def __init__(self, clock):
        self.clock = clock
        self.objects = []

    def add_object(self, game_object):
        self.objects.append(game_object)

    def update(self):
        raise NotImplementedError
