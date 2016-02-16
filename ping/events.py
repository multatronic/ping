from ping.ecs import Component, System
import pygame


class EventBus:
    def __init__(self):
        self.handlers = {}

    def add_event_handler(self, event_type, handler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def tick(self):
        for event in pygame.event.get():
            if event.type in self.handlers:
                for handler in self.handlers[event.type]:
                    handler(event)
