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
    coloring = {}
    queue = collections.deque([(root, 0)])
    while queue:
        node, level = queue.popleft()
        # Assign color based on level
        coloring[node] = level % 2
        for neighbor in G[node]:
            if neighbor not in coloring:
                queue.append((neighbor, level + 1))
    return coloring


def greedy_draw_graph(G):
    # Choose a root node
    root = list(G.nodes())[0]

    # Color the nodes using BFS coloring
    coloring = bfs_color(G, root)

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


def main():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(1, 5)
    G.add_edge(1, 4)
    G.add_edge(2, 6)
    G.add_edge(2, 3)
    G.add_edge(3, 7)
    G.add_edge(3, 4)
    G.add_edge(4, 8)
    G.add_edge(5, 6)
    G.add_edge(5, 8)
    G.add_edge(7, 8)
    G.add_edge(6, 7)
    # G.add_edge(4, 8)
    # G.add_edge(4, 8)
    # G.add_edge(4, 8)
    # G.add_edge(4, 8)
    # G.add_edge(4, 8)

    #G = nx.Graph()
    #G.add_edges_from([(1, 2), (1, 3), (1, 4)])
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
                        greedy_draw_graph(T)



    print(f"The maximum degree in the graph is: {max_degree(G)}")
    print(f"The graph is connected: {is_connected(G)}")


if __name__ == "__main__":
    main()
