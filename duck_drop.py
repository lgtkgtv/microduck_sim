import time
import mujoco

# 1. The MJCF (MuJoCo XML) String
# This is how we define the physical world. 
# We create a red floor and a floating yellow "duck body" (a capsule) 1 meter in the air.
xml_string = """
<mujoco>
  <worldbody>
    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
    <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>
    <body name="duck_body" pos="0 0 1">
      <joint type="free"/>
      <geom type="capsule" size="0.1 0.2" rgba="1 .8 .2 1" mass="0.8"/>
    </body>
  </worldbody>
</mujoco>
"""

def main():
    print("🌍 Loading MuJoCo Physics Sandbox...")
    
    # 2. Model: The blueprint of the world (from our XML)
    model = mujoco.MjModel.from_xml_string(xml_string)
    
    # 3. Data: The live, changing state (like position and velocity)
    data = mujoco.MjData(model)
    
    print("🦆 Dropping the mock duck. Watch its Z-axis height decrease!")
    print("-" * 50)
    
    # 4. The Simulation Loop (Headless - Pure Math!)
    for i in range(25):
        # Tell the physics engine to step forward in time by 2 milliseconds
        mujoco.mj_step(model, data)
        
        # Get the Z-axis height of the duck_body
        # qpos (position array) for a free joint holds [X, Y, Z, and 4 rotation values]
        duck_height = data.qpos[2] 
        
        print(f"Tick {i:02d} | Mock Duck Altitude: {duck_height:.4f} meters")
        time.sleep(0.05) # Slowing down the terminal loop so we can read it
        
    print("-" * 50)
    print("✅ Physics engine is running perfectly. Gravity works!")

if __name__ == "__main__":
    main()
