"""
The client runs on the "timeline", that is a series of time-scheduled events.
Indeed, service checking classes are run on fixed time intervals as well as the
reports back to the server.
"""

import bisect
import logging
import sched
import time

from lightmon import config
from lightmon import jobs

class RunningJob(object):
    "A job that is running in memory"

    def __init__(self, job):
        assert isinstance(job, jobs.Job)

        self.job = job
        self.running_since = time.time()

        # result is set as None at the beginning but everything different
        # (which by the way must be a JobResult object) is interpreted as
        # valid result
        self.result = None

    def start(self):
        """
        Start a scheduled event
        """
        self.job.before()
        self.result = self.job.run()
        self.job.after()

    def getResult(self):
        """
        Retrieve the job result once the job is done
        """
        return self.result


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
            
        # run the real job
        self.logger.info("run [%s/%d]" % (self.jobs[jobnum], jobnum))
        runjob = RunningJob(self.jobs[jobnum])
        runjob.start()

        # TODO: process the result

        # reschedule the job if requested
        if self.jobs[jobnum].repeat:
            self.scheduler.enter(
                    self.jobs[jobnum].delay, # delay in seconds
                    1,                       # priority (unused)
                    self.runJob, (jobnum, )) # job's name
        else:
            # else delete the job from the job list
            self.deleteJob(jobnum)

        # acquire the result
        result = runjob.getResult()
        self.logger.info("job [%s/%d] returned %s" % (self.jobs[jobnum].name,
                                                      jobnum,
                                                      result))

    def deleteJob(self, jobnum):
        "Deletes a job from the job list"
        self.jobs[jobnum] = None
        bisect.insort(self.removed_jobs_idx, jobnum)

    def run(self):
        "Run the client"
        self.scheduler.run()

