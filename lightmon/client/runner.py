import sys

from lightmon.client import client

def run():
    """
    Start the client timeline
    """
    cl = client.Client()

    try:
        cl.run()
    except KeyboardInterrupt:
        sys.stderr.write("goodbye Captain\n")
