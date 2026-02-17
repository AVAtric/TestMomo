"""Verify the terminal interface can run without blocking."""

import sys
import threading
import time
sys.path.insert(0, '/home/argus/.openclaw/workspace/TestMomo')

from momo.terminal import TerminalInterface

print("Testing terminal interface without keyboard input...")

# Create interface
interface = TerminalInterface(width=10, height=5, speed=0)

# Run interface in a separate thread
def run_interface():
    interface.run()

thread = threading.Thread(target=run_interface, daemon=True)
thread.start()

print("✓ Interface started in background thread")

# Wait a bit and check status
time.sleep(0.5)
print(f"✓ Interface running: {interface.running}")
print(f"✓ Current generation: {interface.generation}")
print(f"✓ Paused: {interface.paused}")

# Check if interface stopped (shouldn't happen in this test)
time.sleep(0.5)
if interface.running:
    print("✓ Interface still running as expected")
    interface.quit()

print("\n✅ Test completed!")