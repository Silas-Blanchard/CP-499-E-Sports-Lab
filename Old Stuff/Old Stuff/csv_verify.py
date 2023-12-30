import csv
import sys

def verifyCSV(input):
    #potential_csv = CSVtoString(input)
    potential_csv = open(input);
    row_num = 0
    for row in potential_csv:
        if(len(row.split(","))!=3):
            potential_csv.close()
            return("CSV ERROR AT LINE: %s", row_num + 1)
        else:
            row_num += 1;
    potential_csv.close()
    return("Valid CSV")

input = sys.argv[1]
print(verifyCSV(input))
