#!/usr/bin/env python
"""
Run script
"""

import sys
import getopt

def argcheck(opts):
    print opts

def main(args):
    try:
        opt, opts = getopt.getopt(sys.args[1:], "", ["client", "server", "listen-to=", "server-addr="])
    except getopt.GetoptError, err:
        usage(args[0])
        return True

    options = argcheck(opts)

    return False

def usage(name):
    """
    Print usage instructions
    """
    print """%s <options>
    --client                run in client mode
    --server                run in server mode
    --listen-to <port  >    listen to the port <port> (only for server mode)
    --server-addr <server>  set <server> as the server to connect (only for client mode)
    """ % name

if __name__ == '__main__':
    sys.exit(main(sys.argv))
