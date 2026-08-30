# 🦆 Microduck Physical AI Simulation & Masterclass

[![Live Portal](https://img.shields.io/badge/Web%20Portal-GitHub%20Pages-38bdf8?style=for-the-badge&logo=github)](https://lgtkgtv.github.io/microduck_sim/)
[![Physics Engine](https://img.shields.io/badge/Physics-MuJoCo%203.12-10b981?style=for-the-badge)](https://mujoco.org/)
[![RL Pipeline](https://img.shields.io/badge/RL-PyTorch%20%7C%20PPO-f59e0b?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![ONNX Deployment](https://img.shields.io/badge/Inference-ONNX%20Runtime-a855f7?style=for-the-badge&logo=onnx)](https://onnxruntime.ai/)
[![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)](LICENSE)

A self-contained **Physical AI simulation studio, Reinforcement Learning pipeline, and 6-phase interactive curriculum** for the [Pollen Robotics Microduck](https://github.com/pollen-robotics/microduck) (15-DOF bipedal robot).

This repository contains everything needed to simulate the robot in 3D physics, train locomotion policies using PPO, extract hardware-safe ONNX models, run an asynchronous 50Hz control loop, and teach or learn physical AI through interactive web slides and printable engineering handouts.

---

## 🧭 Understanding the Two Repositories

If you are working in the `~/agy_projects/physical_ai/` workspace, you will notice two directories:

```
~/agy_projects/physical_ai/
├── microduck_sim/   <-- (THIS REPO) Complete Simulation, RL & Masterclass Studio
└── microduck/       <-- (UPSTREAM FIRMWARE) Official Embedded Rust Daemons for RK3566
```

### How They Differ & Work Together:

| Concept | `microduck_sim` *(This Repo)* | `microduck` *(Upstream Firmware)* |
| :--- | :--- | :--- |
| **Role** | **The Digital Twin & Learning Studio** | **The Physical Robot Firmware** |
| **Language Stack** | Python 3.12, MuJoCo, PyTorch, ONNX, HTML5/JS | Rust (`cargo` workspace), C/C++ FFI |
| **Primary Output** | 3D Interactive Simulation, Trained ONNX Policies, Web Curriculum | Compiled binary daemons (`robotd`, `duckctl`) for the Rockchip RK3566 SBC |
| **Hardware Needed?** | ❌ None (Runs 100% on your laptop / PC / WSL2) |  Requires physical Microduck hardware |
| **Self-Contained?** | ✅ **Yes** (100% standalone, ready to run) | ⚠️ Embedded firmware targeting ARM Linux |

### 🌉 The Sim-to-Real Bridge:
1. **Develop in Simulation (`microduck_sim`):** You build the 3D kinematic model, train PPO neural walking policies in MuJoCo, and extract them into clamped `.onnx` files.
2. **Deploy to Hardware (`microduck`):** The resulting `.onnx` policy files are loaded by the low-level Rust `robotd` daemon on the physical robot to execute the 50Hz motor control loop.

---

## ⚡ Quickstart in 3 Steps

### Step 1: Clone & Setup
```bash
# Clone the repository
git clone https://github.com/lgtkgtv/microduck_sim.git
cd microduck_sim

# Install dependencies using uv
uv sync

# (Optional) Install graphics libraries for Linux / WSLg
sudo apt-get update && sudo apt-get install -y libglfw3 libgl1 libgl1-mesa-dev x11-xserver-utils
```

### Step 2: Launch the 3D Interactive Simulation
Launch the native MuJoCo physics viewer with live telemetry and physical interaction:
```bash
./launch.sh
```

### Step 3: Explore the Web Masterclass
Access the live web curriculum at **[https://lgtkgtv.github.io/microduck_sim/](https://lgtkgtv.github.io/microduck_sim/)**  
*Or run it locally for offline classroom use:*
```bash
uv run python -m http.server 8000
# Open http://localhost:8000 in any browser
```

---

## 🎮 Native 3D Simulation Controls

The viewer ([`launch_viewer.py`](launch_viewer.py)) includes an in-frame cursor and full 3D physics interaction:

| Control | Action | Function |
| :--- | :--- | :--- |
| **Left Click + Drag** | `Mouse Left` | **Orbit Camera** in 3D around the robot |
| **Right Click + Drag** | `Mouse Right` | **Pan Camera** across the viewport plane |
| **Scroll Wheel** | `Mouse Wheel` | **Zoom In / Out** |
| **Ctrl + Left Drag** | `Ctrl + Left Click` | **🪢 Force Perturbation:** Grab and pull the robot with virtual spring forces (Cursor turns **Red 🔴**) |
| **Ctrl + Right Drag** | `Ctrl + Right Click` | **🔄 Torque Perturbation:** Apply rotational twist to the torso |
| **Spacebar** | `Space` | **Pause / Resume** physics stepping |
| **Reset** | `R` or `Backspace` | Reset robot position to initial spawn height |
| **Visual Toggles** | `J` / `S` / `C` / `I` / `T` / `F` | Toggle **[J]**oints, **[S]**ite sensors, **[C]**ontact forces, **[I]**nertia ellipsoids, **[T]**ransparency, **[F]**loor texture |
| **Quit** | `ESC` | Close viewer window |

---

## 📚 The 6-Phase Physical AI Curriculum

A complete semester-long curriculum taking students from hardware kinematics to PPO reinforcement learning and swarm DevSecOps:

| Phase | Module Name | Focus Topic | Interactive Slides | Printable PDF |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Anatomy of a Robot** | 15-DOF Kinematics, Actuators & CAN Bus | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/phase1_anatomy.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase1_Anatomy_Handout.pdf) *(4 pgs)* |
| **Phase 2** | **The Invisible Matrix** | MuJoCo Physics, Forward Dynamics & Collision | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/phase2_matrix.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase2_Matrix_Handout.pdf) *(3 pgs)* |
| **Phase 3** | **The Dog Trainer** | Gymnasium, Reward Functions & PPO Training | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/phase3_dogtrainer.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase3_DogTrainer_Handout.pdf) *(3 pgs)* |
| **Phase 4** | **Brain Surgery** | Policy Extraction & Hardware-Safe Clamping | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/phase4_brainsurgery.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase4_BrainSurgery_Handout.pdf) *(3 pgs)* |
| **Phase 5** | **The Nervous System** | 50Hz Dual-Loop Control & Real-Time Scheduling | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/phase5_nervoussystem.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase5_NervousSystem_Handout.pdf) *(3 pgs)* |
| **Phase 6** | **Securing the Swarm** | A/B OTA Updates, CI Gates & ED25519 Crypto | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/phase6_securingswarm.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase6_SecuringSwarm_Handout.pdf) *(3 pgs)* |

* 📘 **[Download Complete Masterclass Manual (19 Pages)](https://lgtkgtv.github.io/microduck_sim/Microduck_Physical_AI_Masterclass_Complete_Book.pdf)**
* 📦 **[Download All Handouts (.ZIP)](https://lgtkgtv.github.io/microduck_sim/microduck_all_handouts.zip)**

---

## 🛠️ Training, Verification & Execution Pipeline

```bash
# Verify all 6 curriculum phases mathematically & empirically
uv run verify_curriculum.py
```

```text
[ Step 1: Verification ] uv run verify_curriculum.py   # Empirically prove all 6 curriculum phases
          │
          ▼
[ Step 2: Simulation ]   uv run duck_drop.py          # Verify MuJoCo physics & contact dynamics
          │
          ▼
[ Step 3: RL Training ]  uv run train_microduck.py    # Train PPO locomotion policy in Gymnasium
          │
          ▼
[ Step 4: Silicon Clamp] uv run export_to_onnx.py     # Extract Actor & bake [-1.0, 1.0] torque clamps
          │
          ▼
[ Step 5: Edge Control ] uv run main.py               # Run 50Hz dual-loop async controller
```

---

## 📁 Clean Repository Structure

```
microduck_sim/
├── index.html                                        # Mission Control Web Portal (GitHub Pages)
├── phase1_anatomy.html ... phase6_securingswarm.html # 6 Interactive HTML slide decks
├── Phase1_Anatomy_Handout.pdf ... Phase6_*.pdf       # 6 Printable ReportLab PDF handouts
├── Microduck_Physical_AI_Masterclass_Complete_Book.pdf # Full 19-page masterclass manual
├── microduck_all_handouts.zip                       # All PDF handouts in one bundle
│
├── launch.sh                                        # One-click native simulation launcher
├── launch_viewer.py                                 # 3D interactive viewer with HUD & cursor
├── train_microduck.py                               # PPO Reinforcement Learning pipeline
├── export_to_onnx.py                                # ONNX policy extractor with silicon clamping
├── main.py                                          # 50Hz asynchronous dual-loop edge controller
├── duck_drop.py                                     # Headless MuJoCo contact validation
├── microduck.xml                                    # Educational MJCF kinematic model
│
├── kinematics/                                      # 15-DOF 3D robot models
│   └── assets/alpha/robot_walk.xml                  # 18-geom production 3D simulation model
├── policies/                                        # Pretrained ONNX locomotion policies
│   ├── alpha_walking.onnx                           # Forward walking policy
│   ├── alpha_stand.onnx                             # Upright balance standing policy
│   └── ball_kick_left.onnx                          # Dynamic kick policy
├── images/                                          # 26 technical engineering diagrams (400x300)
└── generators/                                      # Handout and diagram generation scripts
    ├── generate_handout.py ... generate_phase6_*.py
    ├── generate_images.py ... generate_phase6_*.py
    └── bundle_handouts.py
```

---

## 📄 License & Credits
Built upon the open-source hardware and software specifications of [Pollen Robotics Microduck](https://github.com/pollen-robotics/microduck).  
Released under the MIT License.
