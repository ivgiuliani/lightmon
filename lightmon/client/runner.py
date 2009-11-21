import logging
import sys

from lightmon import config
from lightmon.client import client
from lightmon.jobs.basejob import DummyJob

def run():
    """
    Start the client timeline
    """

    logging.basicConfig(filename=config.LOGGING_FILE,
                        level=config.LOGGING_LEVEL)

    cl = client.Client()

    job = DummyJob("test job", delay=10, repeat=True)
    cl.addJob(job)

    try:
        cl.run()
    except KeyboardInterrupt:
        sys.stderr.write("goodbye Captain\n")
