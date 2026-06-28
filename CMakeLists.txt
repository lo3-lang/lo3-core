cmake_minimum_required(VERSION 3.10)
set(CMAKE_C_COMPILER gcc)
project(lo3 C)
set(CMAKE_C_STANDARD 11)
add_compile_definitions(_DEFAULT_SOURCE _POSIX_C_SOURCE=200809L)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_SOURCE_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_SOURCE_DIR}/bin)

file(GLOB SOURCES "src/*.c")

# POSIX getline needs _POSIX_C_SOURCE; syscall() needs _DEFAULT_SOURCE
add_compile_definitions(_POSIX_C_SOURCE=200809L _DEFAULT_SOURCE)
add_executable(lo3 ${SOURCES})
target_include_directories(lo3 PRIVATE include)

if(UNIX)
    target_link_libraries(lo3 PRIVATE dl)
endif()

enable_testing()
add_subdirectory(test)