Texto = {
    "WarnDifVecSize": "Las dimensiones de los vectores son diferentes.",
    "WarnDifBaseSize": "La dimensión de la base y los vectores es diferente.",
    "WarnDifBaseDim": "La dimensión de un elemento de la base no es correcta.",
    "WarnBaseNotInd": "La base no es linealmente dependiente.",
    "WarnNotSquared": "La matriz de coeficientes no es cuadrada. " +
                        "Por lo tanto el sistema no es resoluble.",
    "WarnDifMatrixSize": "La dimensión de las matrices no coinciden.",
    'WarnNotMatrix' : "La lista dada no es una matriz válida."
    }

# Valor de pi
pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679

#Creador de máximo común divisor
def mcd(a, b):  # Máximo común divisor con dos entradas: a y b

    # en caso de que ambos números sean iguales, el mcd es él mismo.
    if b == a:
        return a

    # búsqueda de divisores comunes.
    while b:
        a, b = b, a % b
    return a

# Convertidor de número a cadena de superíndice
def superindice(numero):
    # Diccionario de correspondencia entre dígitos y superíndices
    superindices = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵',
                    '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻'}

    # Convierte cada dígito a su superíndice correspondiente
    superindice_str = ''.join(superindices[digito] for digito in str(numero))

    return superindice_str

def comprobarDimensiones(a,b):
    #Comprueba que las dimensiones de un sistema de ecuaciones sea el correcto
    if len(a) != len(a[0]):
        raise Exception(Texto["WarnNotSquared"])
    if len(a) != len(b):
        raise Exception(Texto["WarnDifMatrixSize"])
    else:
        return True

def sistemaEcuaciones(a,b):
    comprobarDimensiones(a, b)
    
    n = len(a)
    x = vector([0] * n)
    

    # Eliminación Gaussiana
    for i in range(n):
        if a[i][i] == 0.0:
            return None  # El sistema no tiene solución única

        for j in range(i + 1, n):
            ratio = a[j][i] / a[i][i]

            for k in range(n):
                a[j][k] = a[j][k] - ratio * a[i][k]
                
            b[j] = b[j] - ratio * b[i]

    # Sustitución hacia atrás
    x[n - 1] = b[n - 1] / a[n - 1][n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] = x[i] - a[i][j] * x[j]
        x[i] = x[i] / a[i][i]

    return x
    
def baseCanonica(n):
    #creación de lista vacía dónde se almacenará la base canónica
    e = []
    #Creación de la báse canónica
    for i in range (0,n):
        e += [[]]
        for j in range (0,n):
            if i == j:
                e[i] += [1]
            else:
                e[i] += [0]
                
    return matriz(e)

def deltaKronecker(i,j):
    if i == j:
        return 1 
    else:
        return 0

def comprobarBase(e, n):
    # Revisar si la base tiene la misma dimensión de los vectores
    if len(e) != n:
        raise Exception(Texto["WarnDifBaseSize"])
    else:
        # Revisar la dimensión de cada elemento de la base
        for i in range(n):
            if len(e[i]) != n:
                raise Exception(Texto["WarnDifBaseDim"])

    # Copiar la base en una matriz para la eliminación gaussiana
    matriz = [e[i][:] for i in range(n)]

    # Eliminación Gaussiana
    for columna in range(n):
        # Hacer cero los elementos debajo del pivote
        for fila in range(columna + 1, n):
            if matriz[columna][columna] == 0:
                raise Exception(Texto["WarnBaseNotInd"])
            coeficiente = matriz[fila][columna] / matriz[columna][columna]
            for j in range(columna, n):
                matriz[fila][j] -= coeficiente * matriz[columna][j]

    # Verificar si algún pivote es cero
    for i in range(n):
        if all(valor == 0 for valor in matriz[i][:n]):
            raise Exception(Texto["WarnBaseNotInd"])

    return e
     
