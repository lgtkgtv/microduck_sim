<div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 5px solid #ff9900;">
  <h1 style="color: #333333; margin-top: 0;">🦆 Quickstart for Physical AI: Microduck Simulation</h1>
  <p style="color: #666666; font-size: 1.1em;">An interactive masterclass for building a 50Hz low-latency bipedal control loop using MuJoCo, PyTorch, and ONNX on Ubuntu WSL2.</p>
</div>

<br>

## Module 1: The Sandbox (MuJoCo & Headless Simulation)

Imagine you have a magic, invisible box. Inside this box, gravity exists, objects have weight, and things crash into each other. But none of it is real—it is entirely made of math. This is **MuJoCo** (Multi-Joint dynamics with Contact). 

When we train a robot like the Microduck, we don't start with physical metal and plastic. If a physical robot falls 10,000 times while learning to walk, its motors will burn out and its 3D-printed joints will snap. In our MuJoCo "Sandbox," the robot can fall a million times in an hour, and it costs us nothing.

| Concept                  | The Sandbox Analogy                      | The Engineering Reality                  |
|:-------------------------|:-----------------------------------------|:-----------------------------------------|
| **Physical AI**          | Giving a smart brain to a physical toy.  | Embodied AI models executing physically. |
| **Hugging Face LeRobot** | A community recipe book for robot tricks.| An open-source robotics AI library.      |
| **The Microduck**        | A 25cm tall duck robot you can train.    | A $399 15-DOF bipedal hardware platform. |
| **Telemetry (State)**    | The inner ear and the skin.              | Real-time IMU and joint encoder data.    |

### The Two Halves of the Universe
*   **The Model (`MjModel`):** The blueprint. The immutable physics rules of your world.
*   **The Data (`MjData`):** The live state. The numbers that constantly change (position, velocity).

<div style="background-color: #e6f2ff; padding: 15px; border-radius: 5px;">
  <h4 style="margin-top: 0; color: #0055cc;">⚙️ Core Execution: The Step Loop</h4>
  <p style="margin-bottom: 0;">Nothing happens in MuJoCo until we tell time to move forward by calling <code>mujoco.mj_step(model, data)</code>. The engine actively calculates momentum and acceleration with every step.</p>
</div>

---

## Module 2: The Gym (Reinforcement Learning & PPO)

If you want a dog to sit, you don't grab its legs, calculate joint angles, and manually bend its knees. Instead, you hold up a treat, wait for the dog to figure out the muscle movements, and then give the treat when it succeeds. This is **Reinforcement Learning (RL)**. 

### The Gym Rules (State, Action, Reward)

| Rule                        | The Dog Analogy                    | The Python Equivalent                                  |
|:----------------------------|:-----------------------------------|:-------------------------------------------------------|
| **1. Observation Space**    | What the dog sees and hears.       | `observation_space` (60 float values for sensors).     |
| **2. Action Space**         | What muscles the dog can move.     | `action_space` (15 float values between -1.0 and 1.0). |
| **3. Reward**               | The dog biscuit.                   | `reward` (+1 point for staying up, 0 for falling).     |

### Proximal Policy Optimization (PPO)
PPO acts as both a **Coach (Critic)** and a **Gymnast (Actor)**. The Coach predicts the score based on sensors, while the Gymnast fires the motors. PPO ensures the Gymnast learns safely, limiting drastic weight changes so it doesn't "forget" how to walk after a single mistake.

---

## Module 3: The Brain Surgery (ONNX Export & Clamping)

When training finishes, we get a heavy PyTorch system. We cannot put this on the Microduck because it calculates unnecessary data (the Coach) and produces unbounded numbers that could destroy physical motors.

<div style="background-color: #ffebe6; padding: 15px; border-radius: 5px;">
  <h4 style="margin-top: 0; color: #cc3300;">🛡️ Hardware Safety Clamping</h4>
  <p style="margin-bottom: 0;">By baking <code>torch.clamp(raw_motor_guess, min=-1.0, max=1.0)</code> directly into the computational graph, we guarantee mathematical safety in silicon. The ONNX model will never output a signal that exceeds physical hardware limits.</p>
</div>

| Library                  | Role in our Stack                              | 12-Year-Old Analogy                        |
|:-------------------------|:-----------------------------------------------|:-------------------------------------------|
| `torch`                  | Designs and trains the neural network.         | The Teacher (teaches the brain).           |
| `onnxscript`             | Translates PyTorch math into ONNX format.      | The Translator (writes the rules).         |
| `onnxruntime`            | Executes the ONNX file locally on the edge.    | The Athlete (runs the reflexes).           |

---

## Module 4: The Reflex Loop (Temporal Memory & 50Hz Control)

A robot cannot balance on a single frame of data; it needs to understand momentum. However, infinite memory (like a chatbot context window) causes latency explosions.

### The Sliding Window
We use a fixed-size `deque(maxlen=4)`. When a new sensor frame arrives, it slides in, and the oldest frame falls out. The AI always processes exactly 60 data points (4 frames × 15 sensors). 

