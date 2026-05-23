import subprocess
import os
import time

namespace = os.getenv("NAMESPACE","default")

subprocess.run(
    [
        "kubectl",
        "delete",
        "job",
        "qe-control-plane-job",
        "-n",
        namespace,
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


pod_name = None
for _ in range(30):
    try:
        pod_name = subprocess.check_output(
            [
                "kubectl",
                "get",
                "pods",
                "-n",
                namespace,
                "--selector=job-name=qe-control-plane-job",
                "--output=jsonpath={.items[0].metadata.name}"
            ],
            text=True
        ).strip()
        if pod_name:
            break
    except subprocess.CalledProcessError:
        pass
    time.sleep(2)


if not pod_name:

    raise Exception("Pod was not created in expected time")


subprocess.run(
    [
        "kubectl",
        "wait",
        "-n",
        namespace,
        "--for=condition=Ready",
        f"pod/{pod_name}",
        "--timeout=120s"
    ],
    check=True
)


subprocess.run(
    [
        "./scripts/k8s/copy_k8s_artifacts.sh",
        namespace,
        pod_name
    ],
    check=True
)

run_id = subprocess.check_output(
    [
        "kubectl",
        "exec",
        "-n",
        namespace,
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