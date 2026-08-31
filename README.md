# 🦆 Microduck Physical AI Simulation & Masterclass

[![Live Portal](https://img.shields.io/badge/Web%20Portal-GitHub%20Pages-38bdf8?style=for-the-badge&logo=github)](https://lgtkgtv.github.io/microduck_sim/)
[![Physics Engine](https://img.shields.io/badge/Physics-MuJoCo%203.12-10b981?style=for-the-badge)](https://mujoco.org/)
[![RL Pipeline](https://img.shields.io/badge/RL-PyTorch%20%7C%20PPO-f59e0b?style=for-the-badge&logo=pytorch)](https://pytorch.org/)
[![ONNX Deployment](https://img.shields.io/badge/Inference-ONNX%20Runtime-a855f7?style=for-the-badge&logo=onnx)](https://onnxruntime.ai/)
[![Curriculum Suite](https://img.shields.io/badge/Verified-100%25%206--Phase%20Proofs-34d399?style=for-the-badge)](verify_curriculum.py)
[![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge)](LICENSE)

A self-contained **Physical AI simulation studio, Reinforcement Learning pipeline, and 6-phase interactive curriculum** for the [Pollen Robotics Microduck](https://github.com/pollen-robotics/microduck) (15-DOF bipedal robot).

This repository contains everything needed to simulate the robot in 3D physics, train locomotion policies using PPO, extract hardware-safe ONNX models, run an asynchronous 50Hz edge control loop, and teach or learn physical AI through interactive web slides and printable engineering handouts.

---

## 🧭 Understanding the Two Repositories

If you are working in the `~/agy_projects/physical_ai/` workspace, you will notice two directories:

```text
~/agy_projects/physical_ai/
├── microduck_sim/   <-- (THIS REPO) Complete Simulation, RL & Masterclass Studio
└── microduck/       <-- (UPSTREAM FIRMWARE) Official Embedded Rust Daemons for RK3566
```

### How They Differ & Work Together:

| Feature | `microduck_sim` *(This Repo)* | `microduck` *(Upstream Firmware)* |
| :--- | :--- | :--- |
| **Role** | **The Digital Twin & Learning Studio** | **The Physical Robot Firmware** |
| **Language Stack** | Python 3.12, MuJoCo, PyTorch, ONNX, HTML5/JS | Rust (`cargo` workspace), C/C++ FFI |
| **Primary Output** | 3D Interactive Simulation, Trained ONNX Policies, Web Curriculum | Compiled binary daemons (`robotd`, `duckctl`) for the Rockchip RK3566 SBC |
| **Hardware Needed?** | ❌ None (Runs 100% on your laptop / PC / WSL2) | ⚠️ Requires physical Microduck hardware |
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

The viewer ([`launch_viewer.py`](launch_viewer.py)) includes an in-frame cursor, real-time kinematics telemetry overlay, and full 3D physics interaction:

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
| **Phase 1** | **Anatomy of a Robot** | 15-DOF Kinematics, Actuators & CAN Bus | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/curriculum/phase1_anatomy.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/docs/Phase1_Anatomy_Handout.pdf) *(4 pgs)* |
| **Phase 2** | **The Invisible Matrix** | MuJoCo Physics, Forward Dynamics & Collision | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/curriculum/phase2_matrix.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/docs/Phase2_Matrix_Handout.pdf) *(3 pgs)* |
| **Phase 3** | **The Dog Trainer** | Gymnasium, Reward Functions & PPO Training | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/curriculum/phase3_dogtrainer.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/docs/Phase3_DogTrainer_Handout.pdf) *(3 pgs)* |
| **Phase 4** | **Brain Surgery** | Policy Extraction & Hardware-Safe Clamping | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/curriculum/phase4_brainsurgery.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/docs/Phase4_BrainSurgery_Handout.pdf) *(3 pgs)* |
| **Phase 5** | **The Nervous System** | 50Hz Dual-Loop Control & Real-Time Scheduling | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/curriculum/phase5_nervoussystem.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/docs/Phase5_NervousSystem_Handout.pdf) *(3 pgs)* |
| **Phase 6** | **Securing the Swarm** | A/B OTA Updates, CI Gates & ED25519 Crypto | [🚀 Launch Deck](https://lgtkgtv.github.io/microduck_sim/curriculum/phase6_securingswarm.html) | [📄 PDF Handout](https://lgtkgtv.github.io/microduck_sim/docs/Phase6_SecuringSwarm_Handout.pdf) *(3 pgs)* |

* 📘 **[Download Complete Masterclass Manual (19 Pages)](https://lgtkgtv.github.io/microduck_sim/docs/Microduck_Physical_AI_Masterclass_Complete_Book.pdf)**
* 📦 **[Download All Handouts (.ZIP)](https://lgtkgtv.github.io/microduck_sim/docs/microduck_all_handouts.zip)**

---

## 🛠️ Verification & Execution Pipeline

```text
[ Step 1: Verification ] uv run verify_curriculum.py   # Empirically prove all 6 curriculum phases
          │
          ▼
[ Step 2: Web Plumbing ] uv run verify_web_plumbing.py # Ensure 0 broken links on GitHub Pages
          │
          ▼
[ Step 3: Simulation ]   uv run duck_drop.py          # Verify MuJoCo physics & contact dynamics
          │
          ▼
[ Step 4: RL Training ]  uv run train_microduck.py    # Train PPO locomotion policy in Gymnasium
          │
          ▼
[ Step 5: Silicon Clamp] uv run export_to_onnx.py     # Extract Actor & bake [-1.0, 1.0] torque clamps
          │
          ▼
[ Step 6: Edge Control ] uv run main.py               # Run 50Hz dual-loop async controller
```

---

## 📁 Repository Directory & File Architecture

The repository is structured into modular, self-contained directories:

```text
microduck_sim/
├── index.html                                        # Mission Control Web Portal (GitHub Pages Entry)
│
├── curriculum/                                       # 6 Interactive HTML Slide Decks
│   ├── phase1_anatomy.html                           # Hardware, CAN bus & 50Hz budget
│   ├── phase2_matrix.html                            # MuJoCo MjModel vs MjData & forward dynamics
│   ├── phase3_dogtrainer.html                        # Gymnasium observation/action & PPO reward math
│   ├── phase4_brainsurgery.html                      # Actor extraction & silicon safety clamping
│   ├── phase5_nervoussystem.html                     # 50Hz asynchronous dual-loop control
│   └── phase6_securingswarm.html                     # A/B OTA updates, CI gates & cryptographic checksums
│
├── docs/                                             # High-Resolution PDF Handouts & Book
│   ├── Phase1_Anatomy_Handout.pdf ... Phase6_*.pdf   # Individual 3-4 page printable module handouts
│   ├── Microduck_Physical_AI_Masterclass_Complete_Book.pdf # Full 19-page integrated master manual
│   └── microduck_all_handouts.zip                   # Complete bundled zip archive
│
├── images/                                          # 26 Technical Engineering Diagrams
│   ├── rockchip_rk3566.png, kinematic_tree.png ...   # Used across web slides and PDF books
│
├── generators/                                      # PDF & Diagram Generation Scripts
│   ├── generate_handout.py ... generate_phase6_*.py  # ReportLab 2-column PDF compilers
│   ├── generate_images.py ... generate_phase6_*.py   # Pillow 400x300 diagram rendering engines
│   └── bundle_handouts.py                           # Merges all PDFs into the complete Master Manual
│
├── kinematics/                                      # 15-DOF 3D Robot Models
│   └── assets/alpha/robot_walk.xml                  # 18-geom production 3D simulation MJCF model
│
├── policies/                                        # Pretrained ONNX Locomotion Policies
│   ├── alpha_walking.onnx                           # Forward walking policy
│   ├── alpha_stand.onnx                             # Upright balance standing policy
│   └── ball_kick_left.onnx                          # Dynamic kick policy
│
├── launch.sh                                        # One-click native simulation launcher
├── launch_viewer.py                                 # 3D interactive viewer with HUD & cursor
├── verify_curriculum.py                             # Automated 6-phase curriculum verification suite
├── verify_web_plumbing.py                           # Automated link integrity & 404 checker
├── train_microduck.py                               # PPO Reinforcement Learning training pipeline
├── export_to_onnx.py                                # ONNX policy extractor with silicon clamping
├── main.py                                          # 50Hz asynchronous dual-loop edge controller
├── duck_drop.py                                     # Headless MuJoCo contact dynamics validation
├── microduck.xml                                    # Clean educational 15-DOF MJCF kinematic model
├── pyproject.toml                                   # Python project manifest & dependencies
└── README.md                                        # Master Documentation
```

### Detailed Subdirectory Breakdown:

| Directory / File | Description & Purpose |
| :--- | :--- |
| **[`curriculum/`](curriculum/)** | Houses the 6 interactive web slide decks. Each slide contains embedded interactive widgets, real-time formula calculators, 3D diagrams, and self-grading quizzes with local storage progress tracking. |
| **[`docs/`](docs/)** | Stores all printable course literature: the 6 individual PDF handouts, the 19-page comprehensive master manual, and student zip bundles. |
| **[`images/`](images/)** | Contains the 26 technical diagrams (400x300 PNGs) illustrating kinematics, control loops, neural network graphs, and hardware schematics. |
| **[`generators/`](generators/)** | Contains the 13 Python scripts responsible for programmatically rendering the diagram assets and compiling the PDF companion books via ReportLab and Pillow. |
| **[`kinematics/`](kinematics/)** | Contains the official 3D MJCF kinematic models (`robot_walk.xml`), defining joint limits, inertial properties, and 18 collision geometries for the Microduck. |
| **[`policies/`](policies/)** | Houses pretrained neural network policies in ONNX format (`alpha_walking.onnx`, `alpha_stand.onnx`, `ball_kick_left.onnx`, etc.) for direct execution in simulation or deployment to hardware. |
| **[`verify_curriculum.py`](verify_curriculum.py)** | Mathematical and physical test suite validating all 6 curriculum modules against actual code, forward dynamics, and neural network weights. |
| **[`verify_web_plumbing.py`](verify_web_plumbing.py)** | Automated link integrity tool that scans HTML and dynamic JavaScript routes to guarantee 0 broken links (0 404s). |
| **[`launch_viewer.py`](launch_viewer.py)** / **[`launch.sh`](launch.sh)** | The native GLFW 3D simulation viewer featuring an in-frame cursor, live telemetry HUD overlay, and 3D force/torque perturbation grabbing. |
| **[`train_microduck.py`](train_microduck.py)** | Trains bipedal locomotion policies using PPO inside a custom Gymnasium environment. |
| **[`export_to_onnx.py`](export_to_onnx.py)** | Performs "Brain Surgery": extracts the lightweight Actor network, prunes training overhead, and bakes `[-1.0, 1.0]` torque clamping into the ONNX computational graph. |
| **[`main.py`](main.py)** | Implements the 50Hz asynchronous dual-loop edge controller that decouples the 10Hz visual cortex from the 50Hz spinal reflex loop. |
| **[`microduck.xml`](microduck.xml)** | A clean, educational 15-DOF MJCF model designed for teaching kinematic chains and joint limit configurations. |

---

## 📄 License & Credits
Built upon the open-source hardware and software specifications of [Pollen Robotics Microduck](https://github.com/pollen-robotics/microduck).  
Released under the MIT License.
