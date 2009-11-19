class Job(object):
    "The base class for jobs"
    def __init__(self, name, delay=5, repeat=False, *args, **kwargs):
        self.name = name
        self.delay = delay
        self.repeat = repeat

    def run(self):
        raise NotImplementedError(
                "start() method not implemented for %s job" % self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return u"<Job(name=%(name)s, delay=%(delay)s, repeat=%(repeat)s>" % {
            'name': self.name,
            'delay': self.delay,
            'repeat': 'true' if self.repeat else 'false',
        }

class DummyJob(Job):
    def run(self):
        print("dummy!")
