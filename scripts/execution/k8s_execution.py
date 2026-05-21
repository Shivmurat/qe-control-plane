import subprocess


subprocess.run(
    [
        "kubectl",
        "apply",
        "-f",
        "k8s/jobs/qe-job.yaml"
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