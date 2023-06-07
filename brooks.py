import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import collections


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
    max_edges = (num_nodes * (num_nodes - 1))
    return num_edges == max_edges


def max_degree(G):
    return max(dict(G.degree()).values())


def vertex_with_less_than_max_degree(G):
    max_deg = max_degree(G)
    for node, degree in dict(G.degree()).items():
        if degree < max_deg:
            return node
    return None


def bfs_color(G, root):
    print("Inside BFS Color")
    coloring = {}
    queue = collections.deque([(root, 0)])
    while queue:
        node, level = queue.popleft()
        print("Colouring Node Number: ")
        print(node);
        # Assign color based on level
        coloring[node] = level % 2
        for neighbor in G[node]:
            if neighbor not in coloring:
                queue.append((neighbor, level + 1))
    return coloring


def greedy_draw_graph(G):
    root = list(G.nodes())[0]
    leaves = [node for node in G.nodes() if G.degree(node) == 1]

    # Color the leaves first
    coloring = {}
    for leaf in leaves:
        coloring[leaf] = 0

    # Color the rest of the nodes
    for node in nx.dfs_postorder_nodes(G, source=root):
        if node != root and node not in coloring:
            neighbor_colors = set(coloring[neighbor] for neighbor in G[node])
            for color in range(len(neighbor_colors) + 1):
                if color not in neighbor_colors:
                    coloring[node] = color
                    break

    # Get the color of the first neighbor of the root
    root_neighbor = next(iter(G[root]))
    root_color = coloring[root_neighbor]

    # Color vertex 1 and vertex 3 with the same color as the root neighbor
    coloring[1] = root_color
    coloring[3] = root_color

    # Color the root node last
    neighbor_colors = set(coloring[neighbor] for neighbor in G[root])
    for color in range(len(neighbor_colors) + 1):
        if color not in neighbor_colors:
            coloring[root] = color
            break

    # Get the number of colors used in the coloring
    num_colors = max(coloring.values()) + 1

    # Create a colormap with enough colors
    colormap = cm.get_cmap('viridis', num_colors)

    # Assign the colors to the nodes based on the coloring
    node_colors = [colormap(coloring[node]) for node in G.nodes()]

    nx.draw(G, with_labels=True, node_color=node_colors)
    plt.show()



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

def color_graph_with_spanning_tree(G, T, node1, node2):
    print("Color graph with spanning tree")

    # Find the leaves in the spanning tree
    leaves = [node for node in T.nodes() if T.degree(node) == 1]

    # Color the leaves first
    coloring = {}
    for leaf in leaves:
        coloring[leaf] = 0

    # Color the rest of the nodes in a greedy manner
    for node in nx.dfs_postorder_nodes(T):
        if node in coloring:
            continue
        neighbor_colors = set(coloring[neighbor] for neighbor in T[node])
        color = 0
        while color in neighbor_colors:
            color += 1
        coloring[node] = color

    # Set the same color for node1 and node2
    color = max(coloring.values()) + 1
    coloring[node1] = color
    coloring[node2] = color

    # Get the number of colors used in the coloring
    num_colors = max(coloring.values()) + 1

    # Create a colormap with enough colors
    colormap = cm.get_cmap('viridis', num_colors)

    # Assign the colors to the nodes based on the coloring
    node_colors = [colormap(coloring[node]) for node in G.nodes()]

    # Print each node and its color
    for node, color in zip(G.nodes(), node_colors):
        print(f"Node {node}: Color {color}")

    # Draw the graph with the assigned colors
    nx.draw(G, with_labels=True, node_color=node_colors)
    plt.show()






def main():
    G = nx.Graph()

    G.add_edge(1, 7)
    G.add_edge(1, 5)
    G.add_edge(1, 4)
    G.add_edge(2, 5)
    G.add_edge(2, 7)
    G.add_edge(2, 8)
    G.add_edge(3, 6)
    G.add_edge(3, 7)
    G.add_edge(3, 8)
    G.add_edge(4, 6)
    G.add_edge(4, 8)
    G.add_edge(5, 6)

    

    if is_complete(G) or has_odd_cycle(G):
        raise Exception("the graph is complete or contains an odd cycle")

    if max_degree(G) <= 2:
        # Find a valid coloring
        coloring = nx.coloring.greedy_color(G)
        colors = ['red', 'blue']

        for node in coloring:
            G.nodes[node]['color'] = colors[coloring[node]]

        node_colors = [nx.get_node_attributes(
            G, 'color')[node] for node in G.nodes()]
        nx.draw(G, with_labels=True, node_color=node_colors)
        plt.show()
    else:
        vertex = vertex_with_less_than_max_degree(G)
        if vertex is not None:
            T = nx.bfs_tree(G, vertex)
            greedy_draw_graph(T)
        else:
            print("test")
            vertex = one_vertex_cover(G)
            if vertex is not None:
                subgraphs = split_graph(G, vertex)
                print("test2")
                for subgraph in subgraphs:
                    T = nx.bfs_tree(subgraph, vertex)
                    print("Spanning Tree Edges:")
                    print(T.edges())
                    greedy_draw_graph(T)
            else:
                print("test3")
                x, y, z = find_x_y_z(G)
                if x is not None and y is not None and z is not None:
                    print(f" x = {x} y = {y} z = {z}")
                    modified_graph = G.copy()
                    modified_graph.remove_nodes_from([y, z])
                    modified_graph.add_node(y)
                    modified_graph.add_node(z)
                    if x in modified_graph:
                        modified_graph.add_edge(x, y)
                        modified_graph.add_edge(x, z)
                        T = nx.bfs_tree(modified_graph, x)
                        print(T)
                        color_graph_with_spanning_tree(G,T,y,z)

if __name__ == "__main__":
    main()
