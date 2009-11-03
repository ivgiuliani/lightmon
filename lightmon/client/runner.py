"""
The client runs on the "timeline", that is a series of time-scheduled events.
Indeed, service checking classes are run on fixed time intervals as well as the
reports back to the server.
"""

import sched
import sys
import time

from lightmon import config

class Client(object):
    """
    The main client class. Here we handle the time scheduled events
    (included the lightmon process itself)
    """
    def __init__(self):
        # schedule the lightmon process as every ``SELF_CHECK_EVERY``
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.scheduler.enter(config.SELF_CHECK_EVERY, 1, self.controller, ())

    def controller(self):
        """
        Control if there are stale threads that needs to be killed
        """
        print 'not yet: controller'
        # reschedule ourselves every SELF_CHECK_EVERY seconds
        self.scheduler.enter(config.SELF_CHECK_EVERY, 1, self.controller, ())

    def run(self):
        self.scheduler.run()

def run():
    """
    Start the client timeline
    """
    client = Client()

    try:
        client.run()
    except KeyboardInterrupt:
        sys.stderr.write("goodbye Captain\n")
