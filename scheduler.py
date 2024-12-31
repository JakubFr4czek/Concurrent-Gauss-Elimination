from utility import input_to_matrix, load_input
from tools import gauss_as_symbols, get_foaty, unpack_symbol, get_alphabet
from utility import save_gauss_result
import numpy as np
import warnings
from numba import cuda, NumbaPerformanceWarning    

@cuda.jit
def gaussian_elimination_A_kernel(M, A, cls):
    thread_id = cuda.grid(1)

    if thread_id < len(cls):
        a, b = cls[thread_id]
    
        A[a][b] = M[b][a] / M[a][a]
    
    
@cuda.jit
def gaussian_elimination_B_kernel(M, A, B, cls):
    thread_id = cuda.grid(1)
    
    if thread_id < len(cls):
        a, i, b = cls[thread_id]
        
        B[a][i][b] = M[a][i] * A[a][b]
    
@cuda.jit
def gaussian_elimination_C_kernel(M, B, cls):
    thread_id = cuda.grid(1)
    
    if thread_id < len(cls):
        a, i, b = cls[thread_id]
        
        M[b][i] = M[b][i] - B[a][i][b]


def gaussian_elimination_cuda(Arr, Vec, foaty):
    Arr = np.array(Arr, dtype=np.float64)
    Vec = np.array(Vec, dtype=np.float64)
    
    # Macierz do przeliczenia
    M = np.column_stack((Arr, Vec))
    M_cuda = cuda.to_device(M)
    
    # Tablice na kolejne wyniki obliczeń
    # dla uproszczenia wszystkie rozmiarow wyjsciowej macierzy
    A = np.zeros(M.shape)
    B = np.zeros((M.shape[0], M.shape[1], max(M.shape[0], M.shape[1])))
    
    A_cuda = cuda.to_device(A)
    B_cuda = cuda.to_device(B)
    
    device = cuda.get_current_device()
    max_threads_per_block = device.MAX_THREADS_PER_BLOCK
    
    for cls in foaty:
        
        if cls[0][0] == 'A':
            
            cls_cuda = cuda.to_device(list(map(lambda x: (x[0] - 1, x[1] - 1),map(lambda x : unpack_symbol(x), cls)))) 
            
            blocks_per_grid = (len(cls) + (max_threads_per_block - 1)) // max_threads_per_block

            gaussian_elimination_A_kernel[blocks_per_grid, max_threads_per_block](M_cuda, A_cuda, cls_cuda)
            
        elif cls[0][0] == 'B':
            
            cls_cuda = cuda.to_device(list(map(lambda x : (x[0] - 1, x[1] - 1, x[2] - 1),map(lambda x : unpack_symbol(x), cls)))) 
            
            blocks_per_grid = (len(cls) + (max_threads_per_block - 1)) // max_threads_per_block
            
            gaussian_elimination_B_kernel[blocks_per_grid, max_threads_per_block](M_cuda, A_cuda, B_cuda, cls_cuda)
            
        elif cls[0][0] == 'C':
            
            cls_cuda = cuda.to_device(list(map(lambda x : (x[0] - 1, x[1] - 1, x[2] - 1),map(lambda x : unpack_symbol(x), cls)))) 
            
            blocks_per_grid = (len(cls) + (max_threads_per_block - 1)) // max_threads_per_block
            
            gaussian_elimination_C_kernel[blocks_per_grid, max_threads_per_block](M_cuda, B_cuda, cls_cuda)
            
        else:
            raise Exception("Wrong foaty class!")
        
        cuda.synchronize()
    
    cuda.synchronize()
    M = M_cuda.copy_to_host()
    
    #X = back_substitution(M)
    X = to_identity_and_solve(M)
        
    return M[:, :-1], X

def back_substitution(M):
    n, m = M.shape
    X = np.zeros(n)
    
    X[n - 1] = M[n - 1][m - 1] / M[n - 1][n - 1]
    
    for i in range(n - 2, -1, -1):
        for j in range(i + 1, n):
            M[i][m - 1] -= M[i][j] * X[j]
        
        X[i] = M[i][m - 1] / M[i][i]
    
    return X

def to_identity_and_solve(M):
    n, m = M.shape
    X = np.zeros(n)
    
    for i in range(n - 1, -1, -1):
        M[i] /= M[i][i]
        for j in range(i):
            M[j] -= M[j][i] * M[i]

    return M[:, -1]



def scheduler_run(input, output):
    
    warnings.filterwarnings("ignore", category=NumbaPerformanceWarning)
    
    matrix, vector = input_to_matrix(load_input(input))
    symbols = gauss_as_symbols(matrix)
    alphabet = get_alphabet(symbols)
    foaty = get_foaty(alphabet)

    M, X = gaussian_elimination_cuda(matrix, vector, foaty)

    save_gauss_result(M, X, output )