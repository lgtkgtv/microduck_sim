import os
import time
import numpy as np
import onnxruntime as ort
from collections import deque

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT_ONNX = os.path.join(SCRIPT_DIR, "policies", "checkpoints", "microduck_walking_policy.onnx")
PRODUCTION_ONNX = os.path.join(SCRIPT_DIR, "policies", "alpha_walking.onnx")

def main():
    print("🦆 Starting Microduck Local Edge Simulation...")
    
    # 1. Load the frozen neural network locally (No API Keys, no cloud!)
    policy_to_load = None
    if os.path.exists(CHECKPOINT_ONNX):
        policy_to_load = CHECKPOINT_ONNX
    elif os.path.exists(PRODUCTION_ONNX):
        policy_to_load = PRODUCTION_ONNX

    if not policy_to_load:
        print("Note: No ONNX policy found. Run export_to_onnx.py first!")
        return

    print(f"🧠 Loading ONNX Brain: {os.path.relpath(policy_to_load, SCRIPT_DIR)}")
    session = ort.InferenceSession(policy_to_load)
    input_meta = session.get_inputs()[0]
    input_name = input_meta.name
    expected_dim = input_meta.shape[1] if len(input_meta.shape) > 1 else 60
        
    # 2. Create the Sliding Window Memory Buffer
    # We will only remember the last 4 ticks of telemetry (Fixed size = no explosion)
    memory_buffer = deque(maxlen=4)
    
    # Pre-fill the buffer with zero-state so we don't crash on tick 1
    for _ in range(4):
        memory_buffer.append(np.zeros(15, dtype=np.float32))

    target_hz = 50
    tick_time = 1.0 / target_hz
    
    for tick in range(1, 25): # Run 25 edge steps (~500ms)
        start_time = time.time()
        
        # Sense: Get current state (mocked as 15 float values from sensors)
        current_telemetry = np.random.uniform(-0.1, 0.1, 15).astype(np.float32)
        
        # Add to memory (Oldest state is automatically pushed out)
        memory_buffer.append(current_telemetry)
        
        # Flatten memory
        flattened = np.concatenate(memory_buffer)
        if len(flattened) < expected_dim:
            # Pad if policy expects larger observation (e.g. 61)
            padded = np.zeros(expected_dim, dtype=np.float32)
            padded[:len(flattened)] = flattened
            observation_tensor = padded.reshape(1, -1)
        else:
            observation_tensor = flattened[:expected_dim].reshape(1, -1).astype(np.float32)
        
        # Think: Run the local ONNX policy on your WSL2 GPU/CPU (< 2ms)
        action = session.run(None, {input_name: observation_tensor})[0]
        
        # Act: Pass motor targets to the hardware
        velocities = action[0] 
        print(f"Tick {tick:03d} | Edge Inference OK | Target Velocity [0]: {velocities[0]:+.3f}")
        
        # Maintain 50Hz
        elapsed = time.time() - start_time
        time.sleep(max(0.0, tick_time - elapsed))

    print("✅ 50Hz Edge loop demonstration completed successfully!")

if __name__ == "__main__":
    main()
