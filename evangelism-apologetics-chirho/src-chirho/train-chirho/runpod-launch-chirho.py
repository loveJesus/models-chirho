# For God so loved the world that he gave his only begotten Son,
# that whoever believes in him should not perish but have eternal life. - John 3:16

"""
runpod-launch-chirho.py
Launch an H200 pod on RunPod for Qwen3-4B LoRA generator training.

Steps:
1. Create H200 pod with PyTorch template
2. Wait for pod to be ready
3. Upload training data + script
4. Run training
5. Download results
"""

import json
import os
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
                # Handle variable references like $VAR
                if val_chirho.startswith("$"):
                    val_chirho = os.environ.get(val_chirho[1:], val_chirho)
                os.environ[key_chirho] = val_chirho

import runpod

# ── Constants ──────────────────────────────────────────────────────────
RUNPOD_API_KEY_CHIRHO = os.environ.get("RUNPOD_CHIRHO", "")
if not RUNPOD_API_KEY_CHIRHO:
    print("ERROR: RUNPOD_CHIRHO not found in .env")
    sys.exit(1)

runpod.api_key = RUNPOD_API_KEY_CHIRHO

POD_NAME_CHIRHO = "evangelism-generator-chirho"
GPU_TYPE_CHIRHO = "NVIDIA H200"  # H200 SXM 80GB
# Fallback GPU types in order of preference
FALLBACK_GPUS_CHIRHO = [
    "NVIDIA H100 80GB HBM3",
    "NVIDIA H100 SXM",
    "NVIDIA A100 80GB PCIe",
    "NVIDIA A100-SXM4-80GB",
]

# Docker image with PyTorch + CUDA pre-installed
DOCKER_IMAGE_CHIRHO = "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"

# Volume for persistent storage
VOLUME_SIZE_CHIRHO = 50  # GB

BASE_DIR_CHIRHO = Path("/Volumes/ENC_4TB_WDB_CHIRHO/dev-aleluya/personal-aleluya/models-chirho/evangelism-apologetics-chirho")


def create_pod_chirho():
    """Create an H200 pod on RunPod."""
    print(f"Creating pod: {POD_NAME_CHIRHO}")
    print(f"GPU: {GPU_TYPE_CHIRHO}")

    try:
        pod_chirho = runpod.create_pod(
            name=POD_NAME_CHIRHO,
            image_name=DOCKER_IMAGE_CHIRHO,
            gpu_type_id=GPU_TYPE_CHIRHO,
            gpu_count=1,
            volume_in_gb=VOLUME_SIZE_CHIRHO,
            container_disk_in_gb=30,
            min_vcpu_count=4,
            min_memory_in_gb=32,
            ports="22/tcp,8888/http",
            support_public_ip=True,
        )
        print(f"  Pod created: {pod_chirho}")
        return pod_chirho
    except Exception as e_chirho:
        print(f"  H200 not available: {e_chirho}")
        print("  Trying fallback GPUs...")

        for gpu_chirho in FALLBACK_GPUS_CHIRHO:
            try:
                print(f"  Trying: {gpu_chirho}")
                pod_chirho = runpod.create_pod(
                    name=POD_NAME_CHIRHO,
                    image_name=DOCKER_IMAGE_CHIRHO,
                    gpu_type_id=gpu_chirho,
                    gpu_count=1,
                    volume_in_gb=VOLUME_SIZE_CHIRHO,
                    container_disk_in_gb=30,
                    min_vcpu_count=4,
                    min_memory_in_gb=32,
                    ports="22/tcp,8888/http",
                    support_public_ip=True,
                )
                print(f"  Pod created with {gpu_chirho}: {pod_chirho}")
                return pod_chirho
            except Exception as e2_chirho:
                print(f"    Not available: {e2_chirho}")
                continue

        print("ERROR: No GPU available")
        sys.exit(1)


