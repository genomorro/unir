# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] cell_id="94b304aee1c445ce8d55f7f86bf57de0" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=173
# # Librerías a utilizar
#
# Para la implementación del algoritmo CKY solo serán necesarias dos funciones adicionales, al primera permite seleccionar un elemento de una lista a partir del índice y la segunda para mostrar de manera más clara los resultados. 

# %% cell_id="8a5b061377e846f3be52a4bbf4af35c7" tags=[] deepnote_cell_type="code" deepnote_cell_height=84
from operator import itemgetter
from pprint import pprint

# %% [markdown] cell_id="b31d72d7d3d64d09a86ce31f36f84351" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=148
# # Datos de entrada
#
# La variable `file_grammar` que aparece a continuación emula las reglas gramaticales escritas en un archivo de texto. En este caso se han escrito las reglas propias del ejercicio.

# %% cell_id="b32b518154b440439790cc631fca8675" deepnote_to_be_reexecuted=false execution_millis=32 execution_start=1658943426884 source_hash="bf54f17d" tags=[] deepnote_cell_type="code" deepnote_cell_height=243
file_grammar = """
S -> NP VP
NP -> Det Nominal
NP -> Nominal Nominal
Nominal -> Nominal Noun
Nominal -> Nominal PP
VP -> Verb NP
VP -> Verb PP
PP -> Preposition NP
"""

# %% [markdown] cell_id="479bce7ebdca410db43f4ebe1cfebb25" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=80
# Se crea el lexicón, de forma común, en lingüística se dice que un elemento del lexicón en la entrada de un diccionario, entonces se define como tal en el código.

# %% cell_id="6b541fb5e70b4e3a9d8609bb05fed305" deepnote_to_be_reexecuted=false execution_millis=0 execution_start=1658943426917 source_hash="4d304a3a" tags=[] deepnote_cell_type="code" deepnote_cell_height=225
lexicon_dictionary = {
    'NP': {'time', 'flies', 'arrow'},
    'Nominal': {'time', 'flies', 'arrow'},
    'VP': {'time', 'flies', 'like'},
    'Verb': {'time', 'flies', 'like'},
    'Noun': {'time', 'flies', 'arrow'},
    'Det': {'an'},
    'Preposition': {'like'}
}

# %% [markdown] cell_id="9adc9507e54145b1bacedb7846d73691" tags=[] deepnote_to_be_reexecuted=false source_hash="866cdb3b" execution_start=1658818760262 execution_millis=11 deepnote_cell_type="markdown" deepnote_cell_height=105
# Se expresan las reglas gramaticales y lexicas en forma de tuplas como claves de una probabilidad que se usará para obtener las probabilidades de cada árbol obtenido por el algoritmo. Se eligen tuplas porque son fáciles de manejar, similar a los lenguajes Lisp.

# %% cell_id="db51863ebbc545379b2b7a0010451761" tags=[] deepnote_to_be_reexecuted=false source_hash="105f442" execution_start=1658943426917 execution_millis=1 deepnote_cell_type="code" deepnote_cell_height=549
probabilities = {
    ('Det', 'an'): 0.05,
    ('NP', ('Det', 'Nominal')): 0.3,
    ('NP', ('Nominal', 'Nominal')): 0.2,
    ('NP', 'arrow'): 0.002,
    ('NP', 'flies'): 0.002,
    ('NP', 'time'): 0.002,
    ('Nominal', ('Nominal', 'Noun')): 0.1,
    ('Nominal', 'arrow'): 0.002,
    ('Nominal', 'flies'): 0.002,
    ('Nominal', 'time'): 0.002,
    ('Nominal', ('Nominal', 'PP')): 0.2,
    ('Noun', 'arrow'): 0.01,
    ('Noun', 'flies'): 0.01,
    ('Noun', 'time'): 0.01,
    ('PP', ('Preposition', 'NP')): 0.1,
    ('Preposition', 'like'): 0.05,
    ('S', ('NP', 'VP')): 0.8,
    ('VP', ('Verb', 'PP')): 0.2,
    ('VP', 'flies'): 0.008,
    ('VP', 'like'): 0.008,
    ('VP', ('Verb', 'NP')): 0.3,
    ('VP', 'time'): 0.004,
    ('Verb', 'flies'): 0.02,
    ('Verb', 'like'): 0.02,
    ('Verb', 'time'): 0.01
    }


