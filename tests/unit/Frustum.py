# -*- coding: utf-8 -*-
import logging
from logging import config

from frustum import Frustum

from pytest import fixture, mark


@fixture
def frustum(mocker):
    frustum = Frustum('frustum', 'debug')
    frustum.logger = mocker.MagicMock()
    return frustum


def test_frustum_init(frustum):
    assert frustum.name == 'frustum'
    assert frustum.level == 'debug'
    assert frustum.events == {}
    assert frustum.config == {'version': 1}


@mark.parametrize('level, expected', [
    ('critical', logging.CRITICAL),
    ('error', logging.ERROR),
    ('warning', logging.WARNING),
    ('info', logging.INFO),
    ('debug', logging.DEBUG),
])
def test_frustum_real_level(frustum, level, expected):
    assert frustum.real_level(level) == expected


def test_start_logger(patch, frustum):
    patch.object(logging, 'basicConfig')
    patch.object(config, 'dictConfig')
    patch.object(Frustum, 'set_logger')
    patch.object(Frustum, 'real_level')
    frustum.start_logger()
    Frustum.real_level.assert_called_with(frustum.level)
    logging.basicConfig.assert_called_with(level=frustum.real_level())
    Frustum.set_logger.assert_called_with(frustum.name, frustum.real_level())
    config.dictConfig.assert_called_with(frustum.config)
    assert frustum.logger == logging.getLogger(frustum.name)


def test_frustum_set_formatter(frustum):
    frustum.set_formatter('simple', 'string')
    assert frustum.config['formatters']['simple'] == {'format': 'string'}


def test_frustum_set_logger(patch, frustum):
    patch.object(frustum, 'real_level', return_value=10)
    frustum.set_logger('third_party', 'debug')
    frustum.real_level.assert_called_with('debug')
    assert frustum.config['loggers']['third_party'] == {'level': 10}


def test_frustum_set_logger_handler(patch, frustum):
    patch.object(frustum, 'real_level', return_value=10)
    frustum.set_logger('module', 'debug', handler='console')
    assert frustum.config['loggers']['module']['handlers'] == ['console']


def test_frustum_add_handler(frustum):
    frustum.add_handler('console', 'stream')
    expected = {'class': 'logging.StreamHandler'}
    assert frustum.config['handlers']['console'] == expected


def test_frustum_register_event(frustum):
    message = 'message: {} happened!'
    frustum.register_event('event', 'level', message)
    assert frustum.events['event'] == ('level', message)


def test_frustum_log(frustum):
    frustum.events = {'my-event': ('info', 'hello {}')}
    frustum.log('my-event', 'world')
    frustum.logger.log.assert_called_with(logging.INFO, 'hello world')


def test_frustum_log_custom_event(patch, frustum):
    patch.object(Frustum, 'real_level', return_value='level')
    frustum.log('level', 'message in {}', 'my log')
    Frustum.real_level.assert_called_with('level')
    frustum.logger.log.assert_called_with('level', 'message in my log')
