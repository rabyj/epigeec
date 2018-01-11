CMAKE_MINIMUM_REQUIRED( VERSION 2.8 )

SET( PROJ_NAME "epiGeEC" )
SET( EXECUTABLE_OUTPUT_PATH "${CMAKE_SOURCE_DIR}/epigeec/bin" )
SET( LIBRARY_OUTPUT_PATH "${CMAKE_SOURCE_DIR}/epigeec/lib" )
SET( CMAKE_LIBRARY_PATH ${CMAKE_LIBRARY_PATH} ${CMAKE_SOURCE_DIR}/epigeec/lib )

PROJECT( ${PROJ_NAME} )

ADD_SUBDIRECTORY( "third_party/bwreader" "bwreader" )
ADD_SUBDIRECTORY( "epigeec/cc/core" "core" )
ADD_SUBDIRECTORY( "epigeec/cc/bw_to_hdf5" "bw_to_hdf5" )
ADD_SUBDIRECTORY( "epigeec/cc/bg_to_hdf5" "bg_to_hdf5" )
ADD_SUBDIRECTORY( "epigeec/cc/filter" "filter" )
ADD_SUBDIRECTORY( "epigeec/cc/correlation" "correlation" )
