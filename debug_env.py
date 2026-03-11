import sys
import os
import subprocess

print("--- SYSTEM DIAGNOSTICS ---")
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"Current Working Directory: {os.getcwd()}")

print("\n--- CHECKING LIBRARIES ---")
try:
    import numpy
    print(f"✅ NumPy Found: {numpy.__version__} at {numpy.__file__}")
except ImportError as e:
    print(f"❌ NumPy Error: {e}")

try:
    import moviepy
    print(f"✅ MoviePy Found: {moviepy.__version__} at {moviepy.__file__}")
except ImportError as e:
    print(f"❌ MoviePy Error: {e}")

print("\n--- PATHS SEARCHED ---")
for path in sys.path:
    print(f" - {path}")