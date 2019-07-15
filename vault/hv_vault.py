import urllib2
import simplejson
import socket
try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

__version__ = '19.5.1'

class HVVault(AgentCheck):
    def check(self, instance):
        token = instance.get('token', "")
        hostname = instance.get('host', socket.gethostname())
        port = instance.get('port', 8200)
        ssl = 'https' if instance.get('ssl', True) else 'http'

        lburl = "{}://{}:{}".format(ssl, hostname, port)
        fullurl = "{}/v1/sys/internal/counters/requests".format(lburl)
        req = urllib2.Request(fullurl, headers={'X-Vault-Token': token})

        try:
            response = urllib2.urlopen(req)
            data = simplejson.load(response)
        except urllib2.HTTPError, error:
            data = {}

        value = data.get("data", {}).get("counters", [{}])[-1].get("total", 0)
        self.gauge('hv_vault.counters.requests', value)
