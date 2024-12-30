import sys
from traces_theory import traces_run
from scheduler import scheduler_run

'''
Graf dla macierzy o rozmiarze > 10 staje się nieczytelny i nie jest obliczany,
można to zmienić poprzez ustawienie flagi force_graph na True

traces_run i scheduler run działają niezależnie, pierwsza funkcja służy tylko do wyznaczenia
obiektów matematycznych dotyczących teorii śladów, a druga do wyznaczenia rozwiązania układu równań 
'''

if len(sys.argv) == 3:
    input = sys.argv[1]
    output = sys.argv[2]
elif len(sys.argv == 1):
    input = 'input/example_input.txt'
    output = 'output/gauss_output.txt'
else:
    print("Użycie: python main.py <input_file> <output_file>")
    sys.exit(1)

traces_run(input, force_graph = False)

scheduler_run(input, output)