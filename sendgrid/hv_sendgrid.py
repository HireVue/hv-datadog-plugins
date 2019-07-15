import urllib2
import simplejson
import datetime

try:
    # first, try to import the base class from old versions of the Agent...
    from checks import AgentCheck
except ImportError:
    # ...if the above failed, the check is running in Agent version 6 or later
    from datadog_checks.checks import AgentCheck

__version__ = '19.6.1'


class HVSendgrid(AgentCheck):
    def check(self, instance):
        api_key = instance.get('api_key', "12345")
        account = instance.get('account', api_key[0:5])
        user = instance.get('user', api_key[0:5])
        base_url = instance.get('base_url', "https://api.sendgrid.com")
        tags = instance.get('tags', [])
        now = datetime.datetime.now()
        tstamp = now.strftime('%Y-%m-01')

        fullurl = "{}/v3/stats?aggregated_by=month&start_date={}".format(base_url, tstamp)
        headers = {
            'Authorization': 'Bearer  {}'.format(api_key)
        }
        req = urllib2.Request(fullurl, headers=headers)
        try:
            response = urllib2.urlopen(req)
            data = simplejson.load(response)
        except urllib2.HTTPError:
            data = {}

        filtered_data = [x for x in data if x.get('date',None) == tstamp]

        if len(filtered_data) > 0:
            metrics = filtered_data[0]['stats'][0]['metrics']
            tags.append('sendgrid_account:{}'.format(account))
            tags.append('sendgrid_user:{}'.format(user))
            for metric, value in metrics.iteritems():
                self.gauge('hv_sendgrid.metrics.{}'.format(metric), value, tags=tags)
