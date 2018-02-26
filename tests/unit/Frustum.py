# -*- coding: utf-8 -*-
import logging

from frustum import Frustum

from pytest import fixture, mark


@fixture
def frustum_mock(mocker):
    mocker.patch.object(Frustum, 'start_logger')
    mocker.patch.object(Frustum, 'add_handler')


@fixture
def frustum(mocker):
    mocker.patch.object(logging, 'getLogger')
    return Frustum()


def test_init(frustum_mock):
    frustum = Frustum()
    frustum.start_logger.assert_called_with('frustum', 50)
    frustum.add_handler.assert_called_with(50, 'stdout')
    assert frustum.events == {}


@mark.parametrize('verbosity, level', [
    (0, logging.CRITICAL),
    (1, logging.ERROR),
    (2, logging.WARNING),
    (3, logging.INFO),
    (4, logging.DEBUG),
    (5, logging.DEBUG)
])
def test_init_verbosities(frustum_mock, verbosity, level):
    frustum = Frustum(verbosity=verbosity)
    frustum.start_logger.assert_called_with('frustum', level)
    frustum.add_handler.assert_called_with(level, 'stdout')


def test_logger_output(frustum_mock):
    frustum = Frustum(output='mylog')
    frustum.add_handler.assert_called_with(50, 'mylog')


def test_start_logger(mocker):
    mocker.patch.object(Frustum, '__init__', return_value=None)
    frustum = Frustum()
    frustum.start_logger('name', 1)
    assert frustum.logger == logging.getLogger('name')


def test_add_handler(mocker):
    mocker.patch.object(logging, 'FileHandler')
    mocker.patch.object(logging, 'getLogger')
    frustum = Frustum(output='mylog')
    logging.FileHandler.assert_called_with('mylog')
    logging.FileHandler().setLevel.assert_called_with(logging.CRITICAL)
    logging.getLogger().addHandler.assert_called_with(logging.FileHandler())
    assert isinstance(frustum, Frustum)


def test_frustum_register_event(frustum):
    message = 'message: {} happened!'
    frustum.register_event('event', 'level', message)
    assert frustum.events['event'] == ('level', message)


def test_log(frustum):
    frustum.events = {'my-event': ('info', 'hello {}')}
    frustum.log('my-event', 'world')
    frustum.logger.log.assert_called_with(logging.INFO, 'hello world')


def test_log_custom_event(frustum):
    frustum.events = {}
    frustum.log('my-event', 'world')
    frustum.logger.log.assert_called_with(logging.INFO, 'my-event')