### The 50Hz Heartbeat
Our control loop must run 50 times a second. `1 second / 50 = 20 milliseconds`. 
If ONNX inference takes 2ms on your local hardware, the script explicitly sleeps for the remaining 18ms to ensure perfect cadence.

---

## Module 5: The Anatomy (URDF & MJCF Blueprints)

To put our virtual brain into a physical body, the physics engine needs an XML blueprint (URDF/MJCF) defining the robot.

1. **The Bones (`<joint>`):** Invisible pivot points defining how parts connect and rotate.
2. **The Flesh (`<geom>`):** Physical shapes, weight, and friction properties.
3. **The Muscles (`<actuator>`):** The electrical motors. 

```xml
<!-- Example of a hardware safety limit defined in the MJCF blueprint -->
<default>
  <motor ctrlrange="-1.0 1.0" ctrllimited="true"/> 
</default>





---


---

Converting a URDF to an MJCF is the "Google Translate" of robotics. Hardware manufacturers almost always provide URDF files because they are universally accepted, but URDFs lack the physics depth (like motors, friction, and soft contacts) required for advanced AI training.

Fortunately, DeepMind built a native translator directly into MuJoCo.

Here is how you perform the conversion in your `uv` environment, along with the most critical "gotcha" in the process.

## The Two-Step Conversion Strategy

There are two ways to do this. We will use the **Wrapper Method** because it is the industry standard for Physical AI.

Instead of permanently altering the manufacturer's original URDF, we create an MJCF "wrapper" that dynamically imports the URDF and injects our custom physics rules and motors on top of it.

### Step 1: Create the Wrapper MJCF

Imagine the manufacturer gave you a file named `microduck_vendor.urdf` that only contains the bones and weight of the robot.

Create a new file named `microduck_wrapper.xml` and use the `<include>` tag. This tells MuJoCo to load the URDF, apply a compiler to optimize the meshes, and then attach the motors that the URDF format fundamentally lacks.

```xml
<mujoco model="microduck_optimized">
  <!-- 1. The Compiler: Optimizes the imported URDF for MuJoCo -->
  <compiler angle="radian" meshdir="meshes/" autolimits="true"/>
  
  <!-- 2. The Import: Bring in the manufacturer's raw URDF -->
  <include file="microduck_vendor.urdf"/>
  
  <!-- 3. The Injection: Add MuJoCo-specific physics and hardware safety -->
  <default>
    <motor ctrlrange="-1.0 1.0" ctrllimited="true"/> 
  </default>
  
  <!-- 4. The Muscles: URDF doesn't have motors, so we add them here -->
  <actuator>
    <motor joint="l_hip_yaw" name="motor_l0"/>
    <motor joint="r_hip_yaw" name="motor_r0"/>
    <!-- ... rest of your 15 motors ... -->
  </actuator>
</mujoco>

```

### Step 2: The Python Compiler Script

Now, we write a quick Python script to process this wrapper. When MuJoCo loads a wrapper, it automatically merges the URDF and the MJCF into a single, highly optimized mathematical graph in its memory.

We can then command MuJoCo to dump that merged memory out into a single, clean, finalized MJCF file.

Create a file named `compile_urdf.py`:

```python
import mujoco

def main():
    print("🔄 Loading the URDF through the MJCF Wrapper...")
    
    # 1. Load the wrapper (which automatically pulls in the URDF)
    # Note: This assumes you have a mock 'microduck_vendor.urdf' in the same folder
    try:
        model = mujoco.MjModel.from_xml_path("microduck_wrapper.xml")
    except Exception as e:
        print(f"[-] Error loading model: {e}")
        print("[!] Ensure you have the vendor URDF and mesh files in the correct directory.")
        return

    print("✅ Successfully compiled the URDF into MuJoCo's memory.")
    
    # 2. Dump the highly optimized, merged model into a final MJCF file
    output_filename = "microduck_final_compiled.xml"
    mujoco.mj_saveLastXML(output_filename, model)
    
    print(f"💾 Saved the fully optimized MJCF as: {output_filename}")
    
    # 3. Quick sanity check
    print("-" * 40)
    print("🔍 Final Compiled Hardware Check:")
    print(f"   Joints imported from URDF: {model.njnt}")
    print(f"   Motors injected from MJCF: {model.nu}")
    print("-" * 40)

if __name__ == "__main__":
    main()

```

## The "Gotcha": Autolimits and Inertia

When you run this conversion on a real manufacturer's URDF, you will often see warnings in your terminal about "inertia" or "joint limits."

Because URDF was originally built for moving data rather than simulating physics, manufacturers sometimes leave the physical mass or friction values blank, or set them to `0.0`. If a robot's leg weighs `0.0` kg, the physics engine will divide by zero and the simulation will explode (the duck will vanish into the sky at infinite speed).

MuJoCo's `<compiler>` tag acts as an automated mechanic. By adding `autolimits="true"`, MuJoCo will automatically scan the imported URDF for missing physics data, infer the correct values based on the volume of the 3D meshes, and quietly fix the math before saving the final MJCF.
