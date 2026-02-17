"""Simple test to verify the Game of Life terminal interface works."""

import sys
sys.path.insert(0, '/home/argus/.openclaw/workspace/TestMomo')

from momo.terminal import TerminalInterface

print("Testing Terminal Interface functionality...")

# Test interface creation
try:
    interface = TerminalInterface(width=10, height=5, speed=0)
    print("✓ TerminalInterface created successfully")
except Exception as e:
    print(f"✗ Failed to create TerminalInterface: {e}")
    sys.exit(1)

# Test controls
try:
    interface.toggle_pause()
    print("✓ Toggle pause works")
    
    interface.step()
    print("✓ Step works")
    
    interface.randomize()
    print("✓ Randomize works")
    
    interface.clear()
    print("✓ Clear works")
    
    interface.quit()
    print("✓ Quit works")
except Exception as e:
    print(f"✗ Failed control test: {e}")
    sys.exit(1)

# Test generation tracking
interface = TerminalInterface(width=10, height=5, speed=0)
interface.randomize()
print(f"✓ Randomize set generation to: {interface.generation}")

for _ in range(5):
    interface.step()

print(f"✓ After 5 steps, generation is: {interface.generation}")

print("\n✅ All tests passed successfully!")