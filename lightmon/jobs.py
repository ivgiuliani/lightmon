class Job(object):
    "The base class for jobs"
    def __init__(self, name, delay=5, repeat=False, *args, **kwargs):
        self.name = name
        self.delay = delay
        self.repeat = repeat

    def run(self):
        raise NotImplementedError(
                "run() method not implemented for %s check" % self.name)

class DummyJob(Job):
    def run(self):
        print("dummy!")
