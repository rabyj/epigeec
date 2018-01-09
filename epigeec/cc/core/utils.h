/* Copyright (C) 2015 Jonathan Laperle. All Rights Reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
==============================================================================*/

#include <openssl/md5.h>
#include <string>
#include <iostream>

std::string md5sum(std::string file_path) {
  std::ifstream file(file_path);
  std::basic_string<unsigned char> digest;
  digest.reserve(16);
  std::basic_string<unsigned char> content((std::istreambuf_iterator<char>(file)),
                 std::istreambuf_iterator<char>());
  MD5(&content[0], content.size(), &digest[0]);
  std::string md5;
  md5.reserve(32);
  for(int i = 0; i < 16; ++i)
    sprintf(&md5[i*2], "%02x", (unsigned int)digest[i]);
  return md5;
}