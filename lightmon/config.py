"""
Default settings for lightmon
"""
import logging

# these two variables are True according to in which modes
# lightmon is running
CLIENT = False
SERVER = False

# self check the lightmon status every SELF_CHECK_EVERY seconds
SELF_CHECK_EVERY = 1

# logging default level
LOGGING_LEVEL = logging.INFO

# log file
LOGGING_FILE = "lightmon.log"

# maximum time (in seconds) that threads can use to execute
MAX_CHECK_EXECUTION_TIME = 15

# server listening address (only server)
LISTEN_ADDR = "127.0.0.1"

# server address (only client)
SERVER_ADDR = "127.0.0.1"

# the job list
JOBS = []
