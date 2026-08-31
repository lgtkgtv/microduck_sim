import os
import torch as th
from stable_baselines3 import PPO

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT_DIR = os.path.join(SCRIPT_DIR, "policies", "checkpoints")
PPO_ZIP_PATH = os.path.join(CHECKPOINT_DIR, "microduck_ppo_policy.zip")
ONNX_EXPORT_PATH = os.path.join(CHECKPOINT_DIR, "microduck_walking_policy.onnx")

# 1. Define the Edge Wrapper
class OnnxablePolicy(th.nn.Module):
    def __init__(self, extractor, action_net):
        super().__init__()
        # We only extract the 'actor' network layers, leaving the 'critic' layers behind
        self.extractor = extractor
        self.action_net = action_net

    def forward(self, observation):
        # Pass telemetry through the feature extractor
        action_hidden, _ = self.extractor(observation)
        
        # Get the deterministic target from the network
        raw_action = self.action_net(action_hidden)
        
        # CRITICAL HARDWARE SAFETY: PPO outputs unbounded continuous values. 
        # Stable Baselines3 usually clips these during training behind the scenes. 
        # By adding torch.clamp here, we bake the -1.0 to 1.0 limit directly into 
        # the ONNX silicon math, guaranteeing the robot motors never over-rotate.
        clamped_action = th.clamp(raw_action, min=-1.0, max=1.0)
        
        return clamped_action

def main():
    print(f"📦 Loading trained PPO policy from: {PPO_ZIP_PATH}")
    if not os.path.exists(PPO_ZIP_PATH):
        raise FileNotFoundError(f"Missing PPO checkpoint at {PPO_ZIP_PATH}. Run train_microduck.py first!")

    model = PPO.load(PPO_ZIP_PATH, device="cpu")
    
    # 2. Extract the PyTorch sub-modules
    onnxable_model = OnnxablePolicy(
        model.policy.mlp_extractor, 
        model.policy.action_net
    )
    
    # 3. Create a dummy tensor that matches our 4-frame sliding window (1 batch, 60 sensors)
    dummy_input = th.randn(1, 60)
    
    print(f"🏗️ Exporting to ONNX format: {ONNX_EXPORT_PATH}")
    th.onnx.export(
        onnxable_model,
        dummy_input,
        ONNX_EXPORT_PATH,
        opset_version=17, # Modern opset for broad compatibility
        input_names=["observations"],
        output_names=["actions"]
    )
    
    print(f"✅ Successfully exported '{os.path.basename(ONNX_EXPORT_PATH)}' ({os.path.getsize(ONNX_EXPORT_PATH)} bytes)!")

if __name__ == "__main__":
    main()