# %% [markdown] cell_id="1a0944238c664315879d9da01c13cc9f" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=105
# La función `grammar_rules()` recibe como argumento un texto con reglas gramaticales y las convierte en un diccionario que permite buscar a partir de los nodos hijos de un árbol un posible padre que complete la estructura, esta forma es básica para facilitar la búsqueda en el algoritmo CKY.

# %% cell_id="04460b36a83b48a389171450e1d61513" deepnote_to_be_reexecuted=false execution_millis=9 execution_start=1658943426919 source_hash="b9a5198b" tags=[] deepnote_cell_type="code" deepnote_cell_height=927
def grammar_rules(grammar_buffer):
    '''
    This function parse grammar rules writen in a text variable or a file.

    The text file contain grammar rules writen like:

    NP -> NP VP

    This function doesn't parse lexical rules.

    This function return a dictionary with parents indexed by children, like this:

    {('Det', 'Nominal'): ['NP'],
     ('NP', 'VP'): ['S'],
     ('Verb', 'PP'): ['VP']}

        Parameters:
            grammar_buffer (str): Text with grammar rules
        
        Returns:
            find_parent (dict): Dictionary with the rules indexed by children
    '''
    rules = []
    # leer cada línea del texto
    for line in grammar_buffer.strip().split("\n"):
        # separar cada línea en sus dos miembros
        parent, chidren = line.strip().split("->")
        # Quitar espacio en blanco posterior
        parent = parent.strip()
        # Distinguir los hijos
        chidren = chidren.split()
        #crear la regla (parent, (c1, c2)) como en lisp ;)
        rule = (parent, tuple(chidren))
        rules.append(rule)
    # Crear un diccionario con las reglas invertidas, eso permite buscar al nodo padre
    find_parent = dict()
    for parent, (lc, rc) in rules:
        # Si no existe la entrada, se crea
        if (lc, rc) not in find_parent:
            find_parent[lc, rc] = []
        # Se agrega el caso
        find_parent[lc,rc].append(parent)
    return find_parent

#parents = set(val[0] for val in list(find_parent.values()))
#for i in list(lexicon.keys()):
#    parents.add(i)



# %% [markdown] cell_id="b49c8873344c4a228a61419118b21b0c" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=250
# # Implementación de los algoritmos CKY y PCKY
#
# Ahora se implementa el algoritmo CKY, mismo que recibe como entrada una oración en forma de cadena de texto, un diccionario con reglas gramaticales y un lexicón adecuado a la gramática. Opcionalmente, se puede definir el argumento de entrada `verbose` al valor `True`, de esta manera se mostrará en pantalla cada uno de los pasos que sigue el algoritmo para crear la matriz correspondiente. Esta matriz también tendrá forma de diccionario.

