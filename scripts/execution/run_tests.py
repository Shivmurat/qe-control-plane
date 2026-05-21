import subprocess
import os
from datetime import datetime

from framework.core.context.execution_context import ExecutionContext
from framework.utils.config_loader import ConfigLoader


config = ConfigLoader.load_config()

parallel_workers = config.get("parallel_workers", 1)

allure_results_dir = ExecutionContext.get_allure_results_dir()

allure_report_dir = ExecutionContext.get_allure_report_dir()

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

os.environ["RUN_ID"] = run_id

pytest_command = [
    "pytest",
    "tests/smoke",
    "-v",
    "-n",
    str(parallel_workers),
    f"--alluredir={allure_results_dir}"
]


pytest_result = subprocess.run(pytest_command)


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


exit(pytest_result.returncode)