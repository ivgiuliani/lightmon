#!/usr/bin/env python

"""
A very simple testing facility over python-nose
"""

import os
import sys
import nose

from nose.plugins.allmodules import AllModules

def runtests(args):
    """
    Run the test framework
    """

    # we need to tell nose that all the modules under this directory are
    # proper tests even if they're name doesn't begin with 'test*'
    currpath = os.path.dirname(__file__)
    
    regression_tests = os.path.join(currpath, 'regression')

    argv = args[::]
    argv.extend(['--all-modules', regression_tests])

    return nose.run(argv=argv, plugins=[AllModules()])

if __name__ == '__main__':
    sys.exit(runtests(sys.argv))
