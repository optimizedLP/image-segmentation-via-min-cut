# This script has some runtime errors. Keeps on running for ~30 mins. Need to improve the code


import time
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random

def karger_algorithm(img):
    """
    Performs image segmentation using Karger's algorithm.
    """
    start_time = time.time()
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Create a graph from the image
    graph = nx.Graph()
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            graph.add_node((i, j), weight=gray[i, j])
    
    # Add edges between neighboring pixels
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            if i < gray.shape[0] - 1:
                graph.add_edge((i, j), (i + 1, j), weight=abs(gray[i, j] - gray[i + 1, j]))
            if j < gray.shape[1] - 1:
                graph.add_edge((i, j), (i, j + 1), weight=abs(gray[i, j] - gray[i, j + 1]))
    
    # Perform Karger's algorithm
    while len(graph) > 2:
        edge = random.choice(list(graph.edges()))
        u, v = edge
        graph = nx.contracted_edge(graph, (u, v))
    
    # The remaining nodes represent the minimum cut
    min_cut = list(graph.nodes())
    
    end_time = time.time()
    return min_cut, end_time - start_time

# Load the image
img = cv2.imread('bird.jpg')

# Perform image segmentation using Karger's algorithm
min_cut, execution_time = karger_algorithm(img)

# Display the segmented image
segmented_img = np.zeros_like(img)
for node in min_cut:
    if isinstance(node, tuple):
        i, j = node
        segmented_img[i, j] = 255

plt.imshow(cv2.cvtColor(segmented_img, cv2.COLOR_BGR2RGB))
plt.title("Karger's Algorithm Segmentation")
plt.axis('off')
plt.show()

print("Execution Time:", execution_time, "seconds")
