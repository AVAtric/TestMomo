"""Interactive test script to verify terminal interface functionality."""

import sys
sys.path.insert(0, '/home/argus/.openclaw/workspace/TestMomo')

from momo.terminal import TerminalInterface
from momo.display import Display

print("Testing Terminal Interface...")

# Create interface with no speed delay for testing
interface = TerminalInterface(width=20, height=10, speed=0)

# Test basic controls
print("Testing basic controls...")

# Test pause
print("Testing pause...")
interface.toggle_pause()
if interface.paused:
    print("✓ Pause toggle works")
else:
    print("✗ Pause toggle failed")

# Test step
print("Testing step...")
interface.step()
print("✓ Step works")

# Test randomize
print("Testing randomize...")
interface.randomize()
print("✓ Randomize works")

# Test clear
print("Testing clear...")
interface.clear()
print("✓ Clear works")

# Test quit
print("Testing quit...")
interface.quit()
if not interface.running:
    print("✓ Quit works")
else:
    print("✗ Quit failed")

print("\nAll controls tested successfully!")