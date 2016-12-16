import sys
import math
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

class dbscan_node:
    def __init__(self, coordinates, real_label, info):
        self.info = info
        self.coordinates = coordinates
        self.real_label = real_label
        self.distance_ncluster = None
        self.classification = None

if len(sys.argv) != 5:
    print "Use \"python dbscan_clustering.py [EPS] [MIN_POINTS] [INPUT_FILE] [OUTPUT_FILE]\""
    exit(0)

try:
    EPS = float(sys.argv[1])
    MIN_POINTS = int(sys.argv[2])
except ValueError:
    print "Epsilon and min_points must be numbers"

def distance(p,q):
    sums = 0
    for i in range(len(p.coordinates)):
        sums += (p.coordinates[i] - q.coordinates[i])**2

    return abs(math.sqrt(sums))

def regionQuery(mainNode, nodes, eps):
    closeNodes = []
    for i in range(0, len(nodes)):
        if distance(mainNode, nodes[i]) < eps:
            closeNodes.append(i)

    return closeNodes

# Try to read the data
vgsales = []
try:
    with open(sys.argv[3]) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip the first row with the headers
        next(reader, None)
        for row in reader:
            vgsales.append(row)
except IOError as e:
    print "Failed to open file: " + sys.argv[3] + " for reading"
    exit(0)

# Create nodes to be used for clustering from all the dataset points
nodes = []
for i in range(len(vgsales)):
    # Parse the float values from the string values in the data (we know that they are in indexes 6 - 11)
    for n in range(6, 11):
        vgsales[i][n] = float(vgsales[i][n])

    # Select only NA_Sales and EU_sales
    nodes.append(dbscan_node([vgsales[i][6], vgsales[i][7], vgsales[i][8], vgsales[i][9]], vgsales[i][5], vgsales[i][:6]))

cluster = 1
try:
    colors = {}
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.autoscale_view(True,True,True)
    colors['0'] = '#ff0000'
    ax.set_xlim([0, 14])
    ax.set_ylim([0, 14])
    ax.set_zlim([0, 14])
    for node in nodes:
        if node.classification != None:
            continue
        neighborNodes = regionQuery(node, nodes, EPS)
        if len(neighborNodes) < MIN_POINTS:
            node.classification = 0
        else:­­
            node.classification = cluster
            for i in neighborNodes:
                nodes[i].classification = cluster

            while len(neighborNodes) > 0:
                newNeighborNodes = regionQuery(nodes[neighborNodes[0]], nodes, EPS)
                if len(newNeighborNodes) >= MIN_POINTS:
                    for j in range(0, len(newNeighborNodes)):
                        if nodes[newNeighborNodes[j]].classification == None or nodes[newNeighborNodes[j]].classification == 0:
                            if nodes[newNeighborNodes[j]].classification == None:
                                neighborNodes.append(newNeighborNodes[j])
                            nodes[newNeighborNodes[j]].classification = cluster
                neighborNodes = neighborNodes[1:]
            if str(cluster) not in colors:
                colors[str(cluster)] = ((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
            cluster = cluster + 1

        print node.info
    with open(sys.argv[4], 'w') as csvfile:
        fieldnames = ["Number", "Name", "Platform", "Year", "Genre", "Publisher", "Cluster"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')

        writer.writeheader()
        for i in range(len(nodes)):
            writer.writerow({
                'Number': nodes[i].info[0],
                'Name' : nodes[i].info[1],
                'Platform' : nodes[i].info[2],
                'Year' : nodes[i].info[3],
                'Genre' : nodes[i].info[4],
                'Publisher' : nodes[i].info[5],
                'Cluster' : nodes[i].classification
            })
            ax.scatter(nodes[i].coordinates[0], nodes[i].coordinates[1], nodes[i].coordinates[2], c=colors[str(nodes[i].classification)])
        fig.savefig('3dprojection_vgsales.png')

except IOError as e:
    print "Failed to open file: " + sys.argv[4] + " for writing"
    exit(0)
