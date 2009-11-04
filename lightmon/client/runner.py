import sys

from lightmon.client import client
from lightmon.jobs import Job

def run():
    """
    Start the client timeline
    """
    cl = client.Client()

    job = Job("test job", delay=10, repeat=True)
    cl.addJob(job)

    try:
        cl.run()
    except KeyboardInterrupt:
        sys.stderr.write("goodbye Captain\n")
