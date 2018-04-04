import requests

from django.db import models

from cabot.cabotapp.models import StatusCheck, StatusCheckResult


class PrometheusStatusCheck(StatusCheck):
    check_name = 'prometheus'
    edit_url_name = 'update-prometheus-check'
    duplicate_url_name = 'duplicate-prometheus-check'
    icon_class = 'glyphicon-fire'

    host = models.TextField()
    query = models.TextField(
        help_text='Prometheus expression query string',
    )
    def _run(self):
        result = StatusCheckResult(status_check=self)

        try:
            resp = requests.get(
                self.host + '?query=' + self.query,
                timeout=self.timeout
            )
        except requests.RequestException as e:
            result.error = u'Request error occurred: %s' % (e.message,)
            result.succeeded = False
        else:
            if resp.json().status != 'success':
                result.error = u'Query unsuccessful with response %s' % resp.json().status
                result.succeeded = False
                result.raw_data = resp.content
            else:
                result.succeeded = True
        return result