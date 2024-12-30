import os
from scheduler import scheduler_run

'''
Plik udostępniający interfejs do komunikacji
ze sprawdzarką w pythonie
'''

def compile_generator():
    '''
    Funkcja kompiluje kod generatora układów równań
    '''
    
    os.chdir('./sprawdzarka')
    os.system(f'javac -cp . Generator.java')
    os.chdir('..')

def generate(n):
    '''
    Generuje macierz nxn i wektor 1xn w pliku sprawdzarka/input/input.txt
    oraz oczekiwany wynik po przeprowadzeniu eliminacji Gaussa w pliku sprawdzarka/output/output.txt
    '''   

    os.chdir('./sprawdzarka')
    os.system(f'java -cp . Generator {n} input/input.txt output/output.txt')
    os.chdir('..')
    
def compile_checker():
    '''
    Funkcja kompiluje kod checkera
    '''
    
    os.chdir('./sprawdzarka')
    os.system(f'javac -cp . Checker.java')
    os.chdir('..')
    
def checker(input, output):
    '''
    Uruchamia sprawdzarkę, przyjmuje argumenty input i output, gdzie:
    - input - lokalizacja wejścia do algorytmu eliminacji Gaussa
    - output - lokalizacja wyjścia z algorytmu eliminacji Gaussa
    '''

    os.chdir('./sprawdzarka')
    os.system(f'java -cp . Checker {input} {output}')
    os.chdir('..')

def check(n):
    '''
    Funkcja generuje macierz o rozmiarze nxn i wektor 1xn korzystając z załączonego kodu sprawdzarki
    a następnie sprawdza, czy implementacja algorytmu Gaussa zaproponowana przez Studenta jest poprawna
    '''

    print("Kompilowanie generatora...")
    compile_generator()
    
    print("Kompilowanie checkera...")
    compile_checker()

    print("Generowanie układu równań...")
    generate(n)
    
    input = 'input/input.txt'
    output = 'output/user_output.txt'
    
    print("Uruchomienie schedulera...")
    scheduler_run('sprawdzarka/' + input, 'sprawdzarka/' + output)
    
    print("Uruchomienie checkera...")
    checker(input, output)
    


check(100)
