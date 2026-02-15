# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
runpod-setup-chirho.py
Terminate old pod, create new H200 with SSH key, upload data, run training.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Load env
ENV_PATH_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/.env")
if ENV_PATH_CHIRHO.exists():
    with open(ENV_PATH_CHIRHO) as f_chirho:
        for line_chirho in f_chirho:
            line_chirho = line_chirho.strip()
            if line_chirho and not line_chirho.startswith("#") and "=" in line_chirho:
                if line_chirho.startswith("export "):
                    line_chirho = line_chirho[7:]
                key_chirho, val_chirho = line_chirho.split("=", 1)
                val_chirho = val_chirho.strip('"').strip("'")
                if val_chirho.startswith("$"):
                    val_chirho = os.environ.get(val_chirho[1:], val_chirho)
                os.environ[key_chirho] = val_chirho

import runpod

RUNPOD_API_KEY_CHIRHO = os.environ.get("RUNPOD_CHIRHO", "")
runpod.api_key = RUNPOD_API_KEY_CHIRHO

SSH_PUB_KEY_CHIRHO = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJWN8S5YcLSkwA5xMgNTqOFwMnmUkfWP4AU+p4A/pkgk hallelujah@Hallelujahs-MacBook-Pro.local"

BASE_DIR_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho")
DATA_DIR_CHIRHO = BASE_DIR_CHIRHO / "data-chirho" / "processed-chirho" / "generator-chirho"
TRAIN_SCRIPT_CHIRHO = BASE_DIR_CHIRHO / "src-chirho" / "train-chirho" / "train-generator-runpod-chirho.py"

OLD_POD_ID_CHIRHO = "gvbhv6hmmc2wex"


def terminate_old_pod_chirho():
    """Terminate the old pod without SSH key."""
    try:
        print(f"Terminating old pod: {OLD_POD_ID_CHIRHO}")
        runpod.terminate_pod(OLD_POD_ID_CHIRHO)
        print("  Done.")
        time.sleep(5)
    except Exception as e_chirho:
        print(f"  Warning: {e_chirho}")


def create_pod_with_ssh_chirho():
    """Create H200 pod with SSH public key."""
    print("\nCreating H200 pod with SSH key...")

    gpu_types_chirho = ["NVIDIA H200", "NVIDIA H100 80GB HBM3", "NVIDIA A100 80GB PCIe"]

    for gpu_chirho in gpu_types_chirho:
        try:
            print(f"  Trying: {gpu_chirho}")
            pod_chirho = runpod.create_pod(
                name="evangelism-generator-chirho",
                image_name="runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04",
                gpu_type_id=gpu_chirho,
                gpu_count=1,
                volume_in_gb=50,
                container_disk_in_gb=30,
                min_vcpu_count=4,
                min_memory_in_gb=32,
                ports="22/tcp,8888/http",
                support_public_ip=True,
                env={
                    "PUBLIC_KEY": SSH_PUB_KEY_CHIRHO,
                },
            )
            pod_id_chirho = pod_chirho.get("id", "")
            print(f"  Pod created: {pod_id_chirho} on {gpu_chirho}")
            return pod_id_chirho
        except Exception as e_chirho:
            print(f"    Not available: {e_chirho}")
            continue

    print("ERROR: No GPU available")
    sys.exit(1)


def wait_for_ssh_chirho(pod_id_chirho, timeout_chirho=300):
    """Wait for pod to be running and SSH-accessible."""
    print(f"\nWaiting for pod {pod_id_chirho}...")
    start_chirho = time.time()

    while time.time() - start_chirho < timeout_chirho:
        pod_chirho = runpod.get_pod(pod_id_chirho)
        status_chirho = pod_chirho.get("desiredStatus", "unknown")
        runtime_chirho = pod_chirho.get("runtime", {})

        if status_chirho == "RUNNING" and runtime_chirho:
            ports_chirho = runtime_chirho.get("ports", [])
            for port_chirho in ports_chirho:
                if port_chirho.get("privatePort") == 22:
                    ip_chirho = port_chirho.get("ip")
                    ssh_port_chirho = port_chirho.get("publicPort")
                    print(f"  Pod ready! SSH: {ip_chirho}:{ssh_port_chirho}")

                    # Wait a bit for sshd to start
                    time.sleep(10)

                    # Test SSH
                    test_chirho = subprocess.run(
                        ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10",
                         "-p", str(ssh_port_chirho), f"root@{ip_chirho}", "echo ok"],
                        capture_output=True, text=True, timeout=30,
                    )
                    if test_chirho.returncode == 0:
                        print("  SSH connected!")
                        return ip_chirho, ssh_port_chirho
                    else:
                        print(f"  SSH not ready yet: {test_chirho.stderr.strip()}")
                        time.sleep(10)

        print(f"  Status: {status_chirho} ({int(time.time() - start_chirho)}s)")
        time.sleep(10)

    print("ERROR: Timeout")
    sys.exit(1)


