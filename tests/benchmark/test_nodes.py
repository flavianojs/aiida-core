# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida-core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
# pylint: disable=unused-argument
"""Benchmark tests for nodes."""
import pytest

from aiida.orm import Data


@pytest.mark.usefixtures('clear_database_before_test')
@pytest.mark.benchmark(group='node', min_rounds=100)
def test_store(benchmark):

    def _store():
        return Data().store()

    result = benchmark(_store)
    assert result.pk > 0
