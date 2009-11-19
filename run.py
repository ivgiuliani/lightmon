#!/usr/bin/env python
"""
Run script
"""

import sys
import getopt
import logging

from lightmon import config

def args_evaluation(opts):
    """
    Checks that the arguments are valid
    """

    for name, value in opts:
        if name == "--client":
            config.CLIENT = True 
        elif name == "--server":
            config.SERVER = True
        elif name == "--listen-to":
            config.LISTEN_ADDR = value
        elif name == "--server-addr":
            config.SERVER_ADDR = value
        elif name == "--logging-level":
            values = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
            }
            config.LOGGIN_LEVEL = values[value]

    # check arguments validity
    if config.CLIENT and config.SERVER:
        return False

    return True

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "", [
            "client",
            "server",
            "listen-to=",
            "server-addr=",
            "logging-level=",
            "settings="])
    except getopt.GetoptError, err:
        usage(argv[0])
        return True

    if not opts:
        usage(argv[0])
        return True

    if not args_evaluation(opts):
        usage(argv[0], check[1])
        return True

    if config.CLIENT:
        from lightmon.client import runner
        runner.run()
    elif config.SERVER:
        from lightmon.server import runner
        runner.run()

    return False

def usage(name, errstring=None):
    """
    Print usage instructions
    """
    if errstring: print errstring
    print("""%s <options>
    --client                run in client mode
    --server                run in server mode
    --config <config>       use <config> module as config
    --listen-to <port>      listen to the port <port> (only for server mode)
    --server-addr <server>  set <server> as the server to connect (only for client mode)
    --logging-level <level> set the logging level as <level> (can be INFO or DEBUG)
    """ % name)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
