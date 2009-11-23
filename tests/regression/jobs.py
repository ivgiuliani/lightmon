# vim: set fileencoding=utf-8 :

import unittest

from lightmon.jobs import basejob

class SimpleJob(basejob.Job):
    """
    A simple test job that will be used in tests
    """
    pass


class TestJob(unittest.TestCase):
    def testRepr(self):
        "Test that repr() always returns a consistent format"

        # default behavior
        job = SimpleJob(name="simple job")
        self.assertEqual(repr(job), "<Job(name=simple job, delay=5, repeat=False>")

        # different parameters
        job = SimpleJob(name=u"simple job", delay=10, repeat=False)
        self.assertEqual(repr(job), "<Job(name=simple job, delay=10, repeat=False>")

        job = SimpleJob(name=u"simple job", delay=1, repeat=False)
        self.assertEqual(repr(job), "<Job(name=simple job, delay=1, repeat=False>")

        job = SimpleJob(name=u"simple job", delay=10, repeat=True)
        self.assertEqual(repr(job), "<Job(name=simple job, delay=10, repeat=True>")

        job = SimpleJob(name=u"simple job", delay=10)
        self.assertEqual(repr(job), "<Job(name=simple job, delay=10, repeat=False>")

        job = SimpleJob(name=u"simple job", repeat=True)
        self.assertEqual(repr(job), "<Job(name=simple job, delay=5, repeat=True>")

