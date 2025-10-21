CMAKE_MINIMUM_REQUIRED( VERSION 3.5 )

# Set CMP0167 to OLD to avoid issues with finding Hdf5 and Boost
if(POLICY CMP0167)
    cmake_policy(SET CMP0167 OLD)
endif()

SET( PROJ_NAME "epiGeEC" )
SET( EXECUTABLE_OUTPUT_PATH "${CMAKE_SOURCE_DIR}/epigeec/bin" )
SET( LIBRARY_OUTPUT_PATH "${CMAKE_SOURCE_DIR}/epigeec/lib" )
SET( CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} ${CMAKE_SOURCE_DIR}/epigeec/lib )

SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
SET(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")

SET (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath,'$ORIGIN/../lib'" )
SET (CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath,'$ORIGIN/../lib'" )

PROJECT( ${PROJ_NAME} )

# Platform-specific settings
if(APPLE)
    SET(CMAKE_INSTALL_RPATH "@loader_path/../lib")
    SET(CMAKE_MACOSX_RPATH ON)
    # Add Homebrew library paths for all targets
    link_directories(/opt/homebrew/lib /usr/local/lib)
else() # Linux
    SET(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
    SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath,'$ORIGIN/../lib'")
    SET(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath,'$ORIGIN/../lib'")
endif()

# Find HDF5
find_package(HDF5 COMPONENTS C HL REQUIRED)
if(HDF5_FOUND)
    include_directories(${HDF5_INCLUDE_DIRS})
    message(STATUS "HDF5 found: ${HDF5_LIBRARIES}")
else()
    message(FATAL_ERROR "HDF5 not found!")
endif()

# Find Boost
find_package(Boost COMPONENTS filesystem iostreams REQUIRED)
if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS})
    message(STATUS "Boost found: ${Boost_LIBRARIES}")
else()
    message(FATAL_ERROR "Boost not found!")
endif()

# Find OpenMP
find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    message(STATUS "OpenMP found: ${OpenMP_CXX_VERSION}")
    # Make OpenMP flags available to all subdirectories
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    # Make OpenMP libraries available globally
    link_libraries(OpenMP::OpenMP_CXX)
else()
    message(WARNING "OpenMP not found - building without OpenMP support")
endif()

ADD_SUBDIRECTORY( "third_party/bwreader" "bwreader" )
ADD_SUBDIRECTORY( "epigeec/cc/core" "core" )
ADD_SUBDIRECTORY( "epigeec/cc/bw_to_hdf5" "bw_to_hdf5" )
ADD_SUBDIRECTORY( "epigeec/cc/bg_to_hdf5" "bg_to_hdf5" )
ADD_SUBDIRECTORY( "epigeec/cc/filter" "filter" )
ADD_SUBDIRECTORY( "epigeec/cc/correlation" "correlation" )
ADD_SUBDIRECTORY( "epigeec/cc/correlation_w" "correlation_w" )
ADD_SUBDIRECTORY( "epigeec/cc/correlation_nm" "correlation_nm" )
ADD_SUBDIRECTORY( "epigeec/cc/correlation_w_nm" "correlation_w_nm" )
