import sys
import csv
import libs.kmeans as kmeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random


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

    # Select only NA_Sales, EU_sales and JP_Sales
    nodes.append(kmeans.node([vgsales[i][6], vgsales[i][7], vgsales[i][8]], vgsales[i][5], vgsales[i][:6]))

# Perform k-means
results = kmeans.perform_kmeans(nodes,K)
print("Finished clustering in: " + str(results[2]) + " iterations.")

# Write the result of the k-means clustering to a csv file
try:
    colors = {}
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.autoscale_view(True,True,True)
    ax.set_xlim([0, 15])
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

            #if str(results[0][i].cluster.label) not in colors:
            #    colors[str(results[0][i].cluster.label)] = ((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))

            #ax.scatter(results[0][i].coordinates[0], results[0][i].cluster.coordinates[1], results[0][i].cluster.coordinates[2], c=colors[str(results[0][i].cluster.label)])
    x = []
    y = []
    z = []
    colors = []
    for node in results[0]:
        x.append(node.coordinates[2])
        y.append(node.coordinates[1])
        z.append(node.coordinates[0])
        if node.cluster.label == 0:
            colors.append('#ff0000')
        elif node.cluster.label == 1:
            colors.append('#00ff00')
        else:
            colors.append('#0000ff')
    ax.scatter(x, y, z, c=colors)
    # Change the plot area's size

    fig.savefig('3dprojection.png')
except IOError as e:
    print "Failed to open file: " + sys.argv[2] + " for writing"
    exit(0)
