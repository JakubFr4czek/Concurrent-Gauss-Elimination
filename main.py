from traces_theory import traces_run
from scheduler import scheduler_run

input = 'input/example_input.txt'
output = 'output/gauss_output.txt'

'''
Graf dla macierzy o rozmiarze > 10 staje się nieczytelny i nie jest obliczany,
można to zmienić poprzez ustawienie flagi force_graph na True

traces_run i scheduler run działają niezależnie, pierwsza funkcja służy tylko do wyznaczenia
obiektów matematycznych dotyczących teorii śladów, a druga do wyznaczenia rozwiązania układu równań 
'''

traces_run(input, force_graph = False)

scheduler_run(input, output)