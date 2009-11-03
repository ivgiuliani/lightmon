"""
The client runs on the "timeline", that is a series of time-scheduled events.
Indeed, service checking classes are run on fixed time intervals as well as the
reports back to the server.
"""

import sched
import time

from lightmon import config

class Client(object):
    """
    The main client class. Here we handle the time scheduled events
    (included the lightmon process itself)
    """
    def __init__(self, timefunc=time.time, delayfunc=time.sleep):
        # schedule the lightmon controller process as every ``SELF_CHECK_EVERY``
        self.scheduler = sched.scheduler(timefunc, delayfunc)
        self.scheduler.enter(config.SELF_CHECK_EVERY, 1, self.controller, ())

    def controller(self):
        """
        Control if there are stale threads that needs to be killed
        """
        # reschedule ourselves every SELF_CHECK_EVERY seconds
        self.checkJobs()
        self.scheduler.enter(config.SELF_CHECK_EVERY, 1, self.controller, ())

    def checkJobs(self):
        """
        Check the current status of the check jobs, if the same job is in
        execution twice (or more) kill the older job and report a failure
        """
        raise NotImplementedError

    def addJob(self):
        "Add a new check job"
        raise NotImplementedError

    def run(self):
        "Run the client"
        self.scheduler.run()

