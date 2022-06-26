class Palabra:
    '''
    Clase para guardar el token y la etiqueta de una palabra de un corpus
    '''

    def __init__(self, token: str, tag: str):
        '''
        Constructor de la clase

        token : str
            Token de la palabra

        tag : str
            Etiqueta de la palabra
        '''
        self._token = token
        self._tag = tag

    def Token(self):
        '''
        Método para acceder al token de la palabra
        '''
        return self._token

    def Tag(self):
        '''
        Método par acceder a la etiqueta de la palabra
        '''
        return self._tag

archivo = open('ds/Corpus-tagged.txt', "r")

corpus = list()
oracion_actual = list()

for entrada in archivo.readlines():
    entrada = entrada.split()
    if len(entrada) == 0:
        # Puede ser la primera oración del documento
        # O que termina la oración
        if len(oracion_actual) > 0:
            # Fin de la oración
            corpus.append(oracion_actual)
        oracion_actual = list()
        continue

    elif entrada[0] == '<doc':
        # Inicio de documento. No se hace nada
        continue

    elif entrada[0] == '</doc>':
        # Fin del documento. No se hace nada
        continue
  
    oracion_actual.append(Palabra(token=entrada[0], tag=entrada[2]))

archivo.close()
import pandas as pd

class HMMBigrama:
    '''
    Clase para obtener las matrices de probabilidad HMM Bigrama a partir de un corpus
    '''

    def __init__(self, corpus: [[Palabra]]):
        '''
        Constructor de la clase para calcular el Modelo Oculto de Markov Bigrama
        '''
        self._corpus = corpus
        self._estados = dict()
        self._tokens = dict()
        self._q0 = 'q0'
        self._qF = 'qF'

        self._prob_trans = pd.DataFrame()
        self._prob_obs = pd.DataFrame()

    def Corpus(self):
        return self._corpus.copy()

    def EstadoInicial(self):
        return self._q0

    def EstadoFinal(self):
        return self._qF

    def _ProcesarCorpus(self):
        '''
        Método para contar el número de ocurrencias de estados y tokens
        '''
        for oracion in self._corpus:
            for palabra in oracion:
                            
                # Se recorren todas las palabras de todas las oraciones del corpus recuperando las etiquetas (estados)
                estado = palabra.Tag()
                estados = self._estados
                estados[estado] = estados[estado] + 1 if estado in estados else 1

                # Se recorren todas las palabras de todas las oraciones del corpus recuperando los tokens
                token = palabra.Token()
                tokens = self._tokens
                tokens[token] = tokens[token] + 1 if token in tokens else 1
                

    def Estados(self, incluir_inicial: bool = False, incluir_final: bool = False):
        '''
        Devuelve los estados del bigrama en base al corpus proporcionado al constructor

        incluir_inicial : bool (False)
            Flag para indicar si se quiere recuperar el estado inicial

        incluir_final : bool (False)
            Flag para indicar si se quiere recuperar el estado final

        return
            Diccionario de estados con el número de ocurrencias de cada estado en el corpus
        '''

        if len(self._estados) == 0:
            self._ProcesarCorpus()

        copia_estados = dict()
        if incluir_inicial:
            # Hay tantos estados como oraciones en el corpus
            copia_estados[self._q0] = len(self._corpus)

        copia_estados.update(self._estados)

        if incluir_final:
            # Hay tantos estados como oraciones en el corpus
            copia_estados[self._qF] = len(self._corpus)

        return copia_estados

    def Tokens(self):
        '''
        Devuelve los tokens del bigrama en base al corpus proporcionado al constructor

        return
            Diccionario de tokens con el número de ocurrencias de cada token en el corpus
        '''

        if len(self._tokens) == 0:
            self._ProcesarCorpus()

        return self._tokens.copy()

    def ProbabilidadesDeTransicion(self):
        '''
        Método para calcular las probabilidades de transición bigrama
        a partir del corpus proporcionado a la clase
        '''

        # Si ya se ha calculado se devuelve
        if len(self._prob_trans) != 0:
            return self._prob_trans.copy()

        '''
        En esta parte del código se calcula el número de
        transiciones bigrama, es decir, en el diccionario
        'contador_transiciones' se almacenarán los contadores
        de las transiciones t-1 -> t

        Las claves del diccionario serán los estados de partida
        mientras que los valores de cada clave serán los estados
        de destino y el número de veces que transitan a cada estado
        '''
        q0 = self._q0
        qF = self._qF
        contador_transiciones = {q0: dict()}

        for oracion in self._corpus:
            # Contador de transición q0 a estado q1
            q1 = oracion[0].Tag()
            if q1 not in contador_transiciones[q0]:
                contador_transiciones[q0][q1] = 0
            contador_transiciones[q0][q1] += 1

            # Contador de transiciones entre palabras de la oración
            for it in range(0, len(oracion) - 1):                
                qt_1 = oracion[it].Tag()
                qt = oracion[it+1].Tag()
                if qt_1 not in contador_transiciones:
                    contador_transiciones[qt_1] = dict()
                if qt not in contador_transiciones[qt_1]:
                    contador_transiciones[qt_1][qt] = 0
                contador_transiciones[qt_1][qt] += 1

            # Contador de transición qF_1 a qF
            qF_1 = oracion[-1].Tag()

            if qF_1 not in contador_transiciones:
                contador_transiciones[qF_1] = dict()
            if qF not in contador_transiciones[qF_1]:
                contador_transiciones[qF_1][qF] = 0

            contador_transiciones[qF_1][qF] += 1
            
        '''
        Cálculo de la tabla de probabilidades de transición.

        Se calculan ahora las probabilidades de transición
        siguiendo la relación: P(T|T-1) = C(T-1, T) / C(T-1).

        En 'contador_transiciones' se han acumulado la coincidencias C(T-1, T)
        y en 'estados' se tiene disponible C(T-1) por lo que es posible
        calcular la tabla de probabilidades de transiciones con estos elementos.
        '''
        tags_estados_iniciales = list(
            self.Estados(incluir_inicial=True).keys())
        tags_estados_finales = list(self.Estados(incluir_final=True).keys())
        estados_totales = self.Estados(
            incluir_inicial=True, incluir_final=True)

        prob_trans = {qt_1: {qt: 0 for qt in tags_estados_finales}
                      for qt_1 in tags_estados_iniciales}
        for qt_1 in tags_estados_iniciales:
            for qt in tags_estados_finales:
                prob = 0
                if qt_1 in contador_transiciones and qt in contador_transiciones[qt_1]:
                    cti_1_ti = contador_transiciones[qt_1][qt]
                    cti_1 = estados_totales[qt_1]
                    prob = cti_1_ti / cti_1
                    
                prob_trans[qt_1][qt] = prob

        self._prob_trans = pd.DataFrame.from_dict(prob_trans, orient='index')

        return self._prob_trans.copy()

    def ProbabilidadesDeEmision(self):
        '''
        Método para calcular las probabilidades de emisión
        a partir del corpus proporcionado a la clase
        '''

        if len(self._prob_obs) != 0:
            return self._prob_obs.copy()

        '''
        En esta parte del código se calculan el número de
        ocurrencias de la palabra Wi para la etiqueta Ti  
        '''
        estados = self.Estados()
        contador_observaciones = {key: dict() for key in estados.keys()}

        for oracion in self._corpus:
            for palabra in oracion:
                token = palabra.Token()
                etiqueta = palabra.Tag()
                if token not in contador_observaciones[etiqueta]:
                    contador_observaciones[etiqueta][token] = 0
                contador_observaciones[etiqueta][token] += 1

        '''
        Cálculo de la tabla de probabilidades de emisión.

        Se calculan ahora las probabilidades de emisión
        siguiendo la relación: P(Wi|Ti) = C(Ti,Wi) / C(Ti).

        En 'contador_observaciones' se han acumulado la coincidencias C(Ti, Wi)
        y en 'estados' se tiene disponible C(Ti) por lo que es posible
        calcular la tabla de probabilidad de emisión con estos elementos.
        '''
        tokens = self.Tokens()
        prob_obs = {Ti: {Wi: 0 for Wi in tokens} for Ti in estados}
        for Ti in estados:
            for Wi in tokens:
                prob = 0
                if Ti in contador_observaciones and Wi in contador_observaciones[Ti]:
                    cti_wi = contador_observaciones[Ti][Wi]
                    cti = estados[Ti]
                    prob = cti_wi / cti
                prob_obs[Ti][Wi] = prob

        self._prob_obs = pd.DataFrame.from_dict(prob_obs, orient='index')

        return self._prob_obs

