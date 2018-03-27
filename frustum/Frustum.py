# -*- coding: utf-8 -*-
import logging
from logging import config


class Frustum:

    levels = ['critical', 'error', 'warning', 'info', 'debug']

    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.events = {}
        self.config = {'version': 1}

    def real_level(self, level):
        """
        Finds the real level from a string level
        """
        return getattr(logging, level.upper())

    def start_logger(self):
        """
        Enables the root logger and configures extra loggers.
        """
        level = self.real_level(self.level)
        logging.basicConfig(level=level)
        self.set_logger(self.name, self.level)
        config.dictConfig(self.config)
        self.logger = logging.getLogger(self.name)

    def set_formatter(self, formatter_name, string_format):
        if 'formatters' not in self.config:
            self.config['formatters'] = {}
        self.config['formatters'][formatter_name] = {'format': string_format}

    def set_logger(self, logger_name, level, handler=None):
        """
        Sets the level of a logger
        """
        if 'loggers' not in self.config:
            self.config['loggers'] = {}
        real_level = self.real_level(level)
        self.config['loggers'][logger_name] = {'level': real_level}
        if handler:
            self.config['loggers'][logger_name]['handlers'] = [handler]

    def add_handler(self, handler_name, handler_type):
        handler_classes = {'stream': 'logging.StreamHandler'}
        handler_class = handler_classes[handler_type]
        if 'handlers' not in self.config:
            self.config['handlers'] = {}
        self.config['handlers'][handler_name] = {'class': handler_class}

    def register_event(self, event_name, event_level, message):
        """
        Registers an event so that it can be logged later.
        """
        self.events[event_name] = (event_level, message)

    def log(self, event, *args):
        if event in self.events:
            level = getattr(logging, self.events[event][0].upper())
            message = self.events[event][1]
            self.logger.log(level, message.format(*args))
            return None
        args = list(args)
        level = self.real_level(event)
        message = args.pop(0)
        self.logger.log(level, message.format(*args))
