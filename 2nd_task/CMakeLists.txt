cmake_minimum_required(VERSION 2.8)
project(2nd_task)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")

find_package(PythonInterp 3.0 REQUIRED)

set(py_cmd "${PROJECT_SOURCE_DIR}/A/preparing.py")

execute_process(
                  COMMAND ${py_cmd}
                  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/A
               )
include_directories("A/" "C/" ".")

add_executable(main C/main.cpp)

add_subdirectory("B/")

set_target_properties(Lib PROPERTIES LINKER_LANGUAGE CXX)
target_link_libraries(main Lib)