def upload_and_train_chirho(ip_chirho, port_chirho):
    """Upload data and training script, then start training."""
    ssh_target_chirho = f"root@{ip_chirho}"
    ssh_opts_chirho = ["-o", "StrictHostKeyChecking=no", "-p", str(port_chirho)]

    def ssh_cmd_chirho(cmd_chirho, timeout_secs_chirho=600):
        result_chirho = subprocess.run(
            ["ssh"] + ssh_opts_chirho + [ssh_target_chirho, cmd_chirho],
            capture_output=True, text=True, timeout=timeout_secs_chirho,
        )
        if result_chirho.stdout:
            print(f"  {result_chirho.stdout.strip()}")
        if result_chirho.stderr:
            for line_chirho in result_chirho.stderr.strip().split("\n"):
                if line_chirho and "Warning" not in line_chirho:
                    print(f"  ERR: {line_chirho}")
        return result_chirho

    def scp_chirho(local_chirho, remote_chirho, is_dir_chirho=False):
        cmd_chirho = ["scp", "-o", "StrictHostKeyChecking=no", "-P", str(port_chirho)]
        if is_dir_chirho:
            cmd_chirho.append("-r")
        cmd_chirho.extend([str(local_chirho), f"{ssh_target_chirho}:{remote_chirho}"])
        result_chirho = subprocess.run(cmd_chirho, capture_output=True, text=True, timeout=300)
        return result_chirho.returncode == 0

    # 1. Create directories
    print("\nSetting up pod...")
    ssh_cmd_chirho("mkdir -p /workspace/data/generator-chirho /workspace/models/generator-chirho")

    # 2. Upload training data
    print("\nUploading training data...")
    for split_chirho in ["train-chirho.jsonl", "val-chirho.jsonl", "test-chirho.jsonl"]:
        local_path_chirho = DATA_DIR_CHIRHO / split_chirho
        if local_path_chirho.exists():
            success_chirho = scp_chirho(local_path_chirho, f"/workspace/data/generator-chirho/{split_chirho}")
            size_chirho = local_path_chirho.stat().st_size / 1024 / 1024
            print(f"  {split_chirho}: {size_chirho:.1f}MB {'OK' if success_chirho else 'FAIL'}")

    # 3. Upload training script
    print("\nUploading training script...")
    scp_chirho(TRAIN_SCRIPT_CHIRHO, "/workspace/train-generator-runpod-chirho.py")

    # 4. Install dependencies
    print("\nInstalling dependencies...")
    ssh_cmd_chirho(
        "pip install transformers peft accelerate bitsandbytes 2>&1 | tail -3",
        timeout_secs_chirho=300,
    )

    # 5. Check GPU
    print("\nChecking GPU...")
    ssh_cmd_chirho("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader")

    # 6. Verify data uploaded
    print("\nVerifying data...")
    ssh_cmd_chirho("wc -l /workspace/data/generator-chirho/*.jsonl")

    # 7. Start training in tmux
    print("\nStarting training in tmux...")
    ssh_cmd_chirho(
        'tmux new-session -d -s train_chirho '
        '"python /workspace/train-generator-runpod-chirho.py 2>&1 | tee /workspace/train-log-chirho.txt"'
    )

    print("\n" + "=" * 60)
    print("TRAINING STARTED ON RUNPOD H200!")
    print("=" * 60)
    print(f"\nSSH: ssh -p {port_chirho} root@{ip_chirho}")
    print(f"Monitor: ssh -p {port_chirho} root@{ip_chirho} 'tmux attach -t train_chirho'")
    print(f"Log: ssh -p {port_chirho} root@{ip_chirho} 'tail -f /workspace/train-log-chirho.txt'")
    print(f"\nDownload results when done:")
    print(f"  scp -P {port_chirho} -r root@{ip_chirho}:/workspace/models/generator-chirho/best-chirho/ \\")
    print(f"    {BASE_DIR_CHIRHO}/models-chirho/generator-chirho/best-chirho/")

    # Save pod info
    info_path_chirho = BASE_DIR_CHIRHO / "runpod-info-chirho.json"
    with open(info_path_chirho, "w") as f_chirho:
        json.dump({
            "pod_id_chirho": pod_id_chirho,
            "ip_chirho": ip_chirho,
            "ssh_port_chirho": port_chirho,
        }, f_chirho, indent=2)


if __name__ == "__main__":
    # Terminate old pod
    terminate_old_pod_chirho()

    # Create new pod with SSH key
    pod_id_chirho = create_pod_with_ssh_chirho()

    # Wait for SSH
    ip_chirho, port_chirho = wait_for_ssh_chirho(pod_id_chirho)

    # Upload and train
    upload_and_train_chirho(ip_chirho, port_chirho)
