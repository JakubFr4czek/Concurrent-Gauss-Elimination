'''
Moduł zawiea funkcje pomocnicze, służące do zapisu oraz odczytu z plików
'''

def load_input(filename = 'example_input.txt'):
    '''
    Funkcja wczytuje całą zawartość pliku
    '''
    
    with open(filename, 'r') as file:
        file_contents = file.readlines()

    return file_contents
    
def input_to_matrix(input):
    '''
    Przetłumaczenie zawartości pliku na macierz oraz wektor
    zgodnie z przyjętą konwencją:
    - pierwsza linia to rozmiar macierzy n
    - następne n lini o długości n to kolejne elementy macierzy
    - w n + 1 wierszu znajduje się wektor wyrazów wolnych
    '''
    
    matrix_size = int(input[0][:-1])
    
    # Macierz z wartościami
    matrix = []
    
    for row in range(1, matrix_size + 1):
        matrix.append(list(map(float, input[row].split())))
    
    # Wektor z wyrazami wolnymi
    vector = list(map(float, input[matrix_size + 1].split()))
        
    return matrix, vector
    
def save_graph_as_DOT(G, alphabet, filename = "tmp/G.dot"):
    '''
    Funkcja zapisuje graf Diekerta do pliku w formacie .dot
    '''

    with open(filename, "w") as file:
        file.write("digraph g {\n")
        file.write("rankdir=TB;\n")  # Vertically stack subgraphs
        
        # Ustawienia globalne
        file.write("node [style=filled];\n")  # Aby węzły były wypełnione kolorem
        
        # Zapisanie krawędzi
        for s1_id in range(len(G)):
            for s2_id in G[s1_id]:
                file.write(f"{s1_id} -> {s2_id}\n")

        prefix = alphabet[0][:3]
        
        file.write('subgraph '+prefix+' {\n')
        file.write("rank=same;\n")
        
        # Zapisanie węzłów z odpowiednimi etykietami i kolorami
        for i, symbol in enumerate(alphabet):
            
            if prefix != symbol[:3]:
                prefix = symbol[:3]
                file.write("}\n")  
                file.write('subgraph '+prefix+' {\n')
                file.write("rank=same;\n") 
            
            if 'A' in symbol:
                color = 'lightgreen'
            elif 'B' in symbol:
                color = 'orange'
            else:
                color = 'lightblue'
            
            file.write(f"{i} [label=\"{symbol}\", fillcolor={color}, style=filled]\n")
            
        file.write("}\n")  
        
        file.write("}\n")
    
    
def save_traces_theory_output(alphabet, D, w, foaty, filename = 'output/traces_theory_output.txt'):
    '''
    Funkcja zapisuje do pliku:
    - Alfabet w sensie teori śladów
    - Relację zależności
    - Algorytm eliminacji Gaussa w postaci ciągu symboli (słowo)
    - Postać normalną Foaty
    '''
    with open(filename, "w", encoding="utf-8") as file:
         
        file.write("Alfabet w sensie teorii śladów:\n")
         
        file.write("Σ = {\n")
        for i, element in enumerate(alphabet):
            separator = "," if i < len(alphabet) - 1 else ""
            file.write(f"  {element}{separator}")
            if (i + 1) % 5 == 0 or i == len(alphabet) - 1:
                file.write("\n")
            else:
                file.write(" ")
        file.write("}\n\n")
        
        file.write('Relacja zależności\n')
        
        file.write("D = sym{{\n")
        for i, element in enumerate(D):
            separator = "," if i < len(D) - 1 else ""
            file.write(f"  {element}{separator}")
            if (i + 1) % 5 == 0 or i == len(D) - 1:
                file.write("\n")
            else:
                file.write(" ")
        file.write("}^+} ∪ I_Σ\n\n")
        
        file.write('Algorytm eliminacj Gaussa w postaci ciągu symboli alfabetu:\n')
        
        file.write("w={<\n")
        for i, element in enumerate(w):
            separator = "," if i < len(w) - 1 else ""
            file.write(f"  {element}{separator}")
            if (i + 1) % 5 == 0 or i == len(w) - 1:
                file.write("\n")
            else:
                file.write(" ")
        file.write(">}\n\n")
        
        file.write('Postać normalna Foaty:\n')
        
        file.write("FNF= {\n")
        for cls in foaty:
            file.write("[{")
            for i, element in enumerate(cls):
                separator = "," if i < len(cls) - 1 else ""
                file.write(f"  {element}{separator}")
                if (i + 1) % 5 == 0:
                    file.write("\n")
                else:
                    file.write(" ")
            file.write("}]⌢\n")
        file.write("}")

def save_gauss_result(M, X, filename = 'output/gauss_output.txt'):
    '''
    Zapisuje wyniki obliczeń do pliku
    '''
    
    with open(filename, "w", encoding="utf-8") as file:
        
        file.write(f"{len(M)}\n")
        
        for m in M:
            for el in m:
                file.write(f"{el} ")
            file.write("\n")
        
        for x in X:
            file.write(f"{x} ")