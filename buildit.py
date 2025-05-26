#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with return code {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    # Get the current directory
    project_root = Path.cwd()
    build_dir = project_root / "build"
    
    print("🏗️  Starting build process...")
    
    # Check if CMakeLists.txt exists
    if not (project_root / "CMakeLists.txt").exists():
        print("❌ Error: CMakeLists.txt not found in current directory")
        sys.exit(1)
    
    # Create build directory if it doesn't exist
    if build_dir.exists():
        print(f"🧹 Cleaning existing build directory...")
        shutil.rmtree(build_dir)
    
    build_dir.mkdir()
    print(f"📁 Created build directory: {build_dir}")
    
    # Run cmake to generate build files
    print("⚙️  Configuring with CMake...")
    if not run_command(["cmake", ".."], cwd=build_dir):
        print("❌ CMake configuration failed")
        sys.exit(1)
    
    # Determine build command based on platform
    if sys.platform.startswith('win'):
        build_cmd = ["cmake", "--build", ".", "--config", "Release"]
    else:
        build_cmd = ["make"]
    
    # Run the build
    print("🔨 Building project...")
    if not run_command(build_cmd, cwd=build_dir):
        print("❌ Build failed")
        sys.exit(1)
    
    print("✅ Build completed successfully!")
    
    # List the built executables
    print("\n📦 Built files:")
    for file in build_dir.iterdir():
        if file.is_file() and (file.suffix == '.exe' or file.stat().st_mode & 0o111):
            print(f"   🎯 {file.name}")

if __name__ == "__main__":
    main()