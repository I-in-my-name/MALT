# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/jack/esp/v5.5.1/esp-idf/components/bootloader/subproject"
  "/home/jack/SoftwareWork/MALT/i2sWorkspace/prototype4-1.1/build/bootloader"
  "/home/jack/SoftwareWork/MALT/i2sWorkspace/prototype4-1.1/build/bootloader-prefix"
  "/home/jack/SoftwareWork/MALT/i2sWorkspace/prototype4-1.1/build/bootloader-prefix/tmp"
  "/home/jack/SoftwareWork/MALT/i2sWorkspace/prototype4-1.1/build/bootloader-prefix/src/bootloader-stamp"
  "/home/jack/SoftwareWork/MALT/i2sWorkspace/prototype4-1.1/build/bootloader-prefix/src"
  "/home/jack/SoftwareWork/MALT/i2sWorkspace/prototype4-1.1/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/jack/SoftwareWork/MALT/i2sWorkspace/prototype4-1.1/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/jack/SoftwareWork/MALT/i2sWorkspace/prototype4-1.1/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