hmmbigrama = HMMBigrama(corpus)
hmmbigrama.Tokens()
len(hmmbigrama.Tokens())
hmmbigrama.Estados()
len(hmmbigrama.Estados())

def non_zero_green(val):
    '''
    Función para resaltar en verde las probabilidades que no sean 0
    '''
    return 'background-color: Aquamarine' if val > 0 else ''
prob_transicion = hmmbigrama.ProbabilidadesDeTransicion()
prob_transicion.style.applymap(non_zero_green)

prob_emision = hmmbigrama.ProbabilidadesDeEmision()
prob_emision.style.applymap(non_zero_green)

class Viterbi:
    '''
    Algoritmo de Viterbi para obtener las mejores
    etiquetas de las palabras de una oración
    '''

    def __init__(self, hmmbigrama: HMMBigrama, oracion: str):
        self._hmmbigrama = hmmbigrama
        self._oracion = oracion

        self._estados_relevantes = None
        self._prob_viterbi = pd.DataFrame()
        self._estado_max_anterior = None

    def _CalculoEstadosRelevantes(self):
        self._estados_relevantes = set()
        for palabra_analizar in [x.lower() for x in self._oracion.split()]:
            # Búsqueda de estados
            for oracion in self._hmmbigrama.Corpus():
                for palabra_corpus in oracion:
                    if palabra_corpus.Token() == palabra_analizar:
                        self._estados_relevantes.add(palabra_corpus.Tag())
    def Probabilidades(self):
        if len(self._prob_viterbi) != 0:
            return self._prob_viterbi.copy()

        if not self._estados_relevantes:
            self._CalculoEstadosRelevantes()

        estados_relevantes = self._estados_relevantes

        '''
        Matriz en la que se guardan los valores de Viterbi
        '''
        matriz_viterbi = {q: dict() for q in estados_relevantes}

        '''
        Matriz asociada a la matriz de Viterbi en la que se almacena
        el estado de origen que maximiza cada probabilidad
        '''
        self._estado_max_anterior = {q: dict() for q in estados_relevantes}

        q0 = self._hmmbigrama.EstadoInicial()
        prob_trans = self._hmmbigrama.ProbabilidadesDeTransicion()
        prob_obs = self._hmmbigrama.ProbabilidadesDeEmision()

        token_anterior = None
        for token in [x.lower() for x in self._oracion.split()]:
            for qDestino in estados_relevantes:

                prob_max = 0
                if not token_anterior:
                    # Estado q0
                    prob_max = prob_trans[qDestino][q0]
                else:
                    # Resto de estados
                    for qOrigen in estados_relevantes:
                        ####
                        prob_qOrigen = prob_trans[qDestino][qOrigen]
                        ####
                        if prob_qOrigen > prob_max:
                            ####
                            prob_max = prob_qOrigen
                            #  TODO: usar _estado_max_anterior
                            self._estado_max_anterior[qDestino][token] = prob_max
                            ####

                matriz_viterbi[qDestino][token] = prob_max * prob_obs[token][qDestino]

            token_anterior = token

        self._prob_viterbi = pd.DataFrame.from_dict(matriz_viterbi, orient='index')

        return self._prob_viterbi.copy()

    def DecodificacionSecuenciaOptima(self):
        # Decodificación de la secuencia óptima
        oracion_invertida = [x.lower() for x in self._oracion.split()]
        oracion_invertida.reverse()

        prob_viterbi = self.Probabilidades()

        oracion_etiquetada = []
        # Se busca la probablidad máxima de Viterbi asociada a la última palabra de la oración
        palabra = oracion_invertida[0]
        etiqueta = prob_viterbi[palabra].idxmax()
        oracion_etiquetada.append({'token': palabra, 'tag': etiqueta, 'prob': prob_viterbi[palabra].max()})

        # Ahora se usa la tabla auxiliar de Viterbi que contiene
        # el estado de origen que maximiza cada probabilidad Viterbi
        palabra_anterior = palabra
        for palabra in oracion_invertida[1:]:
            ####
            #  TODO: usar la matriz auxiliar
            etiqueta = prob_viterbi[palabra].idxmax()
            oracion_etiquetada.append({'token': palabra, 'tag': etiqueta, 'prob': prob_viterbi[palabra].max()})
            ####

        # Se recupera el orden de la oración con las palabras ya etiquetadas
        oracion_etiquetada.reverse()

        return oracion_etiquetada

viterbi = Viterbi(hmmbigrama=hmmbigrama, oracion='Habla con el enfermo grave de trasplantes .')
matriz_prob_viterbi = viterbi.Probabilidades()
matriz_prob_viterbi.style.applymap(non_zero_green)
matriz_prob_viterbi.to_excel('out/mia07_t3_tra_resultados_viterbi.xlsx', sheet_name='viterbi')
oracion_etiquetada = viterbi.DecodificacionSecuenciaOptima()
oracion_etiquetada