# %% cell_id="2029ee31918d4ebc929da11c49765dd8" deepnote_to_be_reexecuted=false execution_millis=5 execution_start=1658943426929 output_cleared=false source_hash="22c26beb" tags=[] deepnote_cell_type="code" deepnote_cell_height=1395
def cky_parser(sentence, grammar, lexicon, verbose=False):
    ''' 
    The function cky_parser implements CKY algorithm.

        Parameters:
            sentence (str): A sentence to be analyzed
            grammar (dic): Dictionary with the grammar rules indexed by children
            lexicon (dic): Dictionary with lexical rules indexed by PoS
            verbose (bool): If it is True, show every step in the algorithm
        Returns:
            matrix_cky (dic): Dictionary with all possible cells written by the algorithm
    '''
    words = sentence.lower().split()
    if verbose:
        print(words)
    matrix_cky = dict()
    for i in range(len(words)):
        # Las ordenadas van del 0 al 4
        ordinate = 0
        if verbose:
            print("0: i=",i)
        # Las abscisas van de 1 a 5
        for abscissa in range(i+1, len(words)+1):
            # Se agrega una celda
            matrix_cky[(ordinate, abscissa)] = []
            if verbose:
                print("1: abscissa=",abscissa,"ordinate=",ordinate,"a-o=",abscissa-ordinate)
            # Si se opera sobre la diagonal
            if(abscissa-ordinate==1):
                # Combina la palabra con las categorías del lexicón
                for key in lexicon_dictionary:
                    if verbose:
                        print("2: key=",key,"word=",words[ordinate])
                    # Si la combinación existe en el lexicón se agrega a la matriz
                    if(words[ordinate] in lexicon[key]):
                        matrix_cky[(ordinate,abscissa)].append(
                            (key,0,words[ordinate],words[ordinate]))
                        if verbose:
                            print("2:",matrix_cky)
            # Si hay que operar sobre dos celdas
            elif(abscissa-ordinate>1):
                if verbose:
                    print("3:","(",ordinate,",",abscissa,")")
                # Obtener los valores de las celdas
                for index in range(abscissa-ordinate-1):
                    left = matrix_cky[(ordinate,abscissa-1-index)]
                    down = matrix_cky[(abscissa-1-index,abscissa)]
                    if verbose:
                        print("4: index=",index)
                        print("4: left=",left,"\n  ","down=",down)
                    # Si una de las celdas esta vacía no se hace nada
                    if not left or not down:
                        if verbose:
                            print("5: Nothing to do")
                    else:
                        # Combinar los valores de las celdas
                        for a in left:
                            for b in down:
                                # Obtiene el primer elemento de la tupla
                                # Crea la tupla para buscarla en las reglas
                                if((a[0],b[0]) in grammar):
                                    matrix_cky[(ordinate,abscissa)].append(
                                        (grammar[(a[0],b[0])][0],
                                        abscissa-1-index,a[0],b[0]))
                                    if verbose:
                                        print("6: add=",grammar[(a[0],b[0])][0],abscissa-1-index,a[0],b[0])
                                else:
                                    if verbose:
                                        print("6: Nothing to do")
            if verbose:
                print(matrix_cky)
                print("9: Next Ordinate")
            ordinate+=1
    return matrix_cky


# %% [markdown] cell_id="db5ce37a92ff47479d4f03561f1fb0ea" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=105
# Enseguida se crean dos funciones, la primera, `get_prob()`, se usará para obtener las probabilidades del diccionario de probabilidades, la segunda, `update_prob()`, se usará para actualizar las probabilidades desde los nodos intermedios hasta el nodo padre. 

# %% cell_id="7d434a11078b42148e95f9e4393219ae" tags=[] deepnote_to_be_reexecuted=false source_hash="f1536ffd" execution_start=1658943426937 execution_millis=3 output_cleared=true deepnote_cell_type="code" deepnote_cell_height=567
def get_prob(node, prob_dict):
    '''
    The function get_prob gets a probability from a dictionary.

        Parameters:
            node (tuple): It's a grammar or lexical rule writen in tuple format
            prob_dict (dict): Dictionary with rules as keys an probabilities as values
        Returns:
            prob_dict[node] (float): A probability
    '''
    return prob_dict[node]

def update_prob(left,down,actual, prob_dict):
    '''
        The function get_prob gets a probability from a dictionary.

                Parameters:
                    left (tuple): A tuple with information of a left node
                    down (tuple): A tuple with information of a right node
                    actual (str): Parent node value
                    prob_dict (dict): Dictionary with rules as keys an probabilities as values
                Returns:
                    prob_dict[node] (float): A probability
    '''

    actual_prob = get_prob((actual, (left[0],down[0])), prob_dict)
    prob = left[4] * down[4] * actual_prob
    return prob


# %% [markdown] cell_id="7e1d8f7197d246df96f18c73a2433c28" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=80
# Se actualiza `cky_parser()`. Ahora `pcky_parser()` agregará la información de la probabilidad a cada lista agregada a `matrix_pcky`.

