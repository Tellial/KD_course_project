import random
import math

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

# --------------------
# -- Single Cluster --
# --------------------
class cluster:
    # Init by a node
    def __init__(self, node, label):
        self.label = label
        self.coordinates = node.coordinates
        self.nodes = []

# -------------------
# --- Single Node ---
# -------------------
class node:
    def __init__(self, coordinates, real_label):
        # Coordinates of the node
        self.coordinates = coordinates
        # Real label of the node (generated or real dataset)
        self.real_label = real_label
        # Distance to the nearest cluster (Calculated by find_nearest_cluster())
        self.distance_ncluster = None
        # Cluster this node belongs to
        self.cluster = None
    
    # Returns distance from this node to cluster (or node)
    def distance(self, cluster):
        sums = 0
        for i in range(len(self.coordinates)):
            sums += (self.coordinates[i] - cluster.coordinates[i])**2
        return abs(math.sqrt(sums))
    
    # Returns nearest cluster to this node from the list of the clusters
    def find_nearest_cluster(self, clusters):
        nearest = None
        nearest_value = None
        for cluster in clusters:
            dist = self.distance(cluster)
            if  nearest == None or dist < nearest_value:
                nearest = cluster
                nearest_value = dist
                self.distance_ncluster = dist
        return nearest

# ------------------------------------
# --- K-means clustering algorithm ---
# ------------------------------------
def kmeans(nodes, clusters, K, m_i=100):
    # Limit number of iterations performed by m_i variable
    i = 0
    while i < m_i:
        changes = False
        for k in clusters:
            k.nodes = []
        
        for node in nodes:
            new_cluster = node.find_nearest_cluster(clusters)
            if new_cluster != node.cluster:
                changes = True
                node.cluster = new_cluster
            node.cluster.nodes.append(node)
        
        if changes is False:
            break
        
        for cluster in clusters:
            mean_axes = []
            new_cluster_coords = []    
        
            # Add an empty list for each dimension
            for dimension in nodes[0].coordinates:
                mean_axes.append([])
                
            for node in cluster.nodes:
                for n in range(len(node.coordinates)):
                    mean_axes[n].append(node.coordinates[n])    
            
            for axis in mean_axes:
                new_cluster_coords.append(mean(axis))
            
            cluster.coordinates = new_cluster_coords
        i += 1
    # Return the number of iterations
    return i

# ---------------------------------------
# ------ K-means++ initialization -------
# ---------------------------------------
def k_means_pp_init(nodes, K):
    clusters = []
    cluster_count = 0
    
    # First cluster is chosen randomly
    new_cluster = cluster(nodes[random.randint(0,len(nodes)-1)], cluster_count)
    clusters.append(new_cluster)
    cluster_count += 1
    
    while cluster_count < K:
        # Used in determining if we choose the node as cluster
        sum_distances = 0
        
        # Sum all the distances in power of second
        for node in nodes:
            node.find_nearest_cluster(clusters)
            sum_distances = sum_distances + node.distance_ncluster**2

        for node in nodes:
            if k_meanspp_choose_new(node.distance_ncluster**2, sum_distances):
                clusters.append(cluster(node, cluster_count))
                cluster_count += 1
                break
                
    # Return the new cluster centroid list
    return clusters

# K-means++ probability node to cluster choosing algorithm
def k_meanspp_choose_new(x, y):
    if random.random() < (x / y):
        return True
    else:
        return False

# -----------------
# -- K-means run --
# -----------------

def perform_kmeans(nodes, K):
    clusters = k_means_pp_init(nodes, K)
    # i is iteration counts
    i = kmeans(nodes, clusters, K)
        
    return nodes, clusters, i
