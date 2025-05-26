#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the current directory and build directory
    project_root = Path.cwd()
    build_dir = project_root / "build"
    
    print("🚀 Looking for executable to run...")
    
    # Check if build directory exists
    if not build_dir.exists():
        print("❌ Error: Build directory not found")
        print("   Run buildit.py first to build the project")
        sys.exit(1)
    
    # Find executable files
    executables = []
    for file in build_dir.iterdir():
        if file.is_file():
            # Check if it's an executable (Windows .exe or Unix executable)
            if file.suffix == '.exe' or (not file.suffix and file.stat().st_mode & 0o111):
                executables.append(file)
    
    if not executables:
        print("❌ Error: No executables found in build directory")
        print("   Run buildit.py first to build the project")
        sys.exit(1)
    
    # If multiple executables, show them and pick the first one
    if len(executables) > 1:
        print("📦 Multiple executables found:")
        for i, exe in enumerate(executables):
            print(f"   {i+1}. {exe.name}")
        print(f"   Running the first one: {executables[0].name}")
        executable = executables[0]
    else:
        executable = executables[0]
        print(f"📦 Found executable: {executable.name}")
    
    # Run the executable
    print(f"\n🚀 Running {executable.name}...")
    print("-" * 40)
    
    try:
        # Pass any command line arguments to the executable
        args = sys.argv[1:]  # Get arguments passed to runit.py
        cmd = [str(executable)] + args
        
        result = subprocess.run(cmd, cwd=build_dir, check=True, text=True)
        print("-" * 40)
        print(f"✅ {executable.name} executed successfully!")
        
    except subprocess.CalledProcessError as e:
        print("-" * 40)
        print(f"❌ {executable.name} failed with return code {e.returncode}")
        sys.exit(e.returncode)
        
    except FileNotFoundError:
        print(f"❌ Could not execute {executable.name}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n⚠️  Execution interrupted by user")
        sys.exit(130)

if __name__ == "__main__":
    main()