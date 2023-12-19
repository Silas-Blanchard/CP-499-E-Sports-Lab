import csv
import sys

def CSVtoString(input):
    f = open(input)

    outString = ''
    for row in f:
        outString += row

    f.close()
    return outString

input = sys.argv[1]
print(CSVtoString(input))