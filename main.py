import time
import numpy as np
import onnxruntime as ort
from collections import deque

def main():
    print("🦆 Starting Microduck Local Edge Simulation...")
    
    # 1. Load the frozen neural network locally (No API Keys, no cloud!)
    # (Assuming you downloaded the microduck_walking_policy.onnx from Hugging Face)
    try:
        session = ort.InferenceSession("microduck_walking_policy.onnx")
    except Exception:
        print("Note: 'microduck_walking_policy.onnx' not found. This is structural mock code.")
        return
        
    # 2. Create the Sliding Window Memory Buffer
    # We will only remember the last 4 ticks of telemetry (Fixed size = no explosion)
    memory_buffer = deque(maxlen=4)
    
    # Pre-fill the buffer with zero-state so we don't crash on tick 1
    for _ in range(4):
        memory_buffer.append(np.zeros(15, dtype=np.float32))

    target_hz = 50
    tick_time = 1.0 / target_hz
    
    for tick in range(1, 100): # We can run this forever now!
        start_time = time.time()
        
        # Sense: Get current state (mocked as 15 float values from sensors)
        current_telemetry = np.random.uniform(-0.1, 0.1, 15).astype(np.float32)
        
        # Add to memory (Oldest state is automatically pushed out)
        memory_buffer.append(current_telemetry)
        
        # Flatten our 4 frames of memory into a single fixed tensor array
        # Shape: (1, 60) -> 1 batch, 4 frames * 15 sensors
        observation_tensor = np.concatenate(memory_buffer).reshape(1, -1)
        
        # Think: Run the local ONNX policy on your WSL2 GPU/CPU
        # Inference latency here is typically < 2ms!
        action = session.run(None, {"observations": observation_tensor})[0]
        
        # Act: Pass the 15 motor targets to the hardware
        velocities = action[0] 
        print(f"Tick {tick:03d} | Local Edge Inference | Target Velocity [0]: {velocities[0]:.2f}")
        
        # Maintain 50Hz
        elapsed = time.time() - start_time
        time.sleep(max(0.0, tick_time - elapsed))

if __name__ == "__main__":
    main()
