import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def plot_solution( n , path , M):
    adj_matrix = np.zeros((n, n), dtype='int')
    for i in range(len(path) - 1):
        adj_matrix[ path[ i ] ][path[ i + 1 ] ] = M[ path[ i ] ][ path[ i + 1 ] ]

    G_latest = nx.from_numpy_array(adj_matrix, create_using=nx.DiGraph)
    nodes_pos = nx.kamada_kawai_layout(G_latest)

    scale_factor = 2
    pos_scaled = {
        node: (scale_factor * x if x < 4 else x, scale_factor * y if y < 4 else y)
        for node, (x, y) in nodes_pos.items()
    }
    # Extract edge weights for plotting
    edge_weights = nx.get_edge_attributes(G_latest, 'weight')

    plt.figure(figsize=(10, 10))
    nx.draw(G_latest, pos_scaled, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', arrows=True, arrowsize=20)
    nx.draw_networkx_edge_labels(G_latest, pos_scaled, edge_labels=edge_weights, font_color='red')
    plt.title("Solution:")
    plt.savefig('solution.png', format='png', dpi=300)
    plt.show()
    
    
def plot_problem(M):
    M0 = np.array(M,dtype='int')
    G_latest = nx.from_numpy_array(M0 , create_using=nx.DiGraph)
    nodes_pos = nx.spring_layout(G_latest)

    scale_factor = 3
    pos_scaled = {
        node: (scale_factor * x if x < 4 else x, scale_factor * y if y < 4 else y)
        for node, (x, y) in nodes_pos.items()
    }
    # Extract edge weights for plotting
    edge_weights = nx.get_edge_attributes(G_latest, 'weight')


    plt.figure(figsize=(10, 10))
    nx.draw(G_latest, pos_scaled, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', arrows=True, arrowsize=20)
    nx.draw_networkx_edge_labels(G_latest, pos_scaled, edge_labels=edge_weights, font_color='red')
    plt.title("Problem:")
    plt.show()
    plt.savefig('problem.png', format='png', dpi=300)