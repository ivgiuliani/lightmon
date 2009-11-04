"""
The client runs on the "timeline", that is a series of time-scheduled events.
Indeed, service checking classes are run on fixed time intervals as well as the
reports back to the server.
"""

import bisect
import logging
import sched
import threading
import time

from lightmon import config
from lightmon import jobs

class RunningJob(object):
    def __init__(self, job):
        self.job = job
        self.running_since = time.time()
        self.thread = None

    def start(self):
        thread = threading.Thread(target=self.job.run,
                                  name=self.job.name)
        self.thread = thread
        thread.start()


class Client(object):
    """
    The main client class. Here we handle the time scheduled events
    (included the lightmon process itself)
    """
    logger = logging.getLogger(__name__)

    def __init__(self, timefunc=time.time, delayfunc=time.sleep):
        self.scheduler = sched.scheduler(timefunc, delayfunc)

        self.jobs = []

        # a list of removed jobs indexes, so if possible reuse deleted idx
        # rather than let the job list grow indefinitely
        self.removed_jobs_idx = []

        # a list of jobs currently running (this list gets cleaned
        # up by the controller)
        self.runjobs = []

        # schedule the thread controlling system
        self.enter(config.SELF_CHECK_EVERY, 1, self.controller, ())

    def checkJobs(self):
        """
        Check the current status of the check jobs, if the same job is in
        execution twice (or more) kill the older job and report a failure
        """
        raise NotImplementedError

    def controller(self):
        "Controls the thread execution workflow"
        now = time.time()
        for runjob in self.runjobs:
            if (now - runjob.running_since) > MAX_CHECK_EXECUTION_TIME:
                # thread has exceeded execution time
                pass

        # reschedule ourselves
        self.scheduler.enter(config.SELF_CHECK_EVERY, 1, self.controller, ())

    def addJob(self, job):
        "Add a new check job"
        assert isinstance(job, jobs.Job)

        if self.removed_jobs_idx:
            # reuse idx if possible
            pos = self.removed_jobs_idx[0]
            self.jobs[pos] = job
            del self.removed_jobs_idx[0]
        else:
            # append a job to the job list, it's sequence number identifies it
            # (which happens to match to len(self.jobs) - 1 after an append)
            self.jobs.append(job)
            pos = len(self.jobs) - 1

        self.scheduler.enter(job.delay, 1, self.runJob, (pos, ))

    def runJob(self, jobnum):
        """
        Runs a job. This method gets called by the scheduler and might be
        killed if it takes too much time.
        """
        # first thing check if the job is still in the list (might have been
        # deleted while we were waiting for it)
        if not self.jobs[jobnum]:
            # in that case just ignore it
            return
            
        # TODO: run the real job
        self.logger.info("[run %s/%d]" % (self.jobs[jobnum].name, jobnum))
        self._runThread(jobnum)

        # reschedule the job if requested
        if self.jobs[jobnum].repeat:
            self.scheduler.enter(
                    self.jobs[jobnum].delay, # delay in seconds
                    1,                       # priority (unused)
                    self.runJob, (jobnum, )) # job's name
        else:
            # else delete the job from the job list
            self.deleteJob(jobnum)

    def deleteJob(self, jobnum):
        "Deletes a job from the job list"
        self.jobs[jobnum] = None
        bisect.insort(self.removed_jobs_idx, jobnum)

    def _runThread(self, jobnum):
        "Executes the ``jobnum`` thread"
        job = self.jobs[jobnum]

        runjob = RunningJob(job)
        runjob.start()

        self.runjobs.append(runjob)

    def run(self):
        "Run the client"
        self.scheduler.run()