def wait_for_pod_chirho(pod_id_chirho, timeout_chirho=300):
    """Wait for pod to be running and SSH-accessible."""
    print(f"\nWaiting for pod {pod_id_chirho} to be ready...")
    start_chirho = time.time()

    while time.time() - start_chirho < timeout_chirho:
        pod_chirho = runpod.get_pod(pod_id_chirho)
        status_chirho = pod_chirho.get("desiredStatus", "unknown")
        runtime_chirho = pod_chirho.get("runtime", {})

        if status_chirho == "RUNNING" and runtime_chirho:
            ssh_port_chirho = None
            public_ip_chirho = runtime_chirho.get("ports", [])
            for port_chirho in public_ip_chirho:
                if port_chirho.get("privatePort") == 22:
                    ssh_port_chirho = port_chirho.get("publicPort")
                    public_ip_chirho = port_chirho.get("ip")
                    break

            if ssh_port_chirho:
                print(f"  Pod ready! SSH: {public_ip_chirho}:{ssh_port_chirho}")
                return {
                    "id_chirho": pod_id_chirho,
                    "ip_chirho": public_ip_chirho,
                    "ssh_port_chirho": ssh_port_chirho,
                    "pod_chirho": pod_chirho,
                }

        print(f"  Status: {status_chirho} (elapsed: {int(time.time() - start_chirho)}s)")
        time.sleep(10)

    print("ERROR: Timeout waiting for pod")
    return None


def main_chirho():
    """Launch RunPod for generator training."""
    print("=" * 60)
    print("Model 9: Launch RunPod H200 for Generator Training")
    print("=" * 60)

    # List available GPUs
    print("\nChecking GPU availability...")
    try:
        gpus_chirho = runpod.get_gpus()
        print(f"  Available GPU types: {len(gpus_chirho)}")
        for gpu_chirho in gpus_chirho:
            gpu_id_chirho = gpu_chirho.get("id", "")
            display_chirho = gpu_chirho.get("displayName", "")
            mem_chirho = gpu_chirho.get("memoryInGb", 0)
            if any(kw_chirho in display_chirho.lower() for kw_chirho in ["h200", "h100", "a100"]):
                print(f"    {gpu_id_chirho}: {display_chirho} ({mem_chirho}GB)")
    except Exception as e_chirho:
        print(f"  Warning: Could not list GPUs: {e_chirho}")

    # Create pod
    pod_result_chirho = create_pod_chirho()
    pod_id_chirho = pod_result_chirho.get("id", "")
    if not pod_id_chirho:
        print(f"  Pod response: {pod_result_chirho}")
        pod_id_chirho = pod_result_chirho.get("id", pod_result_chirho)
        if isinstance(pod_id_chirho, dict):
            pod_id_chirho = pod_id_chirho.get("id", "")
    print(f"\n  Pod ID: {pod_id_chirho}")

    # Wait for it
    pod_info_chirho = wait_for_pod_chirho(pod_id_chirho)

    if pod_info_chirho:
        ip_chirho = pod_info_chirho["ip_chirho"]
        port_chirho = pod_info_chirho["ssh_port_chirho"]

        print(f"\n{'=' * 60}")
        print("POD READY — SSH access:")
        print(f"  ssh root@{ip_chirho} -p {port_chirho}")
        print(f"\nSCP data to pod:")
        print(f"  scp -P {port_chirho} -r data-chirho/processed-chirho/generator-chirho/ root@{ip_chirho}:/workspace/data/")
        print(f"  scp -P {port_chirho} train-generator-chirho.py root@{ip_chirho}:/workspace/")
        print(f"\nOn the pod, run:")
        print(f"  pip install transformers peft sentence-transformers accelerate bitsandbytes")
        print(f"  python /workspace/train-generator-chirho.py")
        print("=" * 60)

        # Save pod info for later retrieval
        info_path_chirho = BASE_DIR_CHIRHO / "runpod-info-chirho.json"
        with open(info_path_chirho, "w") as f_chirho:
            json.dump({
                "pod_id_chirho": pod_id_chirho,
                "ip_chirho": ip_chirho,
                "ssh_port_chirho": port_chirho,
            }, f_chirho, indent=2)
        print(f"\nPod info saved to: {info_path_chirho}")


if __name__ == "__main__":
    main_chirho()
