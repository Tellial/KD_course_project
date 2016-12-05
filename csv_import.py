import csv

vgsales = []
with open('data/vgsales.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # Skip the first row with the headers
    next(reader, None)
    for row in reader:
        vgsales.append(row)

print vgsales[0]
print vgsales[-1]