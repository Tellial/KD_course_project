import math
import heapq
from sets import Set
import copy


# Min heap for inter-cluster distances and their associated clusters (wrapped in tuples)
min_dist_heap = []

#--------------------------------------------------------------------------------------------------
# DISTANCE FUNCTION
# Distance function: returns euclidean distance (average linkage) between two clusters wrt x, y, z
#---------------------------------------------------------------------------------------------------
def distance2D(i, j, vgsales, _x, _y, _z):
    x1 = float((vgsales[i][_x]))
    y1 = float((vgsales[i][_y]))
    z1 = float((vgsales[i][_z]))
    x2 = float((vgsales[j][_x]))
    y2 = float((vgsales[j][_y]))
    z2 = float((vgsales[j][_z]))
    
    return float(math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2))

#---------------------------------------------------------------------------------------------
# INITIALIZE DISTANCE MATRIX
# Calculate distances between all row indices once (stored in a minheap)
#---------------------------------------------------------------------------------------------
def init_dist_matrix(vgsales, _x, _y, _z) :
    rows = len(vgsales)
    for i in range (0, rows) :
        for j in range (i+1, rows) :
            if (i != j) :
                d = distance2D(i,j, vgsales, _x, _y, _z)
                dist = (d, i, j)
                heapq.heappush(min_dist_heap, dist)

#-------------------------------------------------------------------------------------------------
# MERGE FUNCTION
# Merge function: merges clusters a and b. Updates cluster centre and distances to other clusters.
#--------------------------------------------------------------------------------------------------
def merge(a, b, vgsales, _x, _y, _z) :
    rows = len(vgsales)

    a_size = float(len(vgsales[a][0]))
    b_size = float(len(vgsales[b][0]))
    union_size = a_size + b_size 

    # New cluster centre calculated
    vgsales[a][_x] = (a_size/union_size) * (vgsales[a][_x]) + (b_size/union_size) * (vgsales[b][_x])
    vgsales[a][_y] = (a_size/union_size) * (vgsales[a][_y]) + (b_size/union_size) * (vgsales[b][_y])
    vgsales[a][_z] = (a_size/union_size) * (vgsales[a][_z]) + (b_size/union_size) * (vgsales[b][_z])

    # Merge clusters into vgsales[a][0]
    vgsales[a][0] = vgsales[a][0].union(vgsales[b][0])

    # Mark the cluster label column with -1: the row has been 'used' 
    vgsales[b][12] = -1 

    # Calculate distances between this new cluster (=a) and all others (=index) and push onto heap
    index = a - 1
    for z in range (1, rows) :
        # If entry has not been wiped, there is a cluster at vgsales[index]
        if vgsales[index][12] != -1 :
            dist = (distance2D(a, index, vgsales, _x, _y, _z), a, index)
            heapq.heappush(min_dist_heap, dist)
        index = index - 1


#---------------------------------------------------------------------------------------------
# CLUSTER
# Pop minimum distances from heap and merge associated clusters until end criterion fulfilled
#----------------------------------------------------------------------------------------------
def cluster(vgsales, C, _x, _y, _z) :
    clusterCount = len(vgsales)
    rows = len(vgsales)
    print 'Starts with %d singletons' % (clusterCount)

    while clusterCount > C :

        min_dist = heapq.heappop(min_dist_heap)
            
        # If clusters at the endpoints of min_dist still exist and have not been merged elsewhere, merge them
        if vgsales[min_dist[1]][12] != -1 and vgsales[min_dist[2]][12] != -1 :
            merge(min_dist[1], min_dist[2], vgsales, _x, _y, _z)
            clusterCount = clusterCount - 1
            if (clusterCount % int(rows/20) == 0) :
                print '%d clusters remaining' % (clusterCount)
            #print 'cC %d' % (clusterCount)

    # Find indices of vgsales containing clusters
    cluster_inds = []
    label = int(1)
    # Label clusters 1 - C (label goes in vgsales[i][12]
    for i in range (0, rows) :
        # If this row represents a cluster
        if (vgsales[i][12] != -1) :
            vgsales[i][12] = int(label) 
            cluster_inds.append(i)
            label = label + 1

    # Index corresponds to cluster number i
    all_clusters = [0]

    # Gather clusters 1 - C with their contents to all_clusters
    for z in range (0, len(cluster_inds)) :
        cluster_contents = []
        ind = cluster_inds[z]
        itemset = copy.deepcopy(vgsales[ind][0])
        
        # While items remain in cluster
        while (len(itemset) > 0) :
            item = int(itemset.pop())
            cluster_contents.append(item)
        all_clusters.append(cluster_contents)

    # Give the rest of the rows a cluster label based on where they belong
    found = 0
    for z in range (0, rows) :
        found == 0
        # If cluster label not assigned yet to row
        if not (vgsales[z][12] != -1) :
            rank = int(vgsales[z][11])
            # Search all_clusters for this rank
            for clusterid in range (1, len(all_clusters)):
                rowlength = len(all_clusters[clusterid])
                for i in range (0, rowlength) :
                    if (rank == all_clusters[clusterid][i]) :
                        vgsales[z][12] = clusterid

    print 'Finished with %d clusters' % (clusterCount)
    