# %% cell_id="6f31147a110644e0abf04b733ddada83" deepnote_to_be_reexecuted=false output_cleared=false source_hash="21fc62b3" tags=[] allow_embed=false execution_start=1658943426950 execution_millis=4 deepnote_cell_type="code" deepnote_cell_height=1467
def pcky_parser(sentence, grammar, lexicon, probabilities_table,verbose=False):
    ''' 
    The function pcky_parser implements PCKY algorithm.

        Parameters:
            sentence (str): A sentence to be analyzed
            grammar (dic): Dictionary with the grammar rules indexed by children
            lexicon (dic): Dictionary with lexical rules indexed by PoS
            probabilities_table (dic): Dictionary with the probability of lexical and gramar rules
            verbose (bool): If it is True, show every step in the algorithm
        Returns:
            matrix_pcky (dic): Dictionary with all possible cells written by the algorithm
    '''
    words = sentence.lower().split()
    if verbose:
        print(words)
    matrix_pcky = dict()
    for i in range(len(words)):
        # Las ordenadas van del 0 al 4
        ordinate = 0
        if verbose:
            print("0: i=",i)
        # Las abscisas van de 1 a 5
        for abscissa in range(i+1, len(words)+1):
            # Se agrega una celda
            matrix_pcky[(ordinate, abscissa)] = []
            if verbose:
                print("1: abscissa=",abscissa,"ordinate=",ordinate,"a-o=",abscissa-ordinate)
            # Si se opera sobre la diagonal
            if(abscissa-ordinate==1):
                # Combina la palabra con las categorías del lexicón
                for key in lexicon_dictionary:
                    if verbose:
                        print("2: key=",key,"word=",words[ordinate])
                    # Si la combinación existe en el lexicón se agrega a la matriz
                    if(words[ordinate] in lexicon[key]):
                        matrix_pcky[(ordinate,abscissa)].append(
                            (key,0,words[ordinate],words[ordinate],
                            get_prob((key,words[ordinate]),probabilities_table)))
                        if verbose:
                            print("2:",matrix_pcky)
            # Si hay que operar sobre dos celdas
            elif(abscissa-ordinate>1):
                if verbose:
                    print("3:","(",ordinate,",",abscissa,")")
                # Obtener los valores de las celdas
                for index in range(abscissa-ordinate-1):
                    left = matrix_pcky[(ordinate,abscissa-1-index)]
                    down = matrix_pcky[(abscissa-1-index,abscissa)]
                    if verbose:
                        print("4: index=",index)
                        print("4: left=",left,"\n  ","down=",down)
                    # Si una de las celdas esta vacía no se hace nada
                    if not left or not down:
                        if verbose:
                            print("5: Nothing to do")
                    else:
                        # Combinar los valores de las celdas
                        for a in left:
                            for b in down:
                                # Obtiene el primer elemento de la tupla
                                # Crea la tupla para buscarla en las reglas
                                if((a[0],b[0]) in grammar):
                                    matrix_pcky[(ordinate,abscissa)].append(
                                        (grammar[(a[0],b[0])][0],
                                        abscissa-1-index,a[0],b[0],
                                        update_prob(a,b,grammar[(a[0],b[0])][0],probabilities_table))
                                        )
                                    if verbose:
                                        print("6: add=",grammar[(a[0],b[0])][0],abscissa-1-index,a[0],b[0])
                                else:
                                    if verbose:
                                        print("6: Nothing to do")
            if verbose:
                print(matrix_pcky)
                print("9: Next Ordinate")
            ordinate+=1
    return matrix_pcky


# %% [markdown] cell_id="ccca19febc534941b7000444df7a28d0" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=148
# # Obtención de resultados
#
# La función `tree()` recorre una matriz generada por el algoritmo CKY en busca de árboles a partir del valor de un nodo en particular, tomando en cuenta una ruta a través de un índice creado por el algoritmo. 

