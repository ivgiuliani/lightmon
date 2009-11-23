import logging

class Job(object):
    """
    Provides a basic interface to the job classes
    """

    # provide logging facilities to jobs
    logger = logging.getLogger(__name__)

    def __init__(self, name, delay=5, repeat=False, *args, **kwargs):
        self.name = name
        self.delay = delay
        self.repeat = repeat

    def before(self):
        """
        A hook that is called before to run the job
        """
        return

    def run(self):
        raise NotImplementedError(
                "start() method not implemented for %s job" % self.name)

    def after(self):
        """
        A hook that is called after the job is ran
        """
        return

    def __str__(self):
        return self.name

    def __repr__(self):
        return u"<Job(name=%(name)s, delay=%(delay)s, repeat=%(repeat)s>" % {
            'name': self.name,
            'delay': self.delay,
            'repeat': 'True' if self.repeat else 'False',
        }

class DummyJob(Job):
    def run(self):
        print("dummy!")
