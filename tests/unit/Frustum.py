# -*- coding: utf-8 -*-
import logging
from logging import config

from frustum import Frustum

from pytest import fixture, mark


@fixture
def frustum_mock(mocker):
    mocker.patch.object(Frustum, 'start_logger')


@fixture
def frustum(mocker):
    mocker.patch.object(Frustum, '__init__', return_value=None)
    frustum = Frustum()
    frustum.logger = mocker.MagicMock()
    frustum.events = {}
    return frustum


def test_frustum_init(frustum_mock):
    frustum = Frustum()
    frustum.start_logger.assert_called_with('frustum', 50)
    assert frustum.events == {}


@mark.parametrize('verbosity, level', [
    (0, logging.CRITICAL),
    (1, logging.ERROR),
    (2, logging.WARNING),
    (3, logging.INFO),
    (4, logging.DEBUG),
    (5, logging.DEBUG)
])
def test_frustum_init_verbosities(frustum_mock, verbosity, level):
    frustum = Frustum(verbosity=verbosity)
    frustum.start_logger.assert_called_with('frustum', level)


def test_frustum_init_output(frustum_mock):
    Frustum(output='mylog')


def test_frustum_init_name(frustum_mock):
    frustum = Frustum(name='test')
    frustum.start_logger.assert_called_with('test', 50)


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
    assert logging.getLogger('third_party').level == 20


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


def test_frustum_log_custom_event(mocker, frustum):
    frustum.log('my-event', 'world')
    frustum.logger.log.assert_called_with(logging.INFO, 'my-event')