# %% cell_id="76d00b96a1184619a033b0574681f6b1" deepnote_to_be_reexecuted=false execution_millis=5 execution_start=1658943426962 output_cleared=false source_hash="de760aab" tags=[] deepnote_cell_type="code" deepnote_cell_height=1305
def tree (matrix,cell,parent="S",index=0,pcky=False):
    '''
    Create a tree from a matrix created by the CKY algorithm.
    See def cky_parser(sentence, grammar, lexicon, verbose=False) function.

        Parameters:
            matrix (dic): Dictionary with CKY algorithm information
            cell (tuple): Node in the matrix to start the analysis
            parent (str): Axiom in the grammar or parent node value for the tree
            index (int): If there is more than one value in cell, this variable let choose which one analyze
            pcky (bool): Enable if matrix contains PCKY algorithm information
        Returns:
            list (list): A list with trees in list shape
    '''
    list = []
    # Revisa que la lista no este vacía
    if len(matrix[cell]) == 0:
        return list
    # Revisa que el índice sea 0, significa que es una hoja
    if matrix[cell][0][1] == 0:
        # Encuentra la hoja que corresponde
        if matrix[cell][index][0] == parent:
            if pcky:
                return [(matrix[cell][index][0],matrix[cell][index][4]), matrix[cell][index][2]]
            else:
                return [matrix[cell][index][0], matrix[cell][index][2]]
        else:
            # Busca en otra hoja
            if index+1 < len(matrix[cell]):
                if pcky:
                    return tree(matrix,cell,parent,index+1,pcky=True)
                else:
                    return tree(matrix,cell,parent,index+1)
            else:
                return list
    # Si no es una hoja, revisa si es la opción correcta
    elif (matrix[cell][index][0]) == parent:
        # Agrega el símbolo
        if pcky:
            list.append((matrix[cell][index][0],matrix[cell][index][4]))
        else:
            list.append(matrix[cell][index][0])
        # Buscar hijos
        child = []
        # Hijo derecho
        if pcky:
            child.append(
                tree(matrix,(cell[0],matrix[cell][index][1]),matrix[cell][index][2],pcky=True))
        else:
            child.append(
                tree(matrix,(cell[0],matrix[cell][index][1]),matrix[cell][index][2]))
        # Hijo izquierdo
        if pcky:
            child.append(
                tree(matrix,(matrix[cell][index][1],cell[1]),matrix[cell][index][3],pcky=True))
        else:
            child.append(
                tree(matrix,(matrix[cell][index][1],cell[1]),matrix[cell][index][3]))
        #Agrega child a la lista
        list.append(child)
        return list
    else:
        if index+1 < len(matrix[cell]):
            if pcky:
                return tree(matrix,cell,parent,index+1,pcky=True)
            else:
                return tree(matrix,cell,parent,index+1)
        else:
            return list


# %% [markdown] cell_id="9c7f41909d5f46c88de820e1973b22ac" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=80
# La función `find_solutions()` servirá como _frontend_ para todas las funciones anteriores, brindará la respuesta propuesta por el algoritmo.

# %% cell_id="9184406a11784cf79803682be1f96ece" tags=[] deepnote_to_be_reexecuted=false source_hash="c900d07e" execution_start=1658943426974 execution_millis=6 deepnote_cell_type="code" deepnote_cell_height=657
def find_solutions(sentence,grammar,lexicon,axiom,probabilities_table={},verbose=False):
    '''
    Find all possible solutions of a CKY analysis in a sentence.

        Parameters:
            sentence (str): A sentence to be analyzed
            grammar (dic): Dictionary with the grammar rules indexed by children
            lexicon (dic): Dictionary with lexical rules indexed by PoS
            axiom (str): Axiom in the grammar
            probabilities_table (dic): Dictionary with the probability of lexical and gramar rules
            verbose (bool): If it is True, show every step in the algorithm

        Returns:
            solutions (list): List with all possible solutinos suggested by the algorithm
    '''
    N = len(sentence.split())
    solutions = []
    if probabilities_table:
        matrix_pcky = pcky_parser(sentence,grammar,lexicon,probabilities_table,verbose)
        candidates = []
        # Busca en (0,N) aquellas listas que contengan el axioma
        for i in enumerate(matrix_pcky[(0,N)]):
            if i[1][0] == axiom:
                candidates.append([i[1][0],i[1][1],i[1][4]])
        # Selecciona aquel con mayor probabilidad
        candidates = max(candidates,key=itemgetter(2))
        solutions = tree(matrix_pcky,(0,N),index=candidates[1],pcky=True)
    else:
        matrix_cky = cky_parser(sentence,grammar,lexicon,verbose)
        for i in enumerate(matrix_cky[(0,N)]):
            if i[1][0] == axiom:
                solutions.append(tree(matrix_cky,(0,N),index=i[0]))
    return solutions


