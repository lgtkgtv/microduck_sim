import os
import time
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT_DIR = os.path.join(SCRIPT_DIR, "policies", "checkpoints")
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
MODEL_SAVE_PATH = os.path.join(CHECKPOINT_DIR, "microduck_ppo_policy")

# 1. Define the Custom Gymnasium Environment
class MicroduckEnv(gym.Env):
    def __init__(self):
        super(MicroduckEnv, self).__init__()
        
        # Action Space: 15 motors, values clamped between -1.0 and 1.0
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(15,), dtype=np.float32)
        
        # Observation Space: 60 sensor readings (4 frames * 15 sensors)
        self.observation_space = gym.spaces.Box(low=-50.0, high=50.0, shape=(60,), dtype=np.float32)
        
        self.state = None
        self.steps = 0

    def reset(self, seed=None, options=None):
        """Resets the simulation after the robot falls."""
        # Seeding is required by the modern Gymnasium API
        super().reset(seed=seed)
        
        self.state = np.random.uniform(-0.1, 0.1, 60).astype(np.float32)
        self.steps = 0
        
        info = {} # Gymnasium requires returning an info dictionary
        return self.state, info

    def step(self, action):
        """Executes one 50Hz tick in the physics engine."""
        self.steps += 1
        
        # Get new mock sensor data
        self.state = np.random.uniform(-0.1, 0.1, 60).astype(np.float32)
        
        reward = 1.0 
        
        # Gymnasium split "done" into terminated (failure) and truncated (time limit)
        terminated = False 
        truncated = bool(self.steps >= 100) 
        
        info = {}
        
        return self.state, reward, terminated, truncated, info

def main():
    print("🥊 Initializing the MuJoCo RL Training Gym...")
    
    env = MicroduckEnv()
    # This checker will now pass successfully!
    check_env(env, warn=True)
    
    print("🧠 Creating the PPO Neural Network...")
    model = PPO("MlpPolicy", env, verbose=1)
    
    print("🏃 Starting the 10,000 timestep training run...")
    model.learn(total_timesteps=10000)
    
    print(f"💾 Saving the trained policy to {MODEL_SAVE_PATH}.zip...")
    model.save(MODEL_SAVE_PATH)
    print("✅ Training complete!")

if __name__ == "__main__":
    main()
