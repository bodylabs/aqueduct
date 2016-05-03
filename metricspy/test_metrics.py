import time
import unittest
import mock

class TestMetrics(unittest.TestCase):

    @mock.patch('datadog.initialize')
    def test_metrics_initialized_with_known_backend(self, initialize_mock): # pylint: disable=unused-argument

        from metricspy.metrics import Metrics
        metrics_uri = 'metrics://abc@datadog?app_key=def&debug=true'

        Metrics(metrics_uri)

        initialize_mock.assert_called_once_with(api_key='abc', app_key='def', debug='true')

    @mock.patch('datadog.initialize')
    def test_metrics_initialized_with_unknown_backend_raise_error(self, initialize_mock): # pylint: disable=unused-argument

        from metricspy.metrics import Metrics

        metrics_uri = 'metrics://abc@unknown?app_key=def&debug=true'

        with self.assertRaises(NotImplementedError):
            Metrics(metrics_uri)

class TestDatadog(unittest.TestCase):

    def setUp(self):

        from metricspy.metrics import Metrics

        metrics_uri = 'metrics://abc@datadog?app_key=def&debug=true'

        self.datadog_metrics = Metrics(metrics_uri)

    @mock.patch('datadog.initialize')
    @mock.patch('datadog.api.metrics.Metric.send')
    def test_datadog_send_metrics_with_tags_tranformed(self, send_mock, initialize_mock): # pylint: disable=unused-argument

        self.datadog_metrics.send('test', 1, tags={'tag1': 'a'})

        send_mock.assert_called_once_with(
            metric='test',
            points=(int(time.time()), 1),
            tags=['tag1:a'],
            type='gauge'
        )

    @mock.patch('datadog.initialize')
    @mock.patch('datadog.api.metrics.Metric.send')
    def test_datadog_send_metrics_with_overrided_timestamp(self, send_mock, initialize_mock): # pylint: disable=unused-argument

        timestamp = int(time.time()) - 5000
        self.datadog_metrics.send('test', 1, tags={'tag1': 'a'}, timestamp=timestamp)

        send_mock.assert_called_once_with(
            metric='test',
            points=(timestamp, 1),
            tags=['tag1:a'],
            type='gauge'
        )
