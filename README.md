# 🦆 Microduck Physical AI Masterclass & Simulation Platform

[![GitHub Pages](https://img.shields.io/badge/Live%20Portal-GitHub%20Pages-38bdf8?style=for-the-badge&logo=github)](https://lgtkgtv.github.io/microduck_sim/)
[![Physics](https://img.shields.io/badge/Physics-MuJoCo%203.12-10b981?style=for-the-badge)](https://mujoco.org/)
[![RL](https://img.shields.io/badge/RL-PyTorch%20%7C%20PPO-f59e0b?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![Inference](https://img.shields.io/badge/Inference-ONNX%20Runtime-a855f7?style=for-the-badge&logo=onnx)](https://onnxruntime.ai/)
[![Daemon](https://img.shields.io/badge/Nervous%20System-Embedded%20Rust-d97706?style=for-the-badge&logo=rust)](https://www.rust-lang.org/)

An end-to-end **Physical AI architecture, training pipeline, native 3D interactive simulation, and semester-long curriculum** for the Hugging Face / Pollen Robotics Microduck (15-DOF bipedal robot). This project bridges headless physics simulation, Reinforcement Learning (PPO), surgical model extraction for hardware safety, a low-latency 50Hz asynchronous control loop, and a full interactive 3D native MuJoCo viewer optimized for WSLg and Linux.

---

## 🌐 Live Interactive Masterclass (GitHub Pages)

> 🚀 **Access the Live Student & Teacher Web Portal:**  
> **[https://lgtkgtv.github.io/microduck_sim/](https://lgtkgtv.github.io/microduck_sim/)**

Students and educators can interact with real-time physics simulations, 3D IMU gravity vectors, motor clamping limits, interactive mock CLI terminals, progression-locked curriculum modules, and skippable 5-question quizzes directly from any web browser without installation.

---

## 📚 The 6-Phase Curriculum Overview

| Phase | Module Name | Core Concept | Interactive Slide Deck | Printable Handout (PDF) |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Anatomy of a Robot** | *Puppets, Strings & The Conductor* | [🚀 Launch Phase 1](https://lgtkgtv.github.io/microduck_sim/phase1_anatomy.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase1_Anatomy_Handout.pdf) *(4 pages)* |
| **Phase 2** | **The Invisible Matrix** | *Virtual Physics Sandbox (MuJoCo)* | [🚀 Launch Phase 2](https://lgtkgtv.github.io/microduck_sim/phase2_matrix.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase2_Matrix_Handout.pdf) *(3 pages)* |
| **Phase 3** | **The Dog Trainer** | *Gym Coach & PPO Reinforcement Learning* | [🚀 Launch Phase 3](https://lgtkgtv.github.io/microduck_sim/phase3_dogtrainer.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase3_DogTrainer_Handout.pdf) *(3 pages)* |
| **Phase 4** | **Brain Surgery & Clamping** | *Actor Isolation & Hardware-Safe Clamping* | [🚀 Launch Phase 4](https://lgtkgtv.github.io/microduck_sim/phase4_brainsurgery.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase4_BrainSurgery_Handout.pdf) *(3 pages)* |
| **Phase 5** | **The Nervous System** | *Spinal Reflexes & Bare-Metal Rust Daemons* | [🚀 Launch Phase 5](https://lgtkgtv.github.io/microduck_sim/phase5_nervoussystem.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase5_NervousSystem_Handout.pdf) *(3 pages)* |
| **Phase 6** | **Securing the Swarm** | *OTA Updates, DevSecOps & Crypto Seals* | [🚀 Launch Phase 6](https://lgtkgtv.github.io/microduck_sim/phase6_securingswarm.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase6_SecuringSwarm_Handout.pdf) *(3 pages)* |

* 📘 **[Download Complete Masterclass Manual (19 Pages)](https://lgtkgtv.github.io/microduck_sim/Microduck_Physical_AI_Masterclass_Complete_Book.pdf)**
* 📦 **[Download All Handouts Bundle (.ZIP)](https://lgtkgtv.github.io/microduck_sim/microduck_all_handouts.zip)**

---

## 🎮 Native 3D Interactive MuJoCo Simulation

This repository includes a standalone, high-performance **interactive 3D MuJoCo viewer** with guaranteed in-frame cursor visibility and full physical interaction support under WSLg / Linux.

```bash
./launch.sh
```

```
=================================================================
🦆 Microduck Physical AI Native Simulation Viewer
=================================================================
Loading MJCF model from: kinematics/assets/alpha/robot_walk.xml
✅ Model and Scene loaded successfully!
  • Generalized coordinates (nq) : 21
  • Degrees of freedom (nv)      : 20
  • Number of joints (njnt)      : 15
  • Number of bodies (nbody)     : 16
  • Number of geoms (ngeom)      : 19
  • Timestep                     : 0.0020 s (500 Hz)
-----------------------------------------------------------------
```

### Interactive Controls Matrix

| Key / Mouse Action | Function | Description |
| :--- | :--- | :--- |
| `Left Click + Drag` | **Orbit Camera** | Orbit in 3D around the Microduck root body. |
| `Right Click + Drag` | **Pan Camera** | Translate the camera view plane. |
| `Scroll Wheel` | **Zoom** | Adjust camera focal distance. |
| `Ctrl + Left Drag` | **🪢 Force Perturbation** | Grab and pull the robot in 3D using dynamic spring forces (Cursor turns **Red 🔴**). |
| `Ctrl + Right Drag`| **🔄 Torque Perturbation** | Apply rotational torque perturbation to the torso. |
| `Spacebar` | **Pause / Resume** | Freeze and resume physics stepping. |
| `R` or `Backspace` | **Reset Simulation** | Reset the robot to initial height and posture. |
| `J` | **Toggle Joints** | Toggle visualization of joint rotation axes. |
| `S` | **Toggle Sites** | Toggle visual sensor sites (Camera, ToF, IMU, Feet). |
| `C` | **Toggle Contacts** | Toggle contact friction points and force vectors. |
| `I` | **Toggle Inertia** | Toggle mass distribution inertia ellipsoids. |
| `T` | **Toggle Transparency** | Toggle semi-transparent body shell mode. |
| `F` | **Toggle Floor** | Toggle floor checkerboard texture and grid. |
| `ESC` | **Quit** | Close simulation window. |

---

## 🏗️ System Architecture & Directory Alignment

```text
                                [ Physical AI Workspace ]
                                            |
         +----------------------------------+----------------------------------+
         |                                                                     |
         v                                                                     v
[ microduck_sim/ ] (This Repo)                                       [ microduck/ ] (Upstream Reference)
├── 🌐 GitHub Pages Curriculum Portal                                ├── 🦀 Embedded Rust Firmware Crates
├── 🎮 Native 3D Interactive Viewer (launch.sh)                      │    ├── robotd (50Hz Real-Time Heartbeat)
├── 🏋️ RL Training (train_microduck.py)                              │    ├── duckctl (CLI Diagnostic Tool)
├── ✂️ ONNX Clamping Pipeline (export_to_onnx.py)                    │    ├── configd / updater / mediad
├── 🏎️ 50Hz Python Async Control Loop (main.py)                      │    └── kinematics (Rust FK/IK Engine)
└── 📦 Printable PDFs & Engineering Schematics                       └── 📦 Upstream Alpha MJCF Kinematics
```

### Dual-Loop Control Hierarchy

```text
[ Visual Cortex ] (Background Thread @ 10Hz)
      RGB Camera -> PyTorch CNN -> Shared Memory (32 Latent Features)
                                           |
                                           v
[ Spinal Cord ]   (Main Thread @ 50Hz / 20ms Heartbeat)
      IMU / Encoders (15 Features) ----> [ FUSION ]
                                           |
                                  [ ONNX Actor Policy ]
                                           |
                            [ Hardware Safety Clamp (-1.0 to 1.0) ]
                                           |
                               [ 15-DOF Motor Actuation ]
```

---

## 📁 Repository Structure

```
.
├── index.html                                        # Mission Control student & teacher dashboard
├── phase1_anatomy.html                              # Phase 1 interactive slide deck (Hardware)
├── phase2_matrix.html                               # Phase 2 interactive slide deck (MuJoCo)
├── phase3_dogtrainer.html                           # Phase 3 interactive slide deck (RL / PPO)
├── phase4_brainsurgery.html                          # Phase 4 interactive slide deck (ONNX Clamping)
├── phase5_nervoussystem.html                        # Phase 5 interactive slide deck (Rust robotd)
├── phase6_securingswarm.html                        # Phase 6 interactive slide deck (DevSecOps)
├── Phase1_Anatomy_Handout.pdf                       # Phase 1 printable ReportLab handout (4 pages)
├── Phase2_Matrix_Handout.pdf                        # Phase 2 printable ReportLab handout (3 pages)
├── Phase3_DogTrainer_Handout.pdf                    # Phase 3 printable ReportLab handout (3 pages)
├── Phase4_BrainSurgery_Handout.pdf                  # Phase 4 printable ReportLab handout (3 pages)
├── Phase5_NervousSystem_Handout.pdf                 # Phase 5 printable ReportLab handout (3 pages)
├── Phase6_SecuringSwarm_Handout.pdf                 # Phase 6 printable ReportLab handout (3 pages)
├── Microduck_Physical_AI_Masterclass_Complete_Book.pdf # Combined 19-page master manual
├── microduck_all_handouts.zip                       # All 6 PDF handouts in a single ZIP bundle
├── launch.sh                                        # Native MuJoCo interactive viewer launcher
├── launch_viewer.py                                 # Full 3D GLFW simulation viewer with HUD & Cursor
├── kinematics/                                      # 15-DOF Kinematic models with 3D geometries
│   └── assets/alpha/robot_walk.xml                  # Full 18-geom production MJCF model
├── policies/                                        # Production ONNX neural locomotion policies
│   ├── alpha_walking.onnx                           # 15-DOF forward walking policy
│   ├── alpha_stand.onnx                             # Upright balance standing policy
│   └── ball_kick_left.onnx                          # Dynamic kick motion policy
├── main.py                                          # 50Hz asynchronous edge controller prototype
├── train_microduck.py                               # PPO Gymnasium training pipeline
├── export_to_onnx.py                                # Extracts and clamps policy to ONNX
├── duck_drop.py                                     # Headless MuJoCo physics validation
├── microduck.xml                                    # Educational MJCF kinematic tree model
├── images/                                          # 26 technical engineering PNG schematics (400x300)
└── .github/workflows/pages.yml                      # GitHub Actions automated Pages deployment
```

---

## 🛠️ Prerequisites & Quickstart

* **Operating System:** Ubuntu 24.04 (Natively or via Windows 11 WSL2 / WSLg).
* **Package Manager:** `uv` (Fast Python package resolver).
* **GPU:** NVIDIA GPU (e.g. RTX 5060 / 40-series) recommended for RL training and hardware rendering.

### 1. Clone & Setup Environment
```bash
# Clone the repository
git clone https://github.com/lgtkgtv/microduck_sim.git
cd microduck_sim

# Install dependencies via uv
uv sync
```

### 2. Install System Graphics Libraries (WSLg / Linux)
```bash
sudo apt-get update
sudo apt-get install -y libglfw3 libglew-dev libgl1 libgl1-mesa-dev libosmesa6 x11-xserver-utils
```

### 3. Launch Interactive 3D Simulation Viewer
```bash
./launch.sh
```

### 4. Run the Curriculum Web Server (Offline Classroom Mode)
```bash
uv run python -m http.server 8000
```
Open `http://localhost:8000` in any browser to access the local portal.

### 5. Train & Export Locomotion Policy
```bash
# Step 1: Train PPO Actor-Critic policy in MuJoCo
uv run train_microduck.py

# Step 2: Extract Actor and bake silicon safety clamps
uv run export_to_onnx.py

# Step 3: Run the 50Hz edge controller
uv run main.py
```

---

## 📄 License & Credits
Built upon the open-source hardware and software specifications of [Pollen Robotics Microduck](https://github.com/pollen-robotics/microduck).
Released under the MIT License.
