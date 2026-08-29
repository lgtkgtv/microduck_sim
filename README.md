```markdown
# Quickstart for Physical AI: Microduck Simulation

An end-to-end Physical AI architecture and training pipeline for the Hugging Face LeRobot Microduck (15-DOF bipedal robot). This project demonstrates how to transition from headless physics simulation to Reinforcement Learning (RL), perform surgical model extraction for hardware safety, and deploy a low-latency 50Hz asynchronous control loop on edge hardware.

## Architecture Overview

This project implements a biological "Dual-Loop" sensor fusion architecture, separating heavy vision processing from the critical, low-latency balance loop.

```text
[ Visual Cortex ] (Background Thread @ 10Hz)
      RGB Camera -> PyTorch CNN -> Shared Memory (32 Features)
                                           |
                                           v
[ Spinal Cord ]   (Main Thread @ 50Hz)
      IMU / Encoders (15 Features) ----> [ FUSION ]
                                           |
                                  [ ONNX Actor Policy ]
                                           |
                            [ Hardware Safety Clamp (-1.0 to 1.0) ]
                                           |
                               [ 15-DOF Motor Actuation ]

```

## Features

* **Headless MuJoCo Simulation:** Mathematically accurate physics execution without the overhead of GUI rendering.
* **PPO Reinforcement Learning:** Custom Gymnasium environment utilizing Stable Baselines3 to train balancing policies.
* **Hardware-Safe Edge Inference:** Surgical extraction of the Actor network from the PPO graph, freezing it to `ONNX` with baked-in tensor clamping to prevent motor burnout.
* **Asynchronous Sensor Fusion:** Thread-safe memory buffering that fuses 10Hz visual telemetry with 50Hz proprioceptive physical telemetry without blocking execution.

## Repository Structure

| File | Description |
| --- | --- |
| `microduck_masterclass.ipynb` | Interactive Jupyter Notebook covering the core concepts step-by-step. |
| `main.py` | Production-ready 50Hz edge controller with dual-loop sensor fusion. |
| `train_microduck.py` | RL training script utilizing PPO and Gymnasium. |
| `export_to_onnx.py` | Extracts the PyTorch Actor network and exports it to a hardware-safe ONNX. |
| `duck_drop.py` | Minimal headless MuJoCo physics validation script. |
| `create_dummy_model.py` | Generates a synthetic, untrained PyTorch network for architectural testing. |
| `microduck.xml` | Core MJCF hardware blueprint defining joints, mass, and actuators. |
| `microduck_vision.xml` | Extended MJCF blueprint including an integrated 60-FOV RGB camera. |

## Prerequisites

* **OS:** Ubuntu 24.04 (Natively or via WSL2 on Windows 11).
* **Environment Manager:** `uv` (Lightning-fast Python package installer and resolver).
* **Hardware:** Local GPU (e.g., NVIDIA RTX series) recommended for inference and RL training.

## Installation

1. Clone the repository and navigate to the project root:
```bash
git clone https://github.com/lgtkgtv/microduck_sim.git
cd microduck_sim
```


2. Initialize the `uv` environment and install dependencies:
```bash
uv init
uv add mujoco onnxruntime numpy torch onnx onnxscript stable-baselines3 gymnasium jupyter

```


3. Install system-level OpenGL graphics libraries (Required for MuJoCo headless rendering on Ubuntu 24.04):
```bash
sudo apt-get update
sudo apt-get install -y libglfw3 libglew-dev libgl1 libgl1-mesa-dev libosmesa6

```



## Usage Guide

### 1. The Interactive Masterclass

The best way to understand the architecture is to walk through the interactive Jupyter notebook.

```bash
uv run jupyter notebook

```

Open `microduck_masterclass.ipynb` in your browser.

### 2. Verify the Physics Engine

Run the minimal gravity test to ensure MuJoCo and the Linux graphics dependencies are communicating.

```bash
uv run duck_drop.py

```

### 3. Train the Robot

Launch the Proximal Policy Optimization (PPO) training gym. This will generate a `microduck_ppo_policy.zip` file upon completion.

```bash
uv run train_microduck.py

```

### 4. Export to Silicon

Extract the reflexes and bake in the hardware safety clamps to generate `microduck_walking_policy.onnx`.

```bash
uv run export_to_onnx.py

```

### 5. Run the Edge Controller

Execute the production 50Hz asynchronous control loop.

```bash
uv run main.py

```

```

```