def determinarCoeficientes(v,e = 0):
    n = len(v)
    
    if e == 0:
        e = baseCanonica(n)
    else:
        comprobarBase(e, n)
    
    coeficientes = sistemaEcuaciones(e, v) 
    
    return coeficientes  

class racional:
    # ---------------- DEFINICIÓN DEL TIPO --------------
    def __init__(self, numerador, denominador=1, presicion=5, simp=False, potenciapi=0):
        # Asignación de un nombre de tipo (hoy interno)
        self.type = 'racional'

        # ----------------- SECCIÓN DE ADVERTENCIAS --------------------
        # Mensajes de advertencia
        self.advertencia = {'size': "Advertencia: el tamaño del número es muy grande y podría fallar",
                            'type': "El tipo de un valor proporcionado no es compatible. Sólo recibe entero o flotante.",
                            'nulldenom': "El denominador no puede ser igual a 0. División entre cero.",
                            'floatval': "Advertencia: algún valor es flotante. Esto podría causar errores de presición",
                            'difpi': 'El valor de las potencias de pi no son iguales, por lo que se perderá presición.'}

        # Excepción mostrada por si el denominador es igual a 0
        if denominador == 0:
            raise Exception(self.advertencia['nulldenom'])

        # Advertencia mostrada por si el tamaño de la presición es muy grande
        if presicion > 15:
            print(self.advertencia['size'])

        # ------------------- ASIGNACIÓN POR TIPOS ----------------------

        # Conversión de un número flotante a un número racional con la presición dada
        if isinstance(numerador, float) or isinstance(denominador, float):
            # Advertencia por existencia de flotante
            print(self.advertencia['floatval'])

            # Asignación del denominador a la potencia de 10 de la presición
            self.denominador = (10 ** presicion)
            # Asignación del numerador redondeado según la presición (multiplicación por 1)
            self.numerador = round(numerador * self.denominador / denominador)

        # Conversión de un número con ambos coeficientes enteros
        elif isinstance(numerador, int) and isinstance(denominador, int):
            self.denominador = denominador
            self.numerador = numerador

        # Error de tipo, ni entero ni flotante
        else:
            raise Exception(self.advertencia['type'])

        # Almacenamiento de la potencia de pi
        self.potenciapi = potenciapi

        # DEBUG ONLY
        self.floatvalue = self.float()

        # simplifica cualquier otro valor
        if simp != True:
            self.simplificar()

    # ----------------- DEFINICIÓN DE OPERACIONES ---------------------
    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = racional(other)

        # En caso de que las potencias de pi sean iguales
        if self.potenciapi == other.potenciapi:
            numerador = (self.numerador * other.denominador) + (other.numerador * self.denominador)
            denominador = self.denominador * other.denominador
            potenciapi = self.potenciapi

        # El caso en el que la potencia de pi del primero sea mayor que el segundo
        elif self.potenciapi > other.potenciapi:
            # Impresión de advertencia por pérdida de presición
            print(self.advertencia['difpi'])
            # Factorización de la potencia de pi más pequeña
            potenciapi = other.potenciapi
            numerador = (self.numerador * other.denominador * pi**(self.potenciapi - other.potenciapi)) + (
                        other.numerador * self.denominador)
            denominador = self.denominador * other.denominador

        # El caso en el que la potencia de pi del primero sea menor que el segundo
        elif self.potenciapi < other.potenciapi:
            # Impresión de advertencia por pérdida de presición
            print(self.advertencia['difpi'])
            # Factorización de la potencia de pi más pequeña
            potenciapi = self.potenciapi
            numerador = (self.numerador * other.denominador) + (
                        other.numerador * self.denominador * pi**(other.potenciapi - self.potenciapi))
            denominador = self.denominador * other.denominador

        # Regresa siempre el mismo formato
        return racional(numerador, denominador, potenciapi=potenciapi)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = racional(other)

        # En caso de que las potencias de pi sean iguales
        if self.potenciapi == other.potenciapi:
            numerador = (self.numerador * other.denominador) - (other.numerador * self.denominador)
            denominador = self.denominador * other.denominador
            potenciapi = self.potenciapi

        # El caso en el que la potencia de pi del primero sea mayor que el segundo
        elif self.potenciapi > other.potenciapi:
            # Impresión de advertencia por pérdida de presición
            print(self.advertencia['difpi'])
            # Factorización de la potencia de pi más pequeña
            potenciapi = other.potenciapi
            numerador = (self.numerador * other.denominador * pi**(self.potenciapi - other.potenciapi)) - (
                        other.numerador * self.denominador)
            denominador = self.denominador * other.denominador

        # El caso en el que la potencia de pi del primero sea menor que el segundo
        elif self.potenciapi < other.potenciapi:
            # Impresión de advertencia por pérdida de presición
            print(self.advertencia['difpi'])
            # Factorización de la potencia de pi más pequeña
            potenciapi = self.potenciapi
            numerador = (self.numerador * other.denominador) - (
                        other.numerador * self.denominador * pi**(other.potenciapi - self.potenciapi))
            denominador = self.denominador * other.denominador

        # Regresa siempre el mismo formato
        return racional(numerador, denominador, potenciapi=potenciapi)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = racional(other)

        numerador = self.numerador * other.numerador
        denominador = self.denominador * other.denominador
        potenciapi = self.potenciapi + other.potenciapi

        return racional(numerador, denominador, potenciapi=potenciapi)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = racional(other)

        numerador = self.numerador * other.denominador
        denominador = self.denominador * other.numerador
        potenciapi = self.potenciapi - other.potenciapi

        return racional(numerador, denominador, potenciapi=potenciapi)

    # ----------------- FUNCIONES DE OPTIMIZACIÓN DE SISTEMA
    def __str__(self):
        text = str(self.numerador)

        if self.potenciapi != 0:
            text += "π" + superindice(self.potenciapi)

        text += "/" + str(self.denominador)  # Devuelve la cadena de fracción

        return text

    def __repr__(self):
        text = str(self.numerador)
    
        if self.potenciapi != 0:
            text += "π" + superindice(self.potenciapi)
    
        text += "/" + str(self.denominador)  # Solo devuelve la cadena de fracción
    
        return text

    # ------------------- DEFINICIÓN DE FUNCIONES -----------------
    def float(self):  # Función para devolver el valor e flotante de la división:
        valor = self.numerador * (pi**self.potenciapi) / self.denominador

        return valor

    def simplificar(self):  # Función para simplificar en cada instancia

        if self.numerador != self.denominador:
            # Encuentra el máximo común divisor para después dividirlo y que las partes sigan siendo enteras
            div = mcd(self.numerador, self.denominador)

            self.numerador = int(self.numerador / div)
            self.denominador = int(self.denominador / div)
        else:
            self.numerador = 1
            self.denominador = 1
            # en caso de que numerador y divisor sean el mismo, el resultado es 1

    def inv(self):  # Función para calcular la inversa del número
        return racional(self.denominador, self.numerador, simp=True)
    
def vector(v):
    n = len(v)
    
    #Genera la lista vacía del vector
    vector = []
    
    #Asigna un valor racional a cada elemento de la lista
    for i in range(0, n):
        #convierte el elemento a un racional
        elemento = racional(v[i])
        
        #añade el elemento convertido
        vector += [elemento]
        
    return vector

def matriz(a):
    n = len(a)
    m = len(a[0])
    
    #creación de la lista vacía
    matriz =[]
    
    for i in range(0,n):
        if len(a[i]) != m:
            raise Exception(Texto['WarnNotMatrix'])
    
        matriz += [vector(a[i])]
    
    return matriz

v1 = vector([4,5,2,3])

v2 = [5,3,1,2]

e = matriz([[1,5,3,0], [7,2,0,0], [3,5,1,3], [0,0,0,1]])


print(determinarCoeficientes(v1,e))
