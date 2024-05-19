#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "epanet2" for configuration ""
set_property(TARGET epanet2 APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(epanet2 PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libepanet2.so"
  IMPORTED_SONAME_NOCONFIG "libepanet2.so"
  )

list(APPEND _cmake_import_check_targets epanet2 )
list(APPEND _cmake_import_check_files_for_epanet2 "${_IMPORT_PREFIX}/lib/libepanet2.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
