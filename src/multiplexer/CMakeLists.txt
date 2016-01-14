cmake_minimum_required (VERSION 2.8)
project(multiplexor)

# Version
set (multiplexor_VERSION_MAJOR 1)
set (multiplexor_VERSION_MINOR 0)
set (multiplexor_VERSION_PATCH 0)

include_directories(
    "src"
)

set(MUX_SOURCES "src/mux.c")
set(DEMUX_SOURCES "src/demux.c")

add_executable(mux ${MUX_SOURCES})
add_executable(demux ${DEMUX_SOURCES})
