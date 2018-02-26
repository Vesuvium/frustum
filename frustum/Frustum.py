# -*- coding: utf-8 -*-
import logging


class Frustum:

    verbosities = ['critical', 'error', 'warning', 'info', 'debug']

    def __init__(self, *args, verbosity=0, name='frustum', output='stdout'):
        level = self._level_from_verbosity(verbosity)
        self.start_logger(name, level)
        self.add_handler(level, output)
        self.events = {}

    def _level_from_verbosity(self, verbosity):
        if verbosity >= len(self.verbosities):
            verbosity = len(self.verbosities) - 1
        return getattr(logging, self.verbosities[verbosity].upper())

    def start_logger(self, name, level):
        logging.basicConfig(level=level)
        self.logger = logging.getLogger(name)

    def add_handler(self, level, output):
        if output != 'stdout':
            handler = logging.FileHandler(output)
            handler.setLevel(level)
            self.logger.addHandler(handler)

    def register_event(self, event_name, event_level, message):
        """
        Registers an event so that it can be logged later.
        """
        self.events[event_name] = (event_level, message)

    def log(self, event, *args):
        message = event
        level = logging.INFO
        if event in self.events:
            level = getattr(logging, self.events[event][0].upper())
            message = self.events[event][1]
        self.logger.log(level, message.format(*args))
