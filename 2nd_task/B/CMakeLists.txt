cmake_minimum_required(VERSION 2.8)

project(Lib)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")

add_library(Lib lib.h)

target_include_directories(Lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
