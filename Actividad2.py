# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] cell_id="15d8ffcd-81b4-434b-8b02-99d3456d595e" deepnote_cell_height=306 deepnote_cell_type="markdown" tags=[]
# # Implementación del algoritmo PCKY
# ## Librerías a utilizar
#
# Para la implementación del algoritmo CKY solo serán necesarias tres paquetes adicionales, el primero permite seleccionar un elemento de una lista a partir del índice, el segundo mostrará de manera más clara los resultados de los árboles y finalmente, pandas que permitirá mostrar la matriz CKY en forma tabular, como un dataframe. 

# %% cell_id="00001-04f871f0-1572-401b-8d1d-d36cdeaa78e2" deepnote_cell_height=112 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=24 execution_start=1659331205499 source_hash="88920eeb" tags=[]
from operator import itemgetter
from pprint import pprint
import pandas as pd

# %% [markdown] cell_id="00002-3d94ab7b-78a5-4716-a632-dcdd11834ae6" deepnote_cell_height=161 deepnote_cell_type="markdown" tags=[]
# ## Datos de entrada
#
# La variable `grammar_file` que aparece a continuación emula las reglas gramaticales escritas en un archivo de texto. En este caso se han escrito las reglas propias del ejercicio.

# %% cell_id="4b1badc35931404891b478a90e85557c" deepnote_cell_height=94 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=1 execution_start=1659331205523 source_hash="679d7507" tags=[]
file = open("ds/grammar.txt",'r')
grammar_file = file.read()


# %% [markdown] cell_id="00008-4a82bc4f-3999-4caa-9fd1-df51d0e3fdc2" deepnote_cell_height=283 deepnote_cell_type="markdown" tags=[]
# La función `read_rules()` recibe como argumento un texto con reglas gramaticales y probabilidades para convierlas en tres diccionarios que permiten buscar los datos necesarios para completar el algoritmo CKY y PCKY.
#
# Se crea el lexicón, de forma común, en lingüística se dice que un elemento del lexicón en la entrada de un diccionario, entonces se define como tal en el código.
#
# Se expresan las reglas gramaticales y lexicas en forma de tuplas como claves de una probabilidad que se usará para obtener las probabilidades de cada árbol obtenido por el algoritmo. Se eligen tuplas porque son fáciles de manejar, similar a los lenguajes Lisp.

# %% cell_id="a9ac5bfaa52d4a9db71a9d99aad0ec87" deepnote_cell_height=963 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=0 execution_start=1659331205524 source_hash="63b2155f" tags=[]
def read_rules(grammar_file):
    '''
    This function read grammar rules writen in a text variable or a file.

    The text file contain grammar rules and probabilities writen like:

    S -> NP VP 0.800

    In grammar rules dictionary, parents indexed by children, like this:

    {('Det', 'Nominal'): ['NP'],
     ('NP', 'VP'): ['S'],
     ('Verb', 'PP'): ['VP']}

        Parameters:
            grammar_file (str): Text with grammar rules
                                                                  
        Returns:
            grammar_rules (dict): Dictionary with the rules indexed by children
            lexicon_rules (dict): Dictionary with terminal simbols
            probabilities (dict): Dictionary with grammar and lexical rules asociated to it's probability
    '''    
    gr_temp_rules = list()
    lexicon_rules = dict()
    probabilities = dict()
    grammar_rules = dict()
    for line in grammar_file.strip().split("\n"):
        parent, children = line.strip().split("->")
        parent = parent.strip()
        children = children.split()
        # Lee las reglas lexicas
        if len(children) == 2:
            if parent not in lexicon_rules:
                lexicon_rules[parent] = set()
            lexicon_rules[parent].add(children[0])
            probabilities[parent,children[0]] = float(children[1])
        # Lee las reglas gramaticales
        else:
            # Crea la regla (parent, (c1, c2)) como en lisp ;)
            rule = (parent, tuple(children[:2]))
            probabilities[rule] = float(children[2])
            gr_temp_rules.append(rule)
    # Crear un diccionario con las reglas invertidas, eso permite buscar al nodo padre
    for (parent, (lc, rc)) in gr_temp_rules:
        # Si no existe la entrada, se crea
        if (lc, rc) not in grammar_rules:
            grammar_rules[lc, rc] = list()
        # Se agrega el caso
        grammar_rules[lc,rc].append(parent)
    return grammar_rules,lexicon_rules,probabilities


