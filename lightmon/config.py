"""
Default settings for lightmon
"""
import logging

# self check the lightmon status every SELF_CHECK_EVERY seconds
SELF_CHECK_EVERY = 1

# logging default level
LOGGING_LEVEL = logging.INFO

# log file
LOGGING_FILE = "lightmon.log"

# maximum time (in seconds) that threads can use to execute
MAX_CHECK_EXECUTION_TIME = 15

# the job list
JOBS = []
