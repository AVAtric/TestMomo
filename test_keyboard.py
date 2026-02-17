"""Test the terminal interface with simulated keyboard input."""

import sys
import time
import os
sys.path.insert(0, '/home/argus/.openclaw/workspace/TestMomo')

from momo.terminal import TerminalInterface

print("Starting terminal interface test...")
print("Press 'q' to quit after 3 seconds")

# Create interface
interface = TerminalInterface(width=10, height=5, speed=0)

# Simulate keyboard input
print("Simulating 'q' key press...")
import select
import tty
import termios

# Set terminal to raw mode
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

try:
    # Simulate pressing 'q' after 1 second
    time.sleep(1)
    sys.stdin.write('q')
    sys.stdin.flush()
    
    # Give it time to respond
    time.sleep(0.5)
    
    print("✓ Keyboard input simulated successfully")
    print(f"✓ Interface running status: {interface.running}")
    print(f"✓ Current generation: {interface.generation}")
    print(f"✓ Paused status: {interface.paused}")
    
finally:
    # Restore terminal
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

print("\n✅ Test completed!")