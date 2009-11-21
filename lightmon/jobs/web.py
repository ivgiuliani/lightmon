"""
A set of jobs for checking web-related statuses
"""

from lightmon.jobs.basejob import Job

import urllib2

class HTTPStatusCodeCheckJob(Job):
    "Makes a HTTP request and checks that the HTTP code returned is `code`"

    def __init__(self, url, code=200, timeout=5, *args, **kwargs):
        """
        Initialize a HTTPCodeCheck object. Parameters are:
        @url = url to check
        @code = http code to compare
        @timeout = go in timeout after `timeout` seconds
        """
        super(HTTPStatusCodeCheckJob, self).__init__(*args, **kwargs)
        self.url = url
        self.code = code
        self.timeout = timeout

    def run(self):
        "Perform the actual http status code check"
        try:
            res = urllib2.urlopen(self.url, timeout=self.timeout)
            # XXX: .getcode() works only in python 2.4
            code = res.getcode()
        except (urllib2.URLError, urllib2.HTTPError):
            return False

        return code == 200
