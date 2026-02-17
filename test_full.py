"""Test the terminal interface with keyboard input."""

import sys
import os
sys.path.insert(0, '/home/argus/.openclaw/workspace/TestMomo')

# Mock stdin for testing
class MockStdin:
    def __init__(self):
        self.data = ""
    
    def fileno(self):
        return 0
    
    def read(self):
        return self.data

# Test the interface
from momo.terminal import TerminalInterface

print("Creating terminal interface...")
interface = TerminalInterface(width=20, height=10, speed=0)
print("✓ Interface created")

# Test running the interface
print("Testing run method...")
interface.run()
print("✓ Run method executed")

print("\nAll tests passed!")