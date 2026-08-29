import time
import json
import random
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# 1. Load the environment variables
env_path = Path.home() / "agy_projects" / ".env"
load_dotenv(dotenv_path=env_path)

# 2. Initialize the client
client = genai.Client()

class MicroduckAction(BaseModel):
    motor_velocities: list[float] = Field(
        description=(
            "Exactly 15 floating-point values bounded strictly between -1.0 and 1.0. "
            "Indexes [0:5] control the Left Leg. "
            "Indexes [5:10] control the Right Leg. "
            "Indexes [10:15] control the Neck & Head."
        )
    )

def generate_mock_telemetry():
    return {
        "imu_pitch": round(random.uniform(-15.0, 15.0), 2),
        "imu_roll": round(random.uniform(-5.0, 5.0), 2),
        "left_foot_contact": random.choice([True, False]),
        "right_foot_contact": random.choice([True, False]),
        "current_joint_angles": [round(random.uniform(-0.5, 0.5), 2) for _ in range(15)]
    }

def main():
    print("🦆 Starting Microduck 50Hz Simulation Loop...")
    print("🧠 Initializing Temporal Memory (Chat Session)...")
    print("---------------------------------------------")
    
    # 3. FIX: Initialize a Chat session instead of single-shot generation
    chat = client.chats.create(model='gemini-2.5-flash')
    
    target_hz = 50
    tick_time = 1.0 / target_hz
    
    for tick in range(1, 4):
        start_time = time.time()
        
        telemetry = generate_mock_telemetry()
        telemetry_str = json.dumps(telemetry)
        
        # We no longer need to repeat the persona setup every time, 
        # just feed it the raw telemetry delta.
        prompt = f"Current telemetry: {telemetry_str}. Stabilize."
        
        try:
            print(f"Tick {tick:02d} | IMU Pitch: {telemetry['imu_pitch']:>6.2f} | Sending to Chat...")
            
            # 4. FIX: Use chat.send_message instead of models.generate_content
            response = chat.send_message(
                prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MicroduckAction,
                    temperature=0.1,
                ),
            )
            
            action = response.parsed
            velocities = action.motor_velocities
            
            if not velocities or len(velocities) != 15:
                raise ValueError(f"Expected 15 velocities, got {len(velocities) if velocities else 0}")
                
            left_leg  = [max(-1.0, min(1.0, v)) for v in velocities[0:5]]
            right_leg = [max(-1.0, min(1.0, v)) for v in velocities[5:10]]
            neck_head = [max(-1.0, min(1.0, v)) for v in velocities[10:15]]
            
            print(f"  [+] Success! Left Leg  : {[round(v, 2) for v in left_leg]}")
            print(f"               Right Leg : {[round(v, 2) for v in right_leg]}")
            print(f"               Neck/Head : {[round(v, 2) for v in neck_head]}")
            
        except Exception as e:
            print(f"  [-] API Glitch or Parsing Error: {e}")
            print("  [-] Applying hardware fail-safe: Zeroing all motor velocities.")
            
        print("-" * 45)
        
        elapsed = time.time() - start_time
        sleep_time = max(0.0, tick_time - elapsed)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
