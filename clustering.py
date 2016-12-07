import csv
import math
import heapq
from sets import Set

# Ending criterion: stops when n clusters remain  
n = 10;

# Attributes (column index, e.g. 6 = NA_Sales, 7 = EU_Sales)
x = 6
y = 7

# Min heap for inter-cluster distances and their associated clusters (wrapped in tuples)
min_dist_heap = []

# Data import stage (this could be made to import just the rank and attribute columns)
vgsales = []
with open('data/vgsales_30.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # Skip the first row with the headers
    next(reader, None)
    for row in reader:
        vgsales.append(row)
rows = len(vgsales)
clusterCount = rows

# Convert each rank number into a set containing the rank number. The ranks are used as ids
for i in range (0, rows) :
    rank = int(vgsales[i][0])
    vgsales[i][0] = Set ([rank])

# Function: returns euclidean distance (average linkage) between two clusters wrt attributes x and y
def distance2D(i, j):
    x1 = float(vgsales[i][x])
    y1 = float(vgsales[i][y])
    x2 = float(vgsales[j][x])
    y2 = float(vgsales[j][y])
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# Function: merges clusters a and b. Updates cluster centre and distances to other clusters.
# Data in other columns except rank and attribute columns is not merged and becomes garbage
def merge(a, b) : 
    a_size = float(len(vgsales[a][0]))
    b_size = float(len(vgsales[b][0]))
    union_size = a_size + b_size 

    # New cluster centre calculated
    vgsales[a][x] = (a_size/union_size) * float(vgsales[a][x]) + (b_size/union_size) * float(vgsales[b][x])
    vgsales[a][y] = (a_size/union_size) * float(vgsales[a][y]) + (b_size/union_size) * float(vgsales[b][y])

    # Merge clusters onto row index a
    vgsales[a][0] = vgsales[a][0].union(vgsales[b][0])

    # Wipe 'Year' column on row index b and replace with -1 to indicate that this entry has been wiped
    # (A convoluted way of flagging/removing wiped entries... we need some other data structure)
    vgsales[b][3] = -1 

    # Calculate distances between this new cluster and all others and push them onto the heap
    index = a - 1
    for z in range (0, rows-1) :
        # If entry has not been wiped, there is a cluster at vgsales[index]
        if vgsales[index][3] != -1 :
            dist = (distance2D(a, index), a, index)
            heapq.heappush(min_dist_heap, dist)
        index = index - 1

# 'MAIN'

# Calculate distances between all row indices once
for i in range (0, rows) :
    for j in range (i+1, rows) :

        # Store inter-cluster distance and cluster row indices into a tuple and push it onto heap
        dist = (distance2D(i, j), i, j)
        heapq.heappush(min_dist_heap, dist)

# Pop minimum distances from heap and merge associated clusters until end criterion fulfilled
while clusterCount > n :
    min_dist = heapq.heappop(min_dist_heap)
    
    # If both clusters still exist and have not been wiped and merged elsewhere, merge them
    if vgsales[min_dist[1]][3] != -1 and vgsales[min_dist[2]][3] != -1 :
        merge(min_dist[1], min_dist[2])
        clusterCount = clusterCount - 1

# Print final clusters and their cluster centre coordinates (e.g. NA_Sales and EU_Sales):
for z in range (0, rows) :
    if int(vgsales[z][3]) != -1 :
        print '%s %f %f' % (vgsales[z][0], float(vgsales[z][x]), float(vgsales[z][y]))
print 'clusterCount = %d' % (clusterCount)


