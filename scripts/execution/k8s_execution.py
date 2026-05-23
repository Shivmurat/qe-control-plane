import subprocess
import os

namespace = os.getenv("NAMESPACE","default")

subprocess.run(
    [
        "kubectl",
        "delete",
        "job",
        "qe-control-plane-job",
        "--ignore-not-found"
    ]
)

subprocess.run(
    [
        "kubectl",
        "apply",
        "-f",
        "k8s/jobs/qe-job.yaml",
        "-n",
        namespace
    ],
    check=True
)


pod_name = subprocess.check_output(
    [
        "kubectl",
        "get",
        "pods",
        "--selector=job-name=qe-control-plane-job",
        "--output=jsonpath={.items[0].metadata.name}"
    ],
    text=True
).strip()


subprocess.run(
    [
        "kubectl",
        "wait",
        "--for=condition=Ready",
        f"pod/{pod_name}",
        "--timeout=120s"
    ],
    check=True
)


subprocess.run(
    [
        "./scripts/k8s/copy_k8s_artifacts.sh"
    ],
    check=True
)

run_id = subprocess.check_output(
    [
        "kubectl",
        "exec",
        pod_name,
        "--",
        "sh",
        "-c",
        "ls /app/artifacts/runs | tail -n 1"
    ],
    text=True
).strip()

print(f"RUN_ID={run_id}")

with open("run_id.txt", "w") as file:
    file.write(run_id)