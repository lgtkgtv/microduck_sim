import torch
import torch.nn as nn

class MicroduckPolicy(nn.Module):
    def __init__(self):
        super().__init__()
        # Input: 60 telemetry points (4 frames * 15 sensors)
        # Output: 15 motor velocities
        self.network = nn.Sequential(
            nn.Linear(60, 32),
            nn.ReLU(),
            nn.Linear(32, 15),
            nn.Tanh() # Tanh is crucial: it strictly bounds outputs between -1.0 and 1.0!
        )

    def forward(self, observations):
        return self.network(observations)

def main():
    print("🧠 Building an untrained synthetic brain...")
    model = MicroduckPolicy()
    
    # To export to ONNX, PyTorch needs a sample input to trace the math graph
    sample_input = torch.randn(1, 60)
    
    # Freeze and export the model
    torch.onnx.export(
        model,                      # The PyTorch model
        sample_input,               # The sample data
        "microduck_walking_policy.onnx", # The output edge file
        input_names=["observations"],    # Name of the input node
        output_names=["actions"]         # Name of the output node
    )
    print("✅ Successfully exported 'microduck_walking_policy.onnx'!")

if __name__ == "__main__":
    main()
