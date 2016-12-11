import sys
import csv
import libs.kmeans as kmeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random


if len(sys.argv) != 4:
    print "Use \"python k-means_clustering.py [CLUSTER_COUNT] [INPUT_FILE] [OUTPUT_FILE]\""
    exit(0)

# Cluster count used for kmeans
try:
    K = int(sys.argv[1])
except ValueError:
    print "Cluster count must be an integer"


# Try to read the data
data = []
try:
    with open(sys.argv[2]) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip the first row with the headers
        next(reader, None)
        for row in reader:
            data.append(row)
except IOError as e:
    print "Failed to open file: " + sys.argv[1] + " for reading"
    exit(0)

# Create nodes to be used for clustering from all the dataset points
nodes = []
for i in range(len(data)):
    # Parse the float values from the string values in the data
    for n in range(len(data[i])):
        try:
            data[i][n] = float(data[i][n])
        except ValueError:
            pass
    print data[i]
    nodes.append(kmeans.node([data[i][0], data[i][1], data[i][2], data[i][3]], data[i][4]))

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
    with open(sys.argv[3], 'w') as csvfile:
        fieldnames = ["Coordinates", "Real label", "Cluster"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')

        writer.writeheader()
        for i in range(len(results[0])):
            writer.writerow({
                "Coordinates": results[0][i].coordinates,
                "Real label" : results[0][i].real_label,
                "Cluster" : results[0][i].cluster.label
            })

            #if str(results[0][i].cluster.label) not in colors:
            #    colors[str(results[0][i].cluster.label)] = ((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
            #ax.scatter(results[0][i].coordinates[0], results[0][i].cluster.coordinates[1], results[0][i].cluster.coordinates[2], c=colors[str(results[0][i].cluster.label)])
    x = []
    y = []
    z = []
    colors = []
    for node in results[0]:
        x.append(node.coordinates[0])
        y.append(node.coordinates[2])
        z.append(node.coordinates[1])
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
