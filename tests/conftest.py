from datetime import datetime

import pytest

from framework.core.context.execution_context import ExecutionContext
from framework.utils.config_loader import ConfigLoader
from framework.utils.logger import LoggerManager

from framework.observability.metrics import test_passed_total
from framework.observability.metrics import test_failed_total
from framework.observability.metrics import test_skipped_total
from framework.observability.metrics import execution_duration_seconds

pytest_plugins = [
    "framework.fixtures.reqres.reqres_fixtures"
]

logger = LoggerManager.get_logger()
config = ConfigLoader.load_config()

def pytest_sessionstart(session):
    """
    Triggered before test session starts
    """

    logger.info("=" * 80)
    logger.info("Starting test execution")
    logger.info(f"Run ID: {ExecutionContext.get_run_id()}")
    logger.info(f"Environment: {config.get('environment')}")
    logger.info(f"Execution Start time: {datetime.now()}")
    logger.info("=" * 80)


def pytest_sessionfinish(session, exitstatus):
    """
    Triggered after test session completes.
    """

    logger.info("=" * 80)
    logger.info("Test execution completed")

    execution_summary= {
        "run_id": ExecutionContext.get_run_id(),
        "environment": config.get("environment"),
        "exit_status": exitstatus,
        "total_duration_seconds": ExecutionContext.get_execution_duration_second(),
        "execution_complated_at": str(datetime.now())
    }

    ExecutionContext.write_execution_summary(execution_summary)

    ExecutionContext.write_test_results()

    ExecutionContext.generate_aggregated_results()

    logger.info(f"Execution summary: {execution_summary}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture per-test execution results
    """

    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    test_result = {
        "worker": ExecutionContext.get_worker_id(),

        "test_name": report.nodeid,

        "status": report.outcome,

        "duration_seconds": round(report.duration, 2)
    }

    ExecutionContext.add_test_result(test_result)

    logger.info(
        f"Test Result | "
        f"Name: {report.nodeid} | "
        f"Status: {report.outcome} | "
        f"Duration: {round(report.duration, 2)}s"
    )


def pytest_runtest_logreport(report):

    if report.when != "call":

        return

    execution_duration_seconds.observe(report.duration)


    if report.passed:

        test_passed_total.inc()


    elif report.failed:

        test_failed_total.inc()


    elif report.skipped:

        test_skipped_total.inc()