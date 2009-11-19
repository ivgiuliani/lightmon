class Job(object):
    "The base class for jobs"
    def __init__(self, name, delay=5, repeat=False, *args, **kwargs):
        self.name = name
        self.delay = delay
        self.repeat = repeat

    def run(self):
        raise NotImplementedError(
                "start() method not implemented for %s job" % self.name)

class DummyJob(Job):
    def run(self):
        print("dummy!")
