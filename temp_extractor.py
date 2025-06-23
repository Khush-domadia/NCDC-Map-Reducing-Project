#!/usr/bin/env python3
from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol

class TempExtractor(MRJob):
    # Use RawValueProtocol for output to prevent adding quotes
    OUTPUT_PROTOCOL = RawValueProtocol
    
    def mapper(self, _, line):
        # Each line is a record in fixed-width format.
        if len(line) < 93:
            return  # skip lines that are too short to parse
        year = line[15:19]
        temp_str = line[87:92]
        # Remove leading '+' if present (for positive temperatures)
        if temp_str.startswith('+'):
            temp_str = temp_str[1:]
        # If temp_str is not digits (e.g., empty or blanks), skip
        if temp_str == "" or temp_str.isspace():
            return
        try:
            temp = int(temp_str)
        except ValueError:
            return  # skip if not an integer
        quality = line[92]
        # Filter out missing or bad data
        if temp != 9999 and quality in "01459":
            # Emit year and temperature
            yield year, temp
    
    def reducer(self, year, temps):
        # For each temperature for this year
        for temp in temps:
            # Format output as "year temp" without quotes
            yield None, f"{year} {temp}"

if __name__ == "__main__":
    TempExtractor.run()
