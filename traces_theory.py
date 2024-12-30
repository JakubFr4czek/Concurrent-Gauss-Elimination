from utility import input_to_matrix, load_input, save_graph_as_DOT, save_traces_theory_output
from tools import calculate_operations, calculate_dependence, gauss_as_symbols, diekert_graph, get_foaty, get_alphabet
from graphviz import Source
import os

def traces_run(filename, force_graph):
    
    matrix, vector = input_to_matrix(load_input(filename))
    operations = calculate_operations(matrix)
    symbols = gauss_as_symbols(matrix)

    alphabet = get_alphabet(symbols)

    w = alphabet

    D = calculate_dependence(symbols)

    G = diekert_graph(alphabet, D)

    foaty = get_foaty(alphabet)

    if len(matrix) <= 10 or force_graph:

        os.makedirs('tmp', exist_ok=True)
        save_graph_as_DOT(G, alphabet, 'tmp/G.dot')
        
        source = Source.from_file('tmp/G.dot')
        source.render('output/diekert_graph', format='png', view=False, cleanup=True)
        
        os.remove('tmp/G.dot')
        os.rmdir('tmp')

    save_traces_theory_output(alphabet, D, w, foaty)

