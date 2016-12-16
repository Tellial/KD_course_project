import sys
import csv
import libs.kmeans as kmeans


if len(sys.argv) != 3:
    print "Use \"python k-means_clustering.py [CLUSTER_COUNT] [OUTPUT_FILE]\""
    exit(0)

# Cluster count used for kmeans
try:
    K = int(sys.argv[1])
except ValueError:
    print "Cluster count must be an integer"


# Try to read the data
vgsales = []
try:
    with open("data/vgsales.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip the first row with the headers
        next(reader, None)
        for row in reader:
            vgsales.append(row)
except IOError as e:
    print "Failed to open file data/vgsales.csv for reading"
    exit(0)

# Create nodes to be used for clustering from all the dataset points
nodes = []
for i in range(len(vgsales)):
    # Parse the float values from the string values in the data (we know that they are in indexes 6 - 11)
    for n in range(6, 11):
        vgsales[i][n] = float(vgsales[i][n])
    nodes.append(kmeans.node(vgsales[i][6:10], vgsales[i][5], vgsales[i][:6]))

# Perform k-means
results = kmeans.perform_kmeans(nodes,K)
print("Finished clustering in: " + str(results[2]) + " iterations.")

# Write the result of the k-means clustering to a csv file
try:
    with open(sys.argv[2], 'w') as csvfile:
        fieldnames = ["Number", "Name", "Platform", "Year", "Genre", "Publisher", "Cluster"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')

        writer.writeheader()
        for i in range(len(results[0])):
            writer.writerow({
                'Number': results[0][i].info[0],
                'Name' : results[0][i].info[1],
                'Platform' : results[0][i].info[2],
                'Year' : results[0][i].info[3],
                'Genre' : results[0][i].info[4],
                'Publisher' : results[0][i].info[5],
                'Cluster' : results[0][i].cluster.label
            })
except IOError as e:
    print "Failed to open file: " + sys.argv[2] + " for writing"
    exit(0)
