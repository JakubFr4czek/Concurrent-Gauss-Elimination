from itertools import chain

'''
Moduł zawiera funkcje odpowiedzialne za wyznaczanie
obiektów matematycznych dotyczących teorii śladów
'''

def calculate_operations(matrix):
    ''' 
    Funkcja wyznacza kolejne operacje jakie należy wykonać na rzędach macierzy.
    
    Służyła ona jedynie do wizualizacji i nie została finalnie wykorzystana.
    '''
    
    d_count = 1
    
    operations = []
    
    for i in range(0, len(matrix)):
        for j in range(i + 1, len(matrix)):
            operations.append(f"D_{d_count}: w_{j + 1} - w_{i + 1} * {matrix[j][i]} / {matrix[i][i]}")
            d_count += 1
            
    return operations
    
def gauss_as_symbols(matrix):
    '''
    Wyznacza symbole odpowiadające poszczególnym operacjom
    
    A_a_b = M[b][a] / M[a][a]
    B_a_i_b = M[a][i] * A_a_b
    C_a_i_b = M[b][i] - B_a_i_b
    
    i - dla którego elementu jest wykonywana operacja
    '''
    
    symbols = []
    
    for i in range(0, len(matrix)):
        for j in range(i + 1, len(matrix)):
            symbol_series = []
            symbol_series.append(f"A_{i+1}_{j+1}")
            for k in range(i, len(matrix) + 1):
                symbol_series.append(f"B_{i+1}_{k+1}_{j+1}")
                symbol_series.append(f"C_{i+1}_{k+1}_{j+1}")
            symbols.append(symbol_series)
            
    return symbols

def unpack_symbol(symbol):
    '''
    Funkcja rozpakowuje symbol, tj. dla:
    A_i_j -> [i, j]
    B_i_j_k -> [i, j, k]
    '''
    
    first = symbol.find('_')
    second = symbol.find('_', first + 1)
    third = symbol.find('_', second + 1)
    
    if first != -1 and second != -1 and third != -1:
        return ([int(symbol[first + 1:second]), int(symbol[second + 1:third]), int(symbol[third+1:])])
    elif first != -1 and second != -1:
        return (int(symbol[first + 1:second]), int(symbol[second + 1:]))

    return ()
    
    

def calculate_dependence(symbols):
    '''
    Funkcja wyznaczająca relacje zależności dla każdego symbolu. Została
    napisana w taki sposób, aby wyznaczała tylko niezbędne relacje i brała
    pod uwagę, że np. jeśli (A, B), (B, C), (A, C) to wystarczy napisać, że
    (A, B), (B, C).
    '''
    
    def calcualte_A_dependency(symbol):
        a, b = unpack_symbol(symbol)
        
        #print(symbol, unpack_symbol(symbol))
        D = []
        
        # Wyliczam a - 1 i sprawdzam, czy jest > 0:
        if int(a) - 1 > 0:
            
            C1 = f"C_{int(a) - 1}_{a}_{b}"        
            C2 = f"C_{int(a) - 1}_{a}_{a}"
        
            D.extend([C1, C2])
            
        return D
        
    def calculate_B_dependency(symbol):
        a, i, b = unpack_symbol(symbol)
        
        D = []

        if int(a) - 1 > 0:
    
            C = f"C_{int(a) - 1}_{i}_{a}"
            
            # Sprawdzam, czy wyrażenie nie zostało już obliczone przy wyliczaniu A_ab
            if C not in calcualte_A_dependency(f"A_{a}_{b}"):
                D.append(C)
        
        # Każde B jest zależne od A_ab
        D.append(f"A_{a}_{b}")
                
        return D
    
    def calculate_C_dependency(symbol):
        a, i ,b = unpack_symbol(symbol)
        
        D = []
        
        if int(a) - 1 > 0:
            
            C = f"C_{int(a) - 1}_{i}_{b}"
            
            # Sprawdzam, czy wyrażenie nie zostało już obliczone przy wyliczaniu B_aib lub A_ab
            if C not in calculate_B_dependency(f"B_{a}_{i}_{b}") and C not in calcualte_A_dependency(f"A_{a}_{b}"):
                D.append(C)
        
        #Każde C jest zależne od B_aib i od A_ab
        D.append(f"B_{a}_{i}_{b}")
        #D.append("A_"+a+b) # Tego już nie trzeba dodawać
        
        return D
        
    # Tylko bezpośrednie zależności
    D = []
    
    # Iteruję po wszystkich symbolach
    for row in symbols:
        for symbol in row:
            # Wyliczam od których operacji symbol jest on zależny
            if symbol[0] == 'A': 
                res = calcualte_A_dependency(symbol)
            elif symbol[0] == 'B':
                res = calculate_B_dependency(symbol)
            elif symbol[0] == 'C':
                res = calculate_C_dependency(symbol)
            else:
                res = []
            
            D.extend([(el, symbol) for el in res])
        
    return D    
    
def diekert_graph(alphabet, D):
    '''
    Funkcja zapisująca relację zależności jako graf
    w postaci listy sąsiedztwa.
    '''
    
    # Przypisuję wszystkim symbolom unikalne numery
    symbol_id = {}
    
    for i, symbol in enumerate(alphabet):
        symbol_id.update({symbol : i})
        
    # Tworzę graf G = (V, E)
    G = [[] for _ in range(len(alphabet))]
    
    # Dodaję relacje zależności do grafu G,
    # Należy pamiętać, że G jest skierowany
    # zatem s2 jest zależne od s1
    for s1, s2 in D:
        s1_id = symbol_id[s1]
        s2_id = symbol_id[s2]
        
        G[s1_id].append(s2_id)
        
    return G

def get_alphabet(symbols):
    '''
    Spłaszcza wygenerowaną listę symboli. One już są
    unikalne więc wszystkie będą stanowić alfabet
    '''
    return list(chain.from_iterable(symbols))

def get_foaty(alphabet):
    '''
    Funkcja wyznaczająca klasy Foaty.
    Korzysta z tego, że najpierw muszą się wykonać 
    wszystkie operacje A_1, potem B_1, C_1, A_2, B_2, ...
    Co znacznie upraszcza wyznaczanie klasy Foaty.
    '''
    
    foaty = []

    alphabet_sorted = sorted(alphabet, key=lambda x : (unpack_symbol(x)[0], x[0]))
    
    prefix = alphabet_sorted[0][:alphabet_sorted[0].find('_', 2)]
    current_foaty = []
    
    for symbol in alphabet_sorted:
        if prefix == symbol[:symbol.find('_', 2)]:
            current_foaty.append(symbol)
        else: 
            foaty.append(current_foaty)
            prefix = symbol[:symbol.find('_', 2)]
            current_foaty = [symbol]
    foaty.append(current_foaty)
    return foaty