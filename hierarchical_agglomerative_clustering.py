import sys
from sets import Set
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy.stats.stats import pearsonr
import libs.agglomerative as agg

# sys.argv[1] = target file for saved csv 
# sys.argv[2] = number of clusters (int)
# sys.argv[3] = x index [6-10]
# sys.argv[4] = y index [6-10]
# sys.argv[5] = z index [6-10]
# sys.argv[6] = data reduction attribute name (optional) [2-5]
# sys.argv[7] = data reduction attribute value (optional) 

# No error checking for sys.argv[7], please take care to provide correct values from vgsales.csv
# 'Rank' attribute from vgsales.csv dataset is used to identify each game. No two have the same rank. 

argc = len(sys.argv)

global errorMessage
errorMessage = 'Help:\nclustering.py [filename.csv] [nof_clusters(int)] [x_index(int)] [y_index(int)] [z_index(int)]\nclustering.py [filename.csv] [nof_clusters(int)] [x_index(int)] [y_index(int)] [z_index(int)] [attribute_index] [attribute_value]\n2=Platform, 3=Year, 4=Genre, 5=Publisher, 6=NA_Sales, 7=EU_Sales, 8=JP_Sales, 9=Other_Sales, 10=Global_Sales\nAcceptable x_index and y_index values: 6-10, all must be different\nAcceptable attribute_index values: 2-5\nFor acceptable attribute_values see dataset vgsales.csv'

# Attribute for narrowing dataset: 2 for Platform, 3 for Year, 4 for Genre, 5 for Publisher
global attribute
attribute = int(0)

# Value of attribute, e.g. 'SNES', '2006', 'Puzzle', 'Nintendo'
global attribute_value
attribute_value = ''

# Ensure correct argument count
if not (argc == 6 or argc == 8) :
    print errorMessage
    exit()

# Read arguments
try:
    filename = sys.argv[1]
    C = int(sys.argv[2])
    _x = int(sys.argv[3])
    _y = int(sys.argv[4])
    _z = int(sys.argv[5])
    if (argc == 8) :
        attribute = int(sys.argv[6])
        attribute_value = sys.argv[7]
except ValueError:
    print errorMessage
    exit()

# Check validity of xyz arguments (within range [6-10] and all values must be different from each other
if not (_x >= 6 and _x <= 10 and _y >= 6 and _y <= 10 and ((_z >= 6 and _z <= 10) or (_z == 0)) and _x != _y and _x != _z and _y != _z) :
    print errorMessage
    exit()

# Check validity of possible attribute argument (attribute_value not checked, refer to vgsales.csv)
if (argc == 8 and not (attribute >= 2 and attribute <= 5)) :
    print errorMessage
    exit()

# Data import
temp_import = []
vgsales = []
with open('data/vgsales.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # Skip the first row with the headers
    next(reader, None)
    for row in reader:
        temp_import.append(row) 
rows = len(temp_import)


# DATA CLEANING AND REDUCTION

# Prune items with irrelevant attributes and/or missing information 
for i in range (0, rows) :
    # If concentrating on an attribute (Platform, Genre etc), strip out others
    if (argc == 8) :
        if(temp_import[i][attribute] == attribute_value) :
            vgsales.append(temp_import[i])
    else :
        vgsales.append(temp_import[i])

rows = len(vgsales)
print 'post-reduction rows %d' % (rows)

global clusterCount
clusterCount = rows

# Add and initialize two columns at the end of each row (one for rank numbers and one for cluster numbers)
for z in range (0,rows) :
    vgsales[z].append(0)
    vgsales[z].append(0)

# Convert column indices 6-10 to floats and indices 0, 3, 11 and 12 to ints 
for z in range (0,rows) :
    for w in range (6,11) :
        vgsales[z][w] = float(vgsales[z][w])
    vgsales[z][0] = int(vgsales[z][0])
    if (vgsales[z][3] != 'N/A') : # Accounting for missing values in 'Year' column
        vgsales[z][3] = int(vgsales[z][3])
    vgsales[z][11] = int(vgsales[z][11])
    vgsales[z][12] = int(vgsales[z][12])

# Convert each rank number into a set containing the rank number and duplicate rank number into index 11 as an int
for i in range (0, rows) :
    rank = int(vgsales[i][0])
    vgsales[i][0] = Set ([rank])
    vgsales[i][11] = rank

print 'Initializing distance matrix'

agg.init_dist_matrix(vgsales, _x, _y, _z)

agg.cluster(vgsales, C, _x, _y, _z)

# Write the result of the clustering to a csv file
axes = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']

# Sets range of axes (zoom)
lim = 10

try:
    colors = {}
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("",fontsize=14)
    ax.set_xlabel((axes[_x - 6]),fontsize=12)
    ax.set_ylabel((axes[_y - 6]),fontsize=12)
    ax.set_zlabel((axes[_z -6]), fontsize=12)
    ax.grid(True,linestyle='-',color='0.75')
    ax.autoscale_view(True,True,True)
    ax.set_xlim([0, lim])
    ax.set_ylim([0, lim])
    ax.set_zlim([0, lim])

    with open(sys.argv[1], 'w') as csvfile:
        fieldnames = ["Number", "Name", "Platform", "Year", "Genre", "Publisher", "Cluster"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')

        writer.writeheader()
        for i in range(0, len(vgsales)):
            writer.writerow({
                'Number': vgsales[i][11],
                'Name' : vgsales[i][1],
                'Platform' : vgsales[i][2],
                'Year' : vgsales[i][3],
                'Genre' : vgsales[i][4],
                'Publisher' : vgsales[i][5],
                'Cluster' : vgsales[i][12]
            })

            if str(vgsales[i][12]) not in colors:
                colors[str(vgsales[i][12])] = ((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))

            ax.scatter(vgsales[i][_x], vgsales[i][_y], vgsales[i][_z], c=colors[str(vgsales[i][12])])

    # Change the plot area's size

    fig.savefig('3dplot_C%d_%d%d%d_%s_%f.png' % (C, _x, _y, _z, attribute_value, lim))
except IOError as e:
    print "Failed to open file: " + sys.argv[1] + " for writing"
    exit(0)