# %% cell_id="24372a71ab9b420b89af86f9d5abf213" tags=[] deepnote_to_be_reexecuted=false source_hash="ec9e4ca2" execution_start=1658943426990 execution_millis=5 deepnote_cell_type="code" deepnote_cell_height=444 deepnote_output_heights=[607, 427]
options = find_solutions("Time flies like an arrow",
                        grammar_rules(file_grammar),
                        lexicon_dictionary,
                        "S")
pprint(options)

# %% cell_id="483bb40a252c4d6aa7115096d13b2a33" tags=[] deepnote_to_be_reexecuted=false source_hash="afdc579" allow_embed=false execution_start=1658943426997 execution_millis=12 deepnote_cell_type="code" deepnote_cell_height=388
options = find_solutions("Time flies like an arrow",
                        grammar_rules(file_grammar),
                        lexicon_dictionary,
                        "S",probabilities)
pprint(options)

# %% [markdown] cell_id="85a07328407f41fc8f557803409dd2c2" tags=[] deepnote_cell_type="markdown" deepnote_cell_height=82
# # Test code

# %% cell_id="04fdcca0d54d47b1b0bb3b561e523342" tags=[] deepnote_to_be_reexecuted=false source_hash="7b30353" execution_start=1658943427010 execution_millis=2 deepnote_cell_type="code" deepnote_cell_height=81
cky = pcky_parser("Time flies like an arrow", grammar_rules(file_grammar), lexicon_dictionary,probabilities)

# %% cell_id="ba40423116664332a0cf7e931653015a" tags=[] deepnote_to_be_reexecuted=false source_hash="4b0bf3fa" allow_embed=false execution_start=1658943427015 execution_millis=4 deepnote_cell_type="code" deepnote_cell_height=81
cky = cky_parser("Time flies like an arrow", grammar_rules(file_grammar), lexicon_dictionary)

# %% cell_id="87e8a97b8027467fb7699e2e22524364" tags=[] deepnote_to_be_reexecuted=false source_hash="c5170a03" execution_start=1658943427032 execution_millis=10 deepnote_cell_type="code" deepnote_cell_height=620 deepnote_output_heights=[252]
import numpy as np
import pandas as pd

# pares de puntos de la matriz
dic_to_df = dict()
for i in range(0,5):
    list = []
    for j in range(0,5-i):
        #print((i,j+i+1),":",cky[(i,j+i+1)])
        list.append(cky[(i,j+i+1)])
        dic_to_df[str(i)] = list

N=5
df = pd.DataFrame(columns = [i for i in range(0,N)], 
                   index = [i for i in range(1,N+1)])

df[0] = dic_to_df['0']
print(df)

#for i in range(0,5):
#    df[i] = dic_to_df[str(i)]

# %% [markdown] cell_id="bd5ca5e02b04420d839dbd040f6b0efe" tags=[] owner_user_id="41b68b99-1317-46a8-8d9f-507b7d8fe1ab" deepnote_cell_type="markdown" deepnote_cell_height=625
# # Cuestionario
#
# 1. ¿Es correcto el análisis sintáctico que se ha obtenido? Justifica la respuesta.
#
#     HOLA
#
# 2. ¿Cuáles son las limitaciones de aplicar el algoritmo CKY probabilístico para realizar el análisis sintáctico? Justifica la respuesta.
#
#     HOLA
#
# 3. ¿Qué posibles mejoras que se podrían aplicar para mejorar el rendimiento del análisis sintáctico? Justifica la respuesta.
#
#     HOLA

# %% [markdown] tags=[] created_in_deepnote_cell=true deepnote_cell_type="markdown"
# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=16bbac0e-c0cf-475a-9977-7067c93e2eaf' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>
