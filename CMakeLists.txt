# Minimum required version of CMake
cmake_minimum_required(VERSION 3.10)

# Project name and version
project(HelloWorld VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the src subdirectory
add_subdirectory(src)

# Add executable target using the source files from src
add_executable(HelloWorld src/hello.cpp)

# Optional: Set compiler-specific options
if(MSVC)
    target_compile_options(HelloWorld PRIVATE /W4)
else()
    target_compile_options(HelloWorld PRIVATE -Wall -Wextra -Wpedantic)
endif()