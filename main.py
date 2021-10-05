import os
import time
import random
from prometheus_client import start_http_server, Gauge


def generate_metrics():
    return [
        {
            "name": "Metric1",
            "description": "Metric1 description",
            "value": random.randint(0, 100)
        },
        {
            "name": "Metric2",
            "description": "Metric2 description",
            "value": random.randint(0, 100)
        },
        {
            "name": "Metric3",
            "description": "Metric3 description",
            "value": random.randint(0, 100)
        }
    ]


class AppMetrics:
    _metrics = {}

    def __init__(self, polling_interval_seconds=5):
        self.polling_interval_seconds = polling_interval_seconds

    def update_metric(self, name, description, value):
        metric = self._metrics.get(name)
        if not metric:
            metric = Gauge(name, description)
            self._metrics[name] = metric
        metric.set(value)

    def run_metrics_loop(self):
        """Metrics fetching loop"""
        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        for i in generate_metrics():
            self.update_metric(i['name'], i['description'], i['value'])


def main():
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))
    app_metrics = AppMetrics(polling_interval_seconds=5)
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
