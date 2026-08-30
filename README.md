# 🦆 Microduck Physical AI Masterclass & Edge Control Loop

[![GitHub Pages](https://img.shields.io/badge/Live%20Portal-GitHub%20Pages-38bdf8?style=for-the-badge&logo=github)](https://lgtkgtv.github.io/microduck_sim/)
[![Physics](https://img.shields.io/badge/Physics-MuJoCo%203.12-10b981?style=for-the-badge)](https://mujoco.org/)
[![RL](https://img.shields.io/badge/RL-PyTorch%20%7C%20PPO-f59e0b?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![Inference](https://img.shields.io/badge/Inference-ONNX%20Runtime-a855f7?style=for-the-badge&logo=onnx)](https://onnxruntime.ai/)
[![Daemon](https://img.shields.io/badge/Nervous%20System-Embedded%20Rust-d97706?style=for-the-badge&logo=rust)](https://www.rust-lang.org/)

An end-to-end **Physical AI architecture, training pipeline, and semester-long curriculum** for the Hugging Face / Pollen Robotics Microduck (15-DOF bipedal robot). This project bridges headless physics simulation, Reinforcement Learning (PPO), surgical model extraction for hardware safety, and a low-latency 50Hz asynchronous control loop deployed via bare-metal Rust daemons on the Rockchip RK3566 edge processor.

---

## 🌐 Live Interactive Masterclass (GitHub Pages)

> 🚀 **Access the Live Student & Teacher Web Portal:**  
> **[https://lgtkgtv.github.io/microduck_sim/](https://lgtkgtv.github.io/microduck_sim/)**

Students and educators can interact with real-time physics simulations, 3D IMU gravity vectors, motor clamping limits, interactive mock CLI terminals, and skippable 5-question quizzes directly from any web browser without installation.

---

## 📚 The 6-Phase Curriculum Overview

| Phase | Module Name | The 12YO Concept | Interactive Slide Deck | Printable Handout (PDF) |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Anatomy of a Robot** | *Puppets, Strings & The Conductor* | [🚀 Launch Phase 1](https://lgtkgtv.github.io/microduck_sim/phase1_anatomy.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase1_Anatomy_Handout.pdf) *(4 pages)* |
| **Phase 2** | **The Invisible Matrix** | *Virtual Physics Sandbox* | [🚀 Launch Phase 2](https://lgtkgtv.github.io/microduck_sim/phase2_matrix.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase2_Matrix_Handout.pdf) *(3 pages)* |
| **Phase 3** | **The Dog Trainer** | *Digital Treats & The Gym Coach* | [🚀 Launch Phase 3](https://lgtkgtv.github.io/microduck_sim/phase3_dogtrainer.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase3_DogTrainer_Handout.pdf) *(3 pages)* |
| **Phase 4** | **Brain Surgery & Clamping** | *Firing Coach & Bowling Bumpers* | [🚀 Launch Phase 4](https://lgtkgtv.github.io/microduck_sim/phase4_brainsurgery.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase4_BrainSurgery_Handout.pdf) *(3 pages)* |
| **Phase 5** | **The Nervous System** | *Spinal Reflexes & Library Rules* | [🚀 Launch Phase 5](https://lgtkgtv.github.io/microduck_sim/phase5_nervoussystem.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase5_NervousSystem_Handout.pdf) *(3 pages)* |
| **Phase 6** | **Securing the Swarm** | *Matrix Skills & Royal Wax Seals* | [🚀 Launch Phase 6](https://lgtkgtv.github.io/microduck_sim/phase6_securingswarm.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/Phase6_SecuringSwarm_Handout.pdf) *(3 pages)* |

* 📘 **[Download Complete Masterclass Manual (19 Pages)](https://lgtkgtv.github.io/microduck_sim/Microduck_Physical_AI_Masterclass_Complete_Book.pdf)**
* 📦 **[Download All Handouts Bundle (.ZIP)](https://lgtkgtv.github.io/microduck_sim/microduck_all_handouts.zip)**

---

## 🏗️ Architecture Overview

This project implements a biological **"Dual-Loop" sensor fusion architecture**, decoupling heavy visual perception from the mission-critical, low-latency 50Hz balance heartbeat.

```text
[ Visual Cortex ] (Background Thread @ 10Hz)
      RGB Camera -> PyTorch CNN -> Shared Memory (32 Features)
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

### Key Technical Highlights
1. **Headless MuJoCo Simulation:** Mathematically accurate physics execution with joint DAG kinematic trees and soft-contact friction cones.
2. **PPO Reinforcement Learning:** Custom Gymnasium environment balancing forward velocity bonuses against high-frequency torque/jerk penalties.
3. **Hardware-Safe Silicon Clamping:** Surgical isolation of the 35KB Actor policy with `torch.clamp()` baked into the ONNX graph to mathematically prevent gear stripping.
4. **Embedded Rust Nervous System:** Bare-metal `robotd` daemon running at 50Hz under `SCHED_FIFO` real-time scheduling with zero garbage collection pauses.
5. **Swarm DevSecOps:** A/B atomic OTA firmware updates with `updaterd`, 1,000-seed headless MuJoCo CI gates, and ED25519 cryptographic model signing.

---

## 📁 Repository Structure

```
.
├── index.html                                        # Main GitHub Pages student & teacher portal
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
├── Microduck_Physical_AI_Masterclass_Complete_Book.pdf # Combined 19-page masterclass manual
├── microduck_all_handouts.zip                       # All 6 PDF handouts in a single ZIP bundle
├── generate_handout.py                              # ReportLab PDF generator for Phase 1
├── generate_phase2_handout.py                       # ReportLab PDF generator for Phase 2
├── generate_phase3_handout.py                       # ReportLab PDF generator for Phase 3
├── generate_phase4_handout.py                       # ReportLab PDF generator for Phase 4
├── generate_phase5_handout.py                       # ReportLab PDF generator for Phase 5
├── generate_phase6_handout.py                       # ReportLab PDF generator for Phase 6
├── generate_images.py                               # Pillow schematic generator for Phase 1
├── generate_phase2_images.py                        # Pillow schematic generator for Phase 2
├── generate_phase3_images.py                        # Pillow schematic generator for Phase 3
├── generate_phase4_images.py                        # Pillow schematic generator for Phase 4
├── generate_phase5_images.py                        # Pillow schematic generator for Phase 5
├── generate_phase6_images.py                        # Pillow schematic generator for Phase 6
├── bundle_handouts.py                               # Merges all PDFs and builds ZIP bundle
├── images/                                          # 26 technical engineering PNG schematics (400x300)
├── main.py                                          # 50Hz asynchronous edge controller
├── train_microduck.py                               # PPO Gymnasium training pipeline
├── export_to_onnx.py                                # Extracts and clamps policy to ONNX
├── duck_drop.py                                     # Headless MuJoCo physics validation
├── microduck.xml                                    # MJCF kinematic tree & actuator definition
├── microduck_vision.xml                             # Extended MJCF with 60° FOV RGB camera
└── .github/workflows/pages.yml                      # GitHub Actions automated Pages deployment
```

---

## 🛠️ Prerequisites & Installation

* **Operating System:** Ubuntu 24.04 (Natively or via Windows 11 WSL2).
* **Package Manager:** `uv` (Fast Python package resolver).
* **Compute:** NVIDIA GPU (e.g. RTX 5060 / 40-series) recommended for RL training.

### 1. Clone & Setup Environment
```bash
# Clone the repository
git clone https://github.com/lgtkgtv/microduck_sim.git
cd microduck_sim

# Initialize uv and install dependencies
uv sync
```

### 2. Install System Graphics Libraries (MuJoCo Headless)
```bash
sudo apt-get update
sudo apt-get install -y libglfw3 libglew-dev libgl1 libgl1-mesa-dev libosmesa6
```

---

## 🚀 Running the Pipeline

### 1. Launch the Interactive Classroom Server
To run the interactive slides and portal completely offline in a classroom or lab:
```bash
uv run python -m http.server 8000
```
Open `http://localhost:8000` in your web browser.

### 2. Verify MuJoCo Headless Physics
```bash
uv run duck_drop.py
```

### 3. Train the Locomotion Policy (PPO)
```bash
uv run train_microduck.py
```

### 4. Extract Reflexes & Bake Silicon Safety Clamps
```bash
uv run export_to_onnx.py
```

### 5. Execute the 50Hz Edge Control Loop
```bash
uv run main.py
```

### 6. Rebuild All Handouts & PDFs
```bash
uv run python bundle_handouts.py
```

---

## 📄 License & Credits
Built upon the open-source hardware and software specifications of [Pollen Robotics Microduck](https://github.com/pollen-robotics/microduck).
Released under the MIT License.
