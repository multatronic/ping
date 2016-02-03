from ping.ecs import Component, System
import pygame


class InputSystem(System):
    def __init__(self):
        super().__init__()
        self.keyboard_input_handlers = {}
        self.generic_handlers = {}

    def add_keyboard_input_handler(self, event_type, key, handler):
        if event_type not in self.keyboard_input_handlers:
            self.keyboard_input_handlers[event_type] = {}
        if key not in self.keyboard_input_handlers[event_type]:
            self.keyboard_input_handlers[event_type][key] = []
        self.keyboard_input_handlers[event_type][key].append(handler)

    def add_generic_event_handler(self, event_type, handler):
        if event_type not in self.generic_handlers:
            self.generic_handlers[event_type] = []
        self.generic_handlers[event_type].append(handler)

    def add_object(self, game_object):
        super().add_object(game_object)
        for event_type in game_object.get_component('input').input_handlers:
            for key, handler in game_object.get_component('input').input_handlers[event_type].items():
                self.add_keyboard_input_handler(event_type, key, handler)

    def update(self, delta_time):
        for event in pygame.event.get():
            if event.type in self.keyboard_input_handlers and \
                            event.key in self.keyboard_input_handlers[event.type]:
                for handler in self.keyboard_input_handlers[event.type][event.key]:
                    handler()
            if event.type in self.generic_handlers:
                for handler in self.generic_handlers[event.type]:
                    handler(event)


class InputComponent(Component):
    'An object which respons to player input.'
    def __init__(self, input_handlers):
        'init object.'
        super().__init__('input')
        self.input_handlers = input_handlers
