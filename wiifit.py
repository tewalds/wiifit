#!/usr/bin/python

from __future__ import division
import csv
import struct
import string
import sys

# Path to WiiFit data file
file_name = sys.argv[1] if len(sys.argv) > 1 else 'RPHealth.dat'

# Adjust based on what the wii took off for each recording, in Kg.
weight_adjustment = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0

# Each record is 0x9271 bytes long
record_length = 0x9281

with open(file_name, 'rb') as in_file:
    # Iterate through each Mii.
    for record_start in xrange(0, record_length * 100, record_length):
        # Go to the start of the current record.
        in_file.seek(record_start)

        # Read the first 30 bytes (header + name).
        line = in_file.read(30)

        # For some reason names are stored as N a m e instead of Name.
        # Throw away the header and any extranous spaces.
        data = struct.unpack('<9xcxcxcxcxcxcxcxcxcxcxc', line)

        # Condense our unpacked characters into a string.
        wf_name = string.join(data, '').strip('\0')
        if not wf_name:
            break

        print 'Found', wf_name

        # Open a new CSV file for this person.
        with open('wiifit_%s.csv' % wf_name, 'w') as out_file:
            writer = csv.writer(out_file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Date', 'Weight', 'BMI', 'Balance'])

            # Weight data starts 0x38a1 bytes into the record.
            in_file.seek(record_start + 0x38a1)

            # Loop through the record data until it starts coming up blank.
            while True:
                # Each line is 21 bytes. We only care about the first bit.
                line = in_file.read(21)

                # 4 bytes of hex-packed date followed by three sets of 2 bytes
                # representing weight, BMI, and balance.
                packed_date, weight, bmi, balance = struct.unpack('>i3H', line[0:10])

                # Unpack the date: http://stackoverflow.com/questions/719129/datetime-hex-format
                year   = packed_date >> 20 & 0x7ff
                month  = (packed_date >> 16 & 0xf) + 1
                day    = packed_date >> 11 & 0x1f
                hour   = packed_date >> 6 & 0x1f
                minute = packed_date & 0x3f
                second = 0

                if year == 0:
                    break

                date = '%s-%02d-%02d %02d:%02d:%02d' % (year, month, day, hour, minute, second)
                writer.writerow([date, weight_adjustment + (weight / 10), bmi / 100, balance / 10])
