"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP11B
Integrantes:
    - Jaime Tuesta de Simón
    - Ignacio Mascarell Agúndez

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict
import math
import random

class IncompatibleEquationError(Exception):
    pass

def es_primo(n:int)->bool:
    """ Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario

    Args:
        n (int): Entero
    
    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None
    
    Examples:
        es_primo(5)=True
        es_primo(4)=False

    Comentarios:
        Para favorecer la complejidad del algoritmo buscamos evitar todos los números. Para ello, ajustamos la búsqueda en 
        la medida de lo posible. Descartamos todos los números congruentes a 0,2,3 o 4 con mod 6. De esta manera nos quitamos los
        números divisibles entre 2 y 3. Ahora tenemos que comprobar los números congruentes a 1 y 5 con mod 6. Hemos reducido el número
        de comparaciones.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 6
    while i <= int(math.sqrt(n)) + 1:
        if n % (i + 1) == 0 or n % (i - 1) == 0:
            return False
        i += 6
    return True

def lista_primos(a,b)-> List[int]:
    """ Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)
    
    Returns:
        List[int]: lista ordenada de primos mayores o iguales que a y menores que b.

    Raises: None
    
    Examples:
        lista_primos(1,11)=[2,3,5,7]
        lista_primos(7,7)=[7]

    Comentarios:
        Caso especial: si a == b, se devuelve [a] cuando a es primo (y [] en caso contrario).
        Si la lista comienza en un término menor que 2, lo ajustamos, ya que 2 es el primer número primo. 
        Iteramos desde a hasta b con ayuda de la función es_primo(n).
    """
    lista_primos = []
    if a == b:
        # Caso especial lista_primos(a,a): se comprueba el propio a. Va antes del ajuste a 2
        # para que, por ejemplo, lista_primos(0,2) siga devolviendo [] y no [2]
        b += 1
    if a < 2:
        a = 2
    for i in range(a, b):
        if es_primo(i):
            lista_primos.append(i)
    return lista_primos

def factorizar(n:int)->Dict[int,int]:
    """ Recibe  un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
    correspondientes exponentes en la descomposición en producto de factores primos de n.
    Args:
        n (int): Entero que se desea factorizar.
    
    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples:
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}

    Comentarios:
        Buscamos reducir la complejidad temporal de nuestra función. Para ello, tras cerrar los casos bases aplicamos una serie de criterios.
        Comenzamos dividiendo todas las veces posibles entre 2 y 3 y actualizamos el diccionario. Después entramos en una rueda de 6k +- 1 para hallar el resto de
        divisores mayores que 2 y 3. El bucle termina cuando p^2 > n: si entonces queda un factor mayor que 1, ese factor es primo.
    """
    dict_fact = {}
    # Casos base
    if n in (0, 1, -1):
        return dict_fact
    n = abs(n)

    # Extraer 2
    exp = 0
    while n % 2 == 0:
        n //= 2
        exp += 1
    if exp != 0:
        dict_fact[2] = exp

    # Extraer 3
    exp = 0
    while n % 3 == 0:
        n //= 3
        exp += 1
    if exp != 0:
        dict_fact[3] = exp

    # Rueda 6k ± 1
    p = 5
    i = 2  # saltos de 2 y 4 para alternar entre 6k + 1 y 6k - 1
    while p * p <= n:
        exp = 0
        while n % p == 0:
            n //= p           
            exp += 1
        if exp != 0:
            dict_fact[p] = exp
        p += i
        if i == 2:
            i = 4
        else:
            i = 2

    # Primo residual
    if n > 1:
        dict_fact[n] = 1

    return dict_fact

def mcd(a:int,b:int)->int:
    """ Calcula el máximo común divisor de dos enteros a y b.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples:
        mcd(10,15)=5
    
    Comentarios:
        Comprobamos que los valores estén ordenados correctamente. Aplicamos el algoritmo de Euclides para hallar el mcd.
    
    """
    if a > b:
        # Queremos que b sea siempre mayor que a
        a, b = b, a
    a, b = abs(a), abs(b)   # Queremos también que ambos números sean positivos (no cambia el resultado)
    while b != 0:
        # Algoritmo de Euclides
        a, b = b, a % b
    return a

def bezout(n: int, m: int) -> tuple[int,int,int]:
    """Finds values that follow Bezout's identity with Lehmer's algorithm

    Args:
        n (int)
        m (int)

    Returns:
        d (int): gcd(n,m)
        xo (int)
        yo (int)

    Raises:
        if n and m not ints -> raise exception

    Comentarios:
        Para mejorar la complejidad temporal del algoritmo, tras cerrar los casos bases, aplicamos el algoritmo de Lehmer. Dicho algoritmo busca 
        en vez de realizar divisiones largas, hace operaciones con las partes más relevantes obteniendo varios cocientes iguales a la vez, acelerando así
        el proceso. Mantiene el tanteo de los coeficientes xo, yo en forma de matriz. Una vez acaba se aplica el algoritmo de
        Euclides.
    """
    # Validar excepciones
    if type(n) != int or type(m) != int:
        raise ZeroDivisionError
    
    # Casos base
    a, b = abs(n), abs(m)
    if (n,m) == (0,0):
        return (0,0,0)
    elif n == 0:
        return (abs(m), 0, 1 if m > 0 else -1)
    elif m == 0:
        return (abs(n), 1 if n > 0 else -1, 0)
    
    # Algoritmo de Lehmer
    # Matriz de coeficientes
    coeffs_matrix = [[1, 0], [0, 1]]  

    while b != 0 and min(a.bit_length(), b.bit_length()) > 128:

        # Valores iniciales
        A, B, C, D = 1, 0, 0, 1
        x, y = obtain_big_nums_lehmers(a, b)

        # Si w1, w2 no son seguros: salir del bucle y aplicar Euclides normal
        if y == 0 or y + C == 0 or y + D == 0:
            break
        w1, w2 = (x+A)//(y+C), (x+B)//(y+D)

        while w1 == w2 and y+C!=0 and y+D!=0 and y!=0:
            w = w1
            A, B, C, D = C, D, A-w*C, B-w*D
            x, y = y, x-w*y

            # Igual que antes: obtener w1 y w2 sólo si se puede
            if y == 0 or y + C == 0 or y + D == 0:
                break
            w1, w2 = (x+A)//(y+C), (x+B)//(y+D)
        
        # Actualizar valores
        if (A,B,C,D)==(1,0,0,1):  
            q = a//b
            a, b = b, a-q*b
            E, F, G, H = coeffs_matrix[0][0], coeffs_matrix[0][1], coeffs_matrix[1][0], coeffs_matrix[1][1]
            coeffs_matrix = [[G,H],[E-q*G,F-q*H]]
        else:  
            a, b = A*a + B*b, C*a + D*b
            E, F, G, H = coeffs_matrix[0][0], coeffs_matrix[0][1], coeffs_matrix[1][0], coeffs_matrix[1][1]
            coeffs_matrix=[[A*E+B*G, A*F+B*H], [C*E+D*G, C*F+D*H]]

    # Euclides estándar
    while b != 0:
        q = a//b
        a, b = b, a-q*b
        E, F, G, H = coeffs_matrix[0][0], coeffs_matrix[0][1], coeffs_matrix[1][0], coeffs_matrix[1][1]
        coeffs_matrix = [[G,H],[E-q*G,F-q*H]]

    # Los coeficientes se han calculado para |n| y |m|: se recupera el signo de las entradas originales
    x, y = coeffs_matrix[0][0], coeffs_matrix[0][1]
    if n < 0:
        x = -x
    if m < 0:
        y = -y
    return abs(a), x, y

def obtain_big_nums_lehmers(a:int, b:int) -> tuple[int,int]:
    """
    Función auxiliar para Bezout.

    Args: 
        a: int
        b: int
    
    Returns:
        x: int
        y: int

    Raises: None

    Comentarios:
        Función en la que se apoya el algoritmo de lehmer para obtener la parte más siginificativa de los números con los que opera
        para facilitar el proceso.
    """
    la, lb = a.bit_length(), b.bit_length()
    s = max(la, lb) - 128
    if s < 0:
        s = 0
    x, y = a >> s, b >> s
    return x, y

def mcd_n(nlist:List[int])->int:
    """ Dados una lista de enteros, devuelve el máximo divisor común a todos ellos.
    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples:
        mcd([4,10,14])=2

    Comentarios:
        Se apoya en la función de máximo común simple.
    """
    #Opcional
    while len(nlist) > 2:
        a,b = nlist[0], nlist[1]
        c = mcd(a,b)
        nlist.remove(a), nlist.remove(b), nlist.append(c)
    return mcd(nlist[0], nlist[1])

def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    #Opcional
    """ Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
    lista de coeficientes [x_1,...,x_n] tal que
        d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    """
    n = len(nlist)
    coeffs = [0]*n
    d = nlist[0]
    coeffs[0] = 1

    for k in range(1,n):
        ak = nlist[k]
        d_new, u, v = bezout(d, ak)
        for i in range(0,k):
            coeffs[i] *= u
        coeffs[k] = v
        d = d_new

    if d < 0:
        d = -d
        coeffs_neg = []
        for c in coeffs:
            coeffs_neg.append(-c)
        coeffs = coeffs_neg
    return d, coeffs

def coprimos(n:int,m:int)->bool:
    """ Determina si dos enteros son coprimos.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples:
        coprimos(14,20)=False
        coprimos(14,15)=True

    Comentarios:
        Devuelve un bool si se cumple la condición dada.
    """
    return mcd(n,m) == 1

def potencia_mod_p(base:int, exp:int, p:int) -> int:
    """ Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.
    
    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si la base y el exponente
        son ambos 0 al mismo tiempo.

    Examples:
        potencia_mod_p(2,3,7)=1

    Comentarios:

    """
    p = abs(p)
    if p == 0 or base == exp == 0:
        raise ZeroDivisionError
    if p == 1:
        return 0
    
    base %= p
    if exp < 0:
        base = inversa_mod_p(base, p)
        exp *= -1

    res = 1
    while exp > 0:
        # Se calculan potencias de la forma base^2^i, por eso se analiza el exponente en binario y se añade al producto sólo aquellos
        # factores en cuyo lugar haya un 1.
        if exp & 1:  # comrpueba si el último dígito en binario es 1 (si es 0 no se añade al resultado)
            res = (res * base) % p
        base = (base * base) % p    
        exp >>= 1  # "elimina" el último dígito (pasa al siguiente, hasta que todos hayan sido comprobados)
    return res

def inversa_mod_p(n:int,p:int)->int:
    """ Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
    
    Examples:
        inversa_mod_p(2,7)=4
    
    Comentarios:
        Para reducir la complejidad temporal se apoya en la función de bezout. Devuelve el coeficiente x que representa el valor buscado.
    """
    p = abs(p)
    if p == 0 or not coprimos(n, p):
        raise ZeroDivisionError
    d, x, y = bezout(n, p)
    return x % p

def euler(n:int)->int:
    """ Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
    menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.
    
    Returns:
        int: Función phi de Euler de n.

    Raises: None

    Examples:
        euler(7)=6
        euler(15)=8

    Comentarios:
        Con el objetivo de reducir la complejidad temporal de la función se apoya en la función de factorizar.
    """
    # Casos específicos
    if n == 1:
        return 1
    
    # Casos generales
    dic_factores = factorizar(n)
    resultado = 1
    for factor in dic_factores:
        resultado *= (factor-1)*factor**(dic_factores[factor]-1)
  
    return resultado

def legendre(n:int,p:int)->int:
    """ Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.
    
    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.

    Examples:
        legendre(2,5)=-1
        legendre(2,7)=1
        legendre(10,5)=0

    Comentarios:
        
    """
    # Caso 1: p divide a n -> devolver 0
    n = n%p
    if n == 0:
        return 0

    # Excepción
    if p == 0:
        raise ZeroDivisionError
    
    # Otros casos: averiguar si hay k tal que k^2 = n mod p
    exp = potencia_mod_p(n, (p-1)//2, p)
    if exp == 1:
        return 1
    else:
        return -1

def miller_rabin_algorithm(p: int) -> bool:
    """Helper function. Studies if a number 'p' is a possible prime or surely not a prime
    Works really well when the number to be studied is really big. Not a certain algorithm but very close to it.

    Args:
        p (int): the number to be studied
    
    Returns:
        bool: True if prime. False if not prime.

    Raises:
        None

    Examples:
        miller_rabin_algorithm(3): True
        miller_rabin_algorithm(4): False
    
    Comentarios:
        Implementado como alternativa probabilística, pero no se usa en el resto de la librería: es_primo, lista_primos,
        factorizar y euler utilizan el test determinista de es_primo (rueda 6k +- 1). Divide el número en el producto de un impar con los
        múltiplos de 2. Elige un número al azar y tras unos cálculos usando aritmética modular determina si el número es certeramente compuesto o probalemente primo.

    """
    # Casos base
    if p < 2:
        return False
    if p in (2,3):
        return True
    if p%2 == 0:
        return False
    
    # Parte 1: p-1 = 2^s*d
    d, s = p-1, 0
    while d%2 == 0:
        d = d//2
        s += 1

    # Parte 2: Bucle que usa base random (mas iteraciones: menos error)
    for i in range(10):  

        a = random.randint(2,p-2)
        x = potencia_mod_p(a,d,p)
        keep_going = False

        # Fermat 
        if x==1 or x==p-1:  # Si no se cumple no es primo
            keep_going = True

        counter = 0
        while not keep_going and counter < s-1:
            x = (x**2)%p
            if x == p-1:  # No es primo
                keep_going = True
            counter += 1

        if not keep_going:
            return False

    return True

def resolver_sistema_congruencias(alist:List[int],blist:List[int],plist:List[int])->Tuple[int,int]:
    """ Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias
    
    a_i * x = b_i (mod p_i)   i=1,...,n
    
    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros
    x congruentes con r módulo m.

    No es necesario que los módulos sean coprimos dos a dos: las congruencias se van combinando de una en una,
    comprobando en cada paso que la nueva es compatible con las anteriores. Los módulos negativos se tratan
    como su valor absoluto.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]
    
    Returns: (r,m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        IncompatibleEquationError: Si no es posible resolver el sistema.

    Examples:
        resolverSistema([2;3;5])=(4,5)
        resolverSistema([2;4;6])=(2,3)
        resolverSistema([1;1;3],[4;7;11])=(10,33)        
    """
    clist = []
    n = len(plist)
    for i in range(n):
        # El módulo se toma en valor absoluto: x = b (mod p) equivale a x = b (mod -p)
        a, b, p = alist[i], blist[i], abs(plist[i])
        if p == 0:
            raise IncompatibleEquationError
        d = mcd(a, p)
        if b % d != 0:
           raise IncompatibleEquationError
        
        a //= d
        b //= d
        p //= d
        try:
            ainv = inversa_mod_p(a, p) 
        except ZeroDivisionError:
            raise IncompatibleEquationError
        c = (ainv * b) % p

        plist[i] = p
        clist.append(c)
        
    r = 0
    M = 1
    for i in range(n):
        # A la congruencia actual (combinación de todas las anteriores) x = r (mod M) se impone la siguiente x = c (mod p). 
        # Si son compatibles, se pasa a la siguiente hasta recorrer todo el sistema.
        # Si alguna no es compatible con el resto del sistema, no existirá solución
        p = plist[i]
        c = clist[i]
        d = mcd(M, p)
        if (c - r) % d != 0:
            # Se exige que r = c (mod d), siendo d = mcd(M, p)
            raise IncompatibleEquationError

        # Partimos de x = r (mod M) => x = r + Mk. Imponiendo la nueva congruencia x = c (mod p) se obtiene r + Mk = c (mod p) => Mk = c − r (mod p).
        # Se escribe M = du, p = dv con mcd(u, v) = 1, dividiendo toda la congruencia por d tenemos uk = (c − r) / d (mod v). (t = k)
        u = M // d
        v = p // d
        ut = ((c - r) // d) % v
        try:
            uinv = inversa_mod_p(u % v, v)
        except ZeroDivisionError:
            raise IncompatibleEquationError
        t = (ut * uinv) % v

        # Ahora, como toda solución de x = r (mod M) es x = r + Mk (t = k), tenemos x = r + Mt (mod Mv).
        # Mv = mcm(M, p), y por tanto si existen soluciones serán congruentes modulo mcm(p1, ..., pn).
        r += M * t
        M = M * v
        r %= M

    return r, M

def raiz_mod_p(n:int,p:int)->int:
    """ Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.

    Examples:
        raiz_mod_p(2,7)=3
    """
    #Opcional
    if p == 2:
        # Como 2 es par, no sirve Cipolla, pero es un caso trivial: 0^2 = 0 mod 2; 1^2 = 1 mod 2. 
        return n % 2
    
    n %= p
    if n == 0:
        return 0
    # Verificar que n es residuo cuadrático: legendre(n,p) debe ser 1
    if legendre(n, p) != 1:
        raise IncompatibleEquationError  # sin raíz en F_p

    # Buscar t tal que u = t^2 - n sea no-residuo
    t = 0
    while True:
        u = (t * t - n) % p
        # u no-residuo si legendre(u,p) == -1 (o potencia_mod_p(u,(p-1)//2,p) == p-1)
        if u != 0 and legendre(u, p) == -1:
            break
        t += 1
        if t == p:
            raise IncompatibleEquationError  # extremadamente improbable si n es residuo

    # Exponenciación binaria en la extensión F_p[w]/(w^2 = u)
    # Representamos acumulador (r0, r1) y base (b0, b1) que significan r0 + r1*w y b0 + b1*w
    e = (p + 1) // 2
    r0, r1 = 1, 0           # elemento neutro (1, 0)
    b0, b1 = t % p, 1       # (t, 1) = t + 1*w

    while e > 0:
        if e & 1:
            # r = r * b: (x1,y1)*(x2,y2) = (x1*x2 + u*y1*y2, x1*y2 + x2*y1) mod p
            nr0 = (r0 * b0 + u * r1 * b1) % p
            nr1 = (r0 * b1 + b0 * r1) % p
            r0, r1 = nr0, nr1
        # b = b * b
        nb0 = (b0 * b0 + u * b1 * b1) % p
        nb1 = (2 * b0 * b1) % p
        b0, b1 = nb0, nb1
        e >>= 1

    # r0 es la parte real de (t + w)^{(p+1)/2}, una raíz de n; la otra es p - r0
    return r0

def ecuacion_cuadratica(a:int,b:int,c:int,p:int)->tuple[int,int]:
    """ Halla, si es posible, las dos posibles soluciones de la ecuación cuadrática ax^2+bx+c=0 (mod p).
    Devuelve una tupla con las dos raíces (distintas o una misma raíz repetida en caso de ser doble).

    Args:
        a (int): Coeficiente de x^2.
        b (int): Coeficiente de x.
        c (int): Término independiente.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns: (x1,x2)
        x1 (int): Primera solución. Entero entre 0 y p-1.
        x2 (int): Segunda solución. Entero entre 0 y p-1.

    Raises:
        IncompatibleEquationError: Si no es posible resolver la ecuación o si a = 0 (mod p), en cuyo caso
            la ecuación no es cuadrática.

    Examples:
        ecuacion_cuadratica(4,1,3,11)
        ecuacion_cuadratica(4,1,5,11)=(3, 5)
        ecuacion_cuadratica(1,2,1,11)=(10,10)
    """
    
    """
    Trabajar con el discriminante. 
    Disc = b**2 -4ac

    caso 1: si Disc congr 0 (mod p) -> sol doble
    caso 2: Disc no es residuo cuadrático mod p (legendre = -1) -> no existen sol (lanzar exception)
    caso 3: Disc residuo cuadrático mod p (legendre = 1) ->  2 raíces distintas
    """
    # Si a = 0 (mod p) la ecuación no es de segundo grado y la fórmula no se puede aplicar (2a no es invertible)
    if a % p == 0:
        raise IncompatibleEquationError

    disc = ((b**2)-(4*a*c))%p # discriminante mod p

    # Caso 1: disc == 0 (mod p)
    if disc%p == 0:
        inv = (inversa_mod_p((2*a)%p, p))
        sol = (-b*inv)%p
        return (sol, sol)
    
    # Case 2: disc != 0 (mod p)
    else:

        # Caso 2.1: legendre(disc,p) = -1
        if legendre(disc, p) == -1:
            raise IncompatibleEquationError
        
        # Caso 2.2: legendre(disc,p) = 1
        elif legendre(disc, p) == 1:
            r = raiz_mod_p(disc, p)

            # Sol1
            inv1 = (inversa_mod_p((2*a)%p, p))
            sol1 = ((-b+r)*inv1)%p

            # Sol2
            inv2 = (inversa_mod_p((2*a)%p, p))
            sol2 = ((-b-r)*inv2)%p

            return (sol1, sol2)

if __name__ == '__main__':
    pass






