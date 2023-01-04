#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lz4.block
import sys
import struct

def print_usage_and_exit(): 
    sys.exit("usage: ./command uncompressed-inputfile.dll compressed-outputfile.dll")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage_and_exit()

    input_filepath = sys.argv[1]
    output_filepath = sys.argv[2]
    header_expected_magic = b'XALZ'
    header_index = b'\0\0\0\0'
    
    with open(input_filepath, "rb") as input_file:
        input_file_read = input_file.read()
        compressed = lz4.block.compress(input_file_read, mode="high_compression", store_size=True)
        header_uncompressed_length = struct.unpack('<I', compressed[0:4])[0]
        print("header index: %s" % header_index)
        print("compressed payload size: %s bytes" % (len(compressed) - 4))
        print("uncompressed length according to header: %s bytes" % header_uncompressed_length)
        input_file.close()
    with open(output_filepath, "wb") as output_file:
        output_file.write(header_expected_magic)
        output_file.write(header_index)
        output_file.write(compressed)
        output_file.close()
    print("result written to file")
