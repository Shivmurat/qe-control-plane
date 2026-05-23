from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram
from prometheus_client import start_http_server


test_passed_total = Counter(
    "test_passed_total",
    "Total passed tests"
)


test_failed_total = Counter(
    "test_failed_total",
    "Total failed tests"
)


test_skipped_total = Counter(
    "test_skipped_total",
    "Total skipped tests"
)


execution_duration_seconds = Histogram(
    "execution_duration_seconds",
    "Test execution duration"
)


active_executions = Gauge(
    "active_executions",
    "Currently active test executions"
)


active_workers = Gauge(
    "active_workers",
    "Currently active pytest workers"
)


def start_metrics_server():

    start_http_server(8000)