# %% [markdown] cell_id="00010-454a2d17-cb63-4123-a1f2-de7e96faa8ac" deepnote_cell_height=236 deepnote_cell_type="markdown" tags=[]
# ## Algoritmos CKY y PCKY
#
# Ahora se implementa el algoritmo CKY, mismo que recibe como entrada una oración en forma de cadena de texto, un diccionario con reglas gramaticales y un lexicón adecuado a la gramática. Opcionalmente, se puede definir el argumento de entrada `verbose` al valor `True`, de esta manera se mostrará en pantalla cada uno de los pasos que sigue el algoritmo para crear la matriz correspondiente. Esta matriz también tendrá forma de diccionario.

# %% cell_id="00011-592afc16-9dd0-4778-82ab-5445e7397ec7" deepnote_cell_height=1395 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=2 execution_start=1659331205531 output_cleared=false source_hash="b9f8d6db" tags=[]
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
            matrix_cky[(ordinate, abscissa)] = list()
            if verbose:
                print("1: abscissa=",abscissa,"ordinate=",ordinate,"a-o=",abscissa-ordinate)
            # Si se opera sobre la diagonal
            if(abscissa-ordinate == 1):
                # Combina la palabra con las categorías del lexicón
                for key in lexicon:
                    if verbose:
                        print("2: key=",key,"word=",words[ordinate])
                    # Si la combinación existe en el lexicón se agrega a la matriz
                    if(words[ordinate] in lexicon[key]):
                        matrix_cky[(ordinate,abscissa)].append(
                            (key,0,words[ordinate],words[ordinate]))
                        if verbose:
                            print("2:",matrix_cky)
            # Si hay que operar sobre dos celdas
            elif(abscissa-ordinate > 1):
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


# %% [markdown] cell_id="00012-13b1464e-647a-4f01-90b5-d3d9af9e9250" deepnote_cell_height=130 deepnote_cell_type="markdown" tags=[]
# Enseguida se crean dos funciones, la primera, `get_prob()`, se usará para obtener las probabilidades del diccionario de probabilidades, la segunda, `update_prob()`, se usará para actualizar las probabilidades desde los nodos intermedios hasta el nodo padre. 

# %% cell_id="00013-ce58d7ee-aaf1-4692-8ab2-8951c865871f" deepnote_cell_height=549 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=0 execution_start=1659331205559 output_cleared=true source_hash="bd748518" tags=[]
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

def update_prob(left, down, actual, prob_dict):
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
    actual_prob = get_prob((actual,(left[0],down[0])),prob_dict)
    prob = left[4]*down[4]*actual_prob
    return prob


# %% [markdown] cell_id="00014-9c29e742-1452-4504-b54b-223bee2c9175" deepnote_cell_height=80 deepnote_cell_type="markdown" tags=[]
# Se actualiza `cky_parser()`. Ahora `pcky_parser()` agregará la información de la probabilidad a cada lista agregada a `matrix_pcky`.

# %% allow_embed=false cell_id="00015-c0276255-8ae0-4c37-b6a4-d157b82bb24f" deepnote_cell_height=1467 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=1 execution_start=1659331205559 output_cleared=false source_hash="daecb7ed" tags=[]
def pcky_parser(sentence, grammar, lexicon, probabilities_table, verbose=False):
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
        for abscissa in range(i+1,len(words)+1):
            # Se agrega una celda
            matrix_pcky[(ordinate, abscissa)] = list()
            if verbose:
                print("1: abscissa=",abscissa,"ordinate=",ordinate,"a-o=",abscissa-ordinate)
            # Si se opera sobre la diagonal
            if(abscissa-ordinate == 1):
                # Combina la palabra con las categorías del lexicón
                for key in lexicon:
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
            elif(abscissa-ordinate > 1):
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


