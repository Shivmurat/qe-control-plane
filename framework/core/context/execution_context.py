import json
import os
from datetime import datetime
from doctest import master
from pathlib import Path

class ExecutionContext:

 #   _run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    _run_id = os.getenv("RUN_ID", datetime.now().strftime("%Y%m%d_%H%M%S"))

    _execution_start_time = datetime.now()

    _project_root = Path(__file__).resolve().parents[3]

  #  _run_root = _project_root / "artifacts" / "runs" / _run_id

    _test_results = []

    @classmethod
    def get_run_id(cls):
        return os.getenv("RUN_ID", cls._run_id)

    @classmethod
    def get_run_root(cls):
        _run_root = cls._project_root / "artifacts" / "runs" / cls._run_id
        _run_root.mkdir(parents=True, exist_ok=True)
        print(f"printing run root dir: {_run_root}")
        return _run_root

    @classmethod
    def get_allure_results_dir(cls):

        path = cls.get_run_root() / "allure-results"

        path.mkdir(parents=True, exist_ok=True)

        return path

    @classmethod
    def get_allure_report_dir(cls):

        path = cls.get_run_root() / "allure-report"

        path.mkdir(parents=True, exist_ok=True)

        return path

    @classmethod
    def get_logs_dir(cls):
        path = cls.get_run_root() / "logs"

        path.mkdir(parents=True, exist_ok=True)

        return path

    @classmethod
    def get_junit_dir(cls):
        path = cls.get_run_root() / "junit"

        path.mkdir(parents=True, exist_ok=True)

        return path

    @classmethod
    def get_execution_summary_file(cls):

        return cls.get_run_root() / "execution_summary.json"


    @classmethod
    def write_execution_summary(cls, summary: dict):

        summary_file = cls.get_execution_summary_file()

        with open(summary_file, "w") as file:
            json.dump(summary, file, indent=4)


    @classmethod
    def get_execution_duration_second(cls):

        duration = datetime.now() - cls._execution_start_time
        return round(duration.total_seconds(), 2)

    @classmethod
    def add_test_result(cls, result: dict):
        cls._test_results.append(result)

    @classmethod
    def get_test_results_file(cls):
        return cls.get_run_root() / f"test_results_{cls.get_worker_id()}.json"

    @classmethod
    def write_test_results(cls):
        results_file = cls.get_test_results_file()

        with open(results_file, "w") as file:
            json.dump(cls._test_results, file, indent=4)


    @classmethod
    def get_worker_id(cls):
        return os.getenv("PYTEST_XDIST_WORKER", "master")

    @classmethod
    def generate_aggregated_results(cls):
        combined_results = []

        run_root = cls.get_run_root()

        result_files = run_root.glob("test_results_*.json")

        for file in result_files:
            with open(file, "r") as f:
                worker_results = json.load(f)

                combined_results.extend(worker_results)

        aggregated_results_file = run_root / "aggregated_results.json"

        with open(aggregated_results_file, "w") as f:
            json.dump(combined_results, f, indent=4)

