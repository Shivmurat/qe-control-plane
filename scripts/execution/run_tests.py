import os
import subprocess
import time
import pytest

from framework.core.context.execution_context import ExecutionContext
from framework.utils.config_loader import ConfigLoader
from framework.observability.metrics import start_metrics_server
from framework.observability.metrics import active_executions

config = ConfigLoader.load_config()

parallel_workers = config.get("parallel_workers", 1)


run_id = ExecutionContext.get_run_id()

os.environ["RUN_ID"] = run_id


allure_results_dir = ExecutionContext.get_allure_results_dir()

allure_report_dir = ExecutionContext.get_allure_report_dir()


junit_report_path = (
    ExecutionContext.get_run_root()
    / "junit"
    / "results.xml"
)


junit_report_path.parent.mkdir(
    parents=True,
    exist_ok=True
)


pytest_command = [
    "pytest",
    "tests/smoke",
    "-v",
 #   "-n",
 #   str(parallel_workers),
    f"--alluredir={allure_results_dir}",
    f"--junitxml={junit_report_path}"
]

start_metrics_server()
print("Metrics server started on port 8000")

active_executions.inc()

#pytest_result = subprocess.run(pytest_command)
pytest_result = pytest.main(pytest_command[1:])

active_executions.dec()


allure_command = [
    "allure",
    "generate",
    str(allure_results_dir),
    "-o",
    str(allure_report_dir),
    "--clean"
]


subprocess.run(allure_command)


print(f"\nAllure report generated at: {allure_report_dir}")

time.sleep(300)
exit(pytest_result)