# %% [markdown] cell_id="00016-e35a2821-10f4-47d3-81a7-38a7e618b838" deepnote_cell_height=161 deepnote_cell_type="markdown" tags=[]
# ## Obtención de resultados
#
# La función `tree()` recorre una matriz generada por el algoritmo CKY en busca de árboles a partir del valor de un nodo en particular, tomando en cuenta una ruta a través de un índice creado por el algoritmo. 

# %% cell_id="00017-dbb37431-292e-490c-9eb5-ea0666dca1ef" deepnote_cell_height=1467 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=8 execution_start=1659331205564 output_cleared=false source_hash="30a3a67a" tags=[]
def tree (matrix, cell, parent="S", index=0, pcky=False):
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
                return [(matrix[cell][index][0],matrix[cell][index][4]),
                         matrix[cell][index][2]]
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
                tree(matrix,
                     (cell[0],matrix[cell][index][1]),
                     matrix[cell][index][2],pcky=True))
        else:
            child.append(
                tree(matrix,
                     (cell[0],matrix[cell][index][1]),
                     matrix[cell][index][2]))
        # Hijo izquierdo
        if pcky:
            child.append(
                tree(matrix,
                     (matrix[cell][index][1],cell[1]),
                     matrix[cell][index][3],pcky=True))
        else:
            child.append(
                tree(matrix,
                     (matrix[cell][index][1],cell[1]),
                     matrix[cell][index][3]))
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


# %% [markdown] cell_id="00018-f0c1a222-4e1c-447e-86a1-2fa41e3f73e3" deepnote_cell_height=80 deepnote_cell_type="markdown" tags=[]
# La función `find_solutions()` servirá como _frontend_ para todas las funciones anteriores, brindará la respuesta propuesta por el algoritmo.

