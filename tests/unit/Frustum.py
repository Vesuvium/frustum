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
    assert frustum.config == {}


def test_start_logger(mocker, frustum):
    mocker.patch.object(logging, 'Logger')
    mocker.patch.object(logging, 'basicConfig')
    mocker.patch.object(config, 'dictConfig')
    frustum.start_logger('name', 10)
    logging.basicConfig.assert_called_with(level=10)
    dictionary = {'version': 1, 'loggers': {'name': {'level': 10}}}
    config.dictConfig.assert_called_with(dictionary)
    assert frustum.logger == logging.getLogger('name')


def test_frustum_set_logger(mocker, frustum):
    frustum.set_logger('third_party', 20)
    assert frustum.config['loggers']['third_party'] == {'level': 20}


def test_frustum_add_handler(frustum):
    frustum.add_handler(1, 'stdout')


def test_frustum_add_handler_else(mocker, frustum):
    mocker.patch.object(logging, 'FileHandler')
    frustum.add_handler(1, 'else')
    logging.FileHandler.assert_called_with('else')
    logging.FileHandler().setLevel.assert_called_with(1)
    frustum.logger.addHandler.assert_called_with(logging.FileHandler())


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
