import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import collections


def colour_two_deg(G):
    coloring = nx.coloring.greedy_color(G)
    colors = ['red', 'blue']

    for node in coloring:
        G.nodes[node]['color'] = colors[coloring[node]]
    node_colors = [nx.get_node_attributes(G, 'color')[node] for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=node_colors)
    plt.show()


def is_connected(G):
    return nx.is_connected(G)


def has_odd_cycle(G):
    for node in G.nodes():
        try:
            cycle = nx.find_cycle(G, source=node)
            if cycle is not None and len(cycle) % 2 == 1:
                return True
        except nx.NetworkXNoCycle:
            continue
    return False


def is_complete(G):
    num_nodes = len(G.nodes())
    num_edges = len(G.edges())
    max_edges = (num_nodes * (num_nodes - 1)) / 2
    return num_edges == max_edges


def max_degree(G):
    return max(dict(G.degree()).values())


def vertex_with_less_than_max_degree(G):
    max_deg = max_degree(G)
    for node, degree in dict(G.degree()).items():
        if degree < max_deg:
            return node
    return None


def one_vertex_cover(G):
    for node in G.nodes():
        if set(G.neighbors(node)) == set(G.nodes()) - {node}:
            return node
    return None


def split_graph(G, cut_vertex):
    # Create a copy of the graph to avoid modifying the original
    G_copy = G.copy()
    # Remove the cut-vertex
    G_copy.remove_node(cut_vertex)
    # Get the connected components
    components = list(nx.connected_components(G_copy))
    # Create subgraphs for each component
    subgraphs = []
    for component in components:
        # Create a subgraph for this component
        subgraph = G.subgraph(component).copy()
        # Add the cut-vertex to the subgraph
        subgraph.add_node(cut_vertex)
        for neighbor in G[cut_vertex]:
            if neighbor in component:
                subgraph.add_edge(cut_vertex, neighbor)
        # Add the subgraph to the list
        subgraphs.append(subgraph)
    return subgraphs


def find_x_y_z(graph):
    for x, y in graph.edges():
        for x, z in graph.edges():
            if x != y and y != z and not graph.has_edge(y, z) and graph.has_edge(x, y) and graph.has_edge(x, z):
                modified_graph = graph.copy()
                modified_graph.remove_nodes_from([y, z])
                if nx.is_connected(modified_graph):
                    return x, y, z
    return None, None, None


def sort_vertices_by_layers(G, T):
    # Perform a breadth-first search on T starting from the root node
    root = list(T.nodes())[0]
    queue = [(root, 0)]  # (node, layer)
    visited = {root}
    layers = [[]]  # List of layers

    while queue:
        node, layer = queue.pop(0)
        if layer == len(layers):
            layers.append([])  # Create a new layer if necessary
        layers[layer].append(node)

        for neighbor in T[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, layer + 1))

    # Flatten the layers and reverse the order
    sorted_vertices = [node for layer in reversed(layers) for node in layer]

    return sorted_vertices


def color_graph_with_spanning_tree(G, T):
    sorted_vertices = sort_vertices_by_layers(G, T)

    # Traverse G in the sorted order and assign colors
    coloring = {}  # Dictionary to store the assigned colors
    for vertex in sorted_vertices:
        # Get the colors of the neighbors
        neighbor_colors = {coloring[neighbor] for neighbor in G[vertex] if neighbor in coloring}

        # Find the lowest available color
        color = 0
        while color in neighbor_colors:
            color += 1

        # Assign the color to the vertex
        coloring[vertex] = color

    # Draw the graph with the assigned colors
    node_colors = [coloring.get(node, -1) for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=node_colors)
    plt.show()


def color_graph_with_spanning_tree_with_nodes(G, T, node1, node2):
    print("Color graph with spanning tree")

    # Find the leaves in the spanning tree
    leaves = [node for node in T.nodes() if T.degree(node) == 1]

    # Color the leaves first
    coloring = {}
    for leaf in leaves:
        coloring[leaf] = 0

    # Set the same color for node1 and node2
    color = max(coloring.values()) + 1
    coloring[node1] = color
    coloring[node2] = color

    # Remove node1 and node2 from the graph G
    G_without_nodes = G.copy()
    G_without_nodes.remove_nodes_from([node1, node2])

    # Use the first function to color the remaining nodes
    sorted_vertices = sort_vertices_by_layers(G_without_nodes, T)

    # Traverse G_without_nodes in the sorted order and assign colors
    for vertex in sorted_vertices:
        # Get the colors of the valid neighbors in coloring
        neighbor_colors = {coloring[neighbor] for neighbor in G[vertex] if neighbor in coloring}

        # Find the lowest available color
        color = 0
        while color in neighbor_colors:
            color += 1

        # Assign the color to the vertex
        coloring[vertex] = color

    # Draw the graph with the assigned colors
    node_colors = [coloring.get(node, -1) for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=node_colors)
    plt.show()


def build_graph():
    G = nx.Graph()

    edges = edges_entry.get().split()
    for edge in edges:
        u, v = edge.split(',')
        G.add_edge(u, v)

    pos = nx.spring_layout(G)

    if is_complete(G) or has_odd_cycle(G):
        raise Exception("The graph is complete or contains an odd cycle")

    if max_degree(G) <= 2:
        colour_two_deg(G)
        return
    else:
        vertex = vertex_with_less_than_max_degree(G)
        if vertex is not None:
            T = nx.bfs_tree(G, vertex)
            color_graph_with_spanning_tree(G, T)
        else:
            vertex = one_vertex_cover(G)
            if vertex is not None:
                subgraphs = split_graph(G, vertex)
                for subgraph in subgraphs:
                    T = nx.bfs_tree(subgraph, vertex)
                    # color_graph_with_spanning_tree_with_nodes(G,T)
            else:
                x, y, z = find_x_y_z(G)
                if x is not None and y is not None and z is not None:
                    print(f" x = {x} y = {y} z = {z}")
                    modified_graph = G.copy()
                    modified_graph.remove_nodes_from([y, z])
                    modified_graph.add_node(y)
                    modified_graph.add_node(z)
                    if x in modified_graph:
                        print("here")
                        modified_graph.add_edge(x, y)
                        modified_graph.add_edge(x, z)
                        T = nx.bfs_tree(modified_graph, x)
                        print(T)
                        color_graph_with_spanning_tree_with_nodes(G, T, y, z)


root = tk.Tk()
root.title("Graph Builder")

edges_label = tk.Label(root, text="Add Edges (comma-separated):")
edges_label.pack()

edges_entry = tk.Entry(root)
edges_entry.pack()

build_graph_button = tk.Button(root, text="Build Graph", command=build_graph)
build_graph_button.pack()

root.mainloop()
