#!/usr/bin/env python
"""
Run script
"""

import sys
import getopt

def argcheck(opts):
    class Options:
        "Default arguments"
        client = False
        server = False
        listen_to = "127.0.0.1"
        server_addr = "127.0.0.1"

        def check(self):
            client = self.client
            server = self.server
            listen_to = self.listen_to
            server_addr = self.server_addr

            if client and server or not (client or server):
                return (False, "Cannot be both client and server simultaneosly")
            # TODO: check for listen_to/server_addr validity
            # elif ...
            return (True, "ok")

    o = Options()
    for name, value in opts:
        if name == "--client":
            o.client = True
        elif name == "--server":
            o.server = True
        elif name == "--listen-to":
            o.listen_to = value
        elif name == "--server-addr":
            o.server_addr = value
    return o

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "", ["client", "server", "listen-to=", "server-addr="])
    except getopt.GetoptError, err:
        usage(argv[0])
        return True

    options = argcheck(opts)
    check = options.check()
    if not check[0]:
        usage(argv[0], check[1])
        return True

    if options.client:
        from lightmon.client import runner
        runner.run()
    elif options.server:
        from lightmon.server import runner
        runner.run()

    return False

def usage(name, errstring=None):
    """
    Print usage instructions
    """
    if errstring: print errstring
    print """%s <options>
    --client                run in client mode
    --server                run in server mode
    --listen-to <port>      listen to the port <port> (only for server mode)
    --server-addr <server>  set <server> as the server to connect (only for client mode)
    """ % name

if __name__ == '__main__':
    sys.exit(main(sys.argv))