# %% cell_id="00019-c4f8c998-7cc9-4048-92b2-88e1e0692315" deepnote_cell_height=819 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=3 execution_start=1659331205580 source_hash="87db1a70" tags=[]
def find_solutions(sentence, grammar, lexicon, axiom, probabilities_table={}, verbose=False):
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
            df (dataframe): Data frame with the CKY matrix, useful for printing
    '''
    N = len(sentence.split())
    solutions = list()
    if probabilities_table:
        matrix = pcky_parser(sentence,grammar,lexicon,probabilities_table,verbose)
        candidates = list()
        # Busca en (0,N) aquellas listas que contengan el axioma
        for i in enumerate(matrix[(0,N)]):
            if i[1][0] == axiom:
                # En candidates se guarda el índice y la probabilidad
                candidates.append([i[0],i[1][4]])
        # Selecciona aquel con mayor probabilidad
        candidates = max(candidates,key=itemgetter(1))
        solutions = tree(matrix,(0,N),index=candidates[0],pcky=True)
    else:
        matrix = cky_parser(sentence,grammar,lexicon,verbose)
        for i in enumerate(matrix[(0,N)]):
            if i[1][0] == axiom:
                solutions.append(tree(matrix,(0,N),index=i[0]))
    # Crea un dataframe, útil para ver la matriz
    df = pd.DataFrame(columns = [i for i in range(0,N)],
                        index = [i for i in range(1,N+1)])
    for i in range(0,5):
        for j in range(0,5-i):
            df.loc[j+i+1,i] = matrix[(i,j+i+1)]
    df = df.transpose()
    return solutions, df


# %% cell_id="fd1ca87ae0f2471ba95b384b98214b71" deepnote_cell_height=81 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=4 execution_start=1659331205586 source_hash="51234cde" tags=[]
grammar_rules, lexicon_rules, probabilities = read_rules(grammar_file)

# %% cell_id="00020-fb337946-e035-4086-8bea-6bec16c7fa1d" deepnote_cell_height=769 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=360 execution_start=1659331205593 source_hash="ab24d0bb" tags=[]
options, matrix = find_solutions("Time flies like an arrow",
                        grammar_rules,lexicon_rules,"S")
pprint(options)
matrix

# %% allow_embed=false cell_id="00021-501b4cbe-d222-4717-b18e-ad7c786a33f7" deepnote_cell_height=714 deepnote_cell_type="code" deepnote_to_be_reexecuted=false execution_millis=261 execution_start=1659331205699 source_hash="c181e2ad" tags=[]
options, matrix = find_solutions("Time flies like an arrow",
                        grammar_rules,lexicon_rules,"S",probabilities)
pprint(options)
matrix

# %% [markdown] cell_id="00026-29024627-2f74-40b8-98a0-53cec4e26fcc" deepnote_cell_height=2883 deepnote_cell_type="markdown" owner_user_id="41b68b99-1317-46a8-8d9f-507b7d8fe1ab" tags=[]
# ## Cuestionario
#
# 1. ¿Es correcto el análisis sintáctico que se ha obtenido? Justifica la respuesta.
#
# Sí. Basado en la gramática proporcionada el resultado es satisfactorio y se muestra a continuación.
#
# \usepackage{tikz}
# \usepackage{tikz-qtree}
# \begin{figure}[!ht]
#     \centering
#         \Tree [.S~(9.600000000000002e-13)
#                 [.NP~(0.002) time ]
#                 [.VP 
#                     [.Verb~(0.02) flies ]
#                     [.PP~(1.5000000000000002e-07) 
#                         [.Preposition~(0.05) like ]
#                         [.NP~(3e-05) 
#                             [.Det~(0.05) an ]
#                             [.Nominal~(0.002) arrow ] ] ] ] ]
# \caption{Árbol sintáctico proporcionado por el algoritmo PCKY}
# \end{figure}
#
# 2. ¿Cuáles son las limitaciones de aplicar el algoritmo CKY probabilístico para realizar el análisis sintáctico? Justifica la respuesta.
#
# Los problemas se presentan debido a la información guardada en la gramática, si ésta no tiene un elemento particular necesario para el análisis, proporcionará resultados truncos.
#
# Por supuesto, las probabilidades de aparición de la gramática podrían llevar a resultados dudosos, incluso cuando su objetivo es el contrario, pero estas probabilidades siempre dependerán del corpus de origen, que puede ser distinto al de la oración a analizar, ya sea en registro, en dialecto, etc.
#
# En el caso particular de este ejercicio, el hecho de tener algunos símbolos intermedios creados para llegar a la forma normal de Chomsky permite que el algoritmo genere posibles soluciones impensables para el análisis linguístico. El algoritmo CKY propone dos soluciones y el PCKY seleccionó el correcto, pero si se examina la opción desechada se puede observar:
#
#     ['NP', [['Nominal', 'time'], ['Nominal', 'flies']]]
#
# Lo cual es un elemento impensable pues sugiere que una frase nomimal puede tener dos núcleos. Este análisis va en contra del principio de endocentrismo que establece, como su nombre indica, que cada frase tiene un núcleo que determina el tipo de la frase.
#
# Finalmente, el algoritmo que usa este tipo de gramáticas, arrastra la misma gran crítica que los lingǘistas hacen a la teoría de Chomsky: No es capaz de analizar lenguas aglutinantes. 
#
# 3. ¿Qué posibles mejoras que se podrían aplicar para mejorar el rendimiento del análisis sintáctico? Justifica la respuesta.
#
# El algoritmo se basa en el uso de cualquier gramática en forma normal de Chomsky, esto es porque computacionalmente es posible generar automáticamente generadas mediante corpus de análisis, sin embargo, el programa minimalista de Chomsky sugiere la teoría X-barra que tiene su principio en los estudios de Ray Jackendoff. Esta teoría proporciona la posibilidad de crear gramáticas consistentes siempre en la forma normal de Chomsky. Dejar de ignorar el conocimiento linguístico proporcionaría mejores gramáticas para la IA.
#
# Por otra parte, analizar solo las probabilidades de los subárboles que llevan a una propuesta de solución aumentaría el rendimiento a nivel de cómputo.
#
#  

# %% [markdown] created_in_deepnote_cell=true deepnote_cell_type="markdown" tags=[]
# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=16bbac0e-c0cf-475a-9977-7067c93e2eaf' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>
