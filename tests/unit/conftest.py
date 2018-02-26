# -*- coding: utf-8 -*-
from pytest import fixture


@fixture
def magic(mocker):
    return mocker.MagicMock


@fixture
def patch(mocker):
    return mocker.patch
