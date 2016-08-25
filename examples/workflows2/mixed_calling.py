#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-

__copyright__ = u"Copyright (c), This file is part of the AiiDA platform. For further information please visit http://www.aiida.net/.. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.6.0"
__authors__ = "The AiiDA team."

from aiida.backends.utils import load_dbenv, is_dbenv_loaded

if not is_dbenv_loaded():
    load_dbenv()

import time
from aiida.orm.data.simple import make_int
from aiida.workflows2.run import async, run
from aiida.workflows2.wf import wf
from aiida.workflows2.fragmented_wf import FragmentedWorkfunction,\
    ResultToContext


@wf
def f1(inp=None):
    p2 = async(long_running, a=inp)
    a = 1  # Do some work...
    r2 = p2.result()
    print("a={}".format(a))
    print("r2={}".format(r2))

    return {'r1': r2['r2']}


@wf
def long_running(a):
    time.sleep(2)
    return {'r2': a}


class F1(FragmentedWorkfunction):
    @classmethod
    def _define(cls, spec):
        spec.dynamic_input()
        spec.dynamic_output()
        spec.outline(cls.s1, cls.s2)

    def s1(self, ctx):
        p2 = self.submit(LongRunning, inputs={'a': self.inputs.inp})
        ctx.a = 1 #  Do some work...
        return ResultToContext(r2=p2)

    def s2(self, ctx):
        print("a={}".format(ctx.a))
        print("r2={}".format(ctx.r2))

        self.out("r1", ctx.r2['r2'])


class LongRunning(FragmentedWorkfunction):
    @classmethod
    def _define(cls, spec):
        spec.dynamic_input()
        spec.dynamic_output()
        spec.outline(cls.s1)

    def s1(self, ctx):
        time.sleep(2)
        self.out("r2", self.inputs.a)


class F1WaitFor(FragmentedWorkfunction):
    @classmethod
    def _define(cls, spec):
        spec.dynamic_input()
        spec.dynamic_output()
        spec.outline(cls.s1, cls.s2)

    def s1(self, ctx):
        p2 = async(long_running, a=self.inputs.inp)
        ctx.a = 1
        ctx.r2 = p2.result()

    def s2(self, ctx):
        print("a={}".format(ctx.a))
        print("r2={}".format(ctx.r2))

        self.out("r1", ctx.r2['r2'])


if __name__ == '__main__':
    five = make_int(5)

    r1 = f1(five)
    run(F1, inp=five)
    R1 = run(F1WaitFor, inp=five)['r1']

