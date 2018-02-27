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


def test_frustum_real_level_number(frustum):
    assert frustum.real_level(0) == logging.CRITICAL


def test_frustum_real_level_number_threshold(frustum):
    assert frustum.real_level(7) == logging.DEBUG


def test_start_logger(patch, frustum):
    patch.object(logging, 'basicConfig')
    patch.object(config, 'dictConfig')
    patch.object(Frustum, 'set_logger')
    frustum.start_logger()
    logging.basicConfig.assert_called_with(level=frustum.level)
    Frustum.set_logger.assert_called_with(frustum.name, frustum.level)
    config.dictConfig.assert_called_with(frustum.config)
    assert frustum.logger == logging.getLogger(frustum.name)


def test_frustum_set_logger(patch, frustum):
    patch.object(frustum, 'real_level', return_value=10)
    frustum.set_logger('third_party', 'debug')
    frustum.real_level.assert_called_with('debug')
    assert frustum.config['loggers']['third_party'] == {'level': 10}


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


def test_frustum_log_custom_event(frustum):
    frustum.log('my-event', 'world')
    frustum.logger.log.assert_called_with(logging.INFO, 'my-event')
