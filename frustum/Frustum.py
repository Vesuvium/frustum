# -*- coding: utf-8 -*-
import logging
from logging import config


class Frustum:

    levels = ['critical', 'error', 'warning', 'info', 'debug']

    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.config = {}
        self.events = {}

    def _level_from_verbosity(self, verbosity):
        if verbosity >= len(self.verbosities):
            verbosity = len(self.verbosities) - 1
        return getattr(logging, self.verbosities[verbosity].upper())

    def start_logger(self, name, level):
        """
        Starts the logger, enabling the root logger and the module-specific
        logger.
        If the root logger has been already started, basicConfig does nothing.
        """
        logging.basicConfig(level=level)
        dictionary = {
            'version': 1,
            'loggers': {
            }
        }
        dictionary['loggers'][name] = {'level': level}
        config.dictConfig(dictionary)
        self.logger = logging.getLogger(name)

    def set_logger(self, logger_name, level):
        """
        Sets the level of a third party logger
        """
        if 'loggers' not in self.config:
            self.config['loggers'] = {}
        self.config['loggers'][logger_name] = {'level': level}

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
