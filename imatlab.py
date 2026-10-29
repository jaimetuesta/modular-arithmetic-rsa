"""
imatlab.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP11B
Integrantes:
    - Jaime Tuesta de Simón
    - Ignacio Mascarell Agúndez

Descripción:
Sistema interactivo IMAT-LAB de resolución de ecuaciones en aritmética modular.

Interfaz de acceso interactivo o por lotes a la librería modular.py. Si este script se ejecuta sin parámetros,
lanza la interfaz de usuario para el modo interactivo.
"""

from typing import List, TextIO
from io import StringIO
import sys
import re
import modular


# --- Expresiones regulares de los comandos ---

primo_rx = re.compile(r'^\s*primo\(\s*([+-]?\d+)\s*\)\s*$')
lista_primos_rx = re.compile(r'^\s*primos\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)\s*$')
factorizar_rx = re.compile(r'^\s*factorizar\(\s*([+-]?\d+)\s*\)\s*$')
mcd_rx = re.compile(r'^\s*mcd\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)\s*$')
mcd_n_rx = re.compile(r'^\s*mcd\(\s*([^)]+)\s*\)\s*$')
coprimos_rx = re.compile(r'^\s*coprimos\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)\s*$')
potencia_rx = re.compile(r'^\s*pow\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)\s*$')
inversa_rx = re.compile(r'^\s*inv\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)\s*$')
euler_rx = re.compile(r'^\s*euler\(\s*([+-]?\d+)\s*\)\s*$')
legendre_rx = re.compile(r'^\s*legendre\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)\s*$')
sistema_rx = re.compile(r'^\s*resolverSistema\(\s*([^)]+)\s*\)\s*$')
raiz_rx = re.compile(r'^\s*raiz\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)\s*$')
cuadratica_rx = re.compile(r'^\s*ecCuadratica\(\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*\)\s*$')

AYUDA = """
COMANDOS VÁLIDOS:
primo(n)                                     - Calcula si n es primo
primos(a,b)                                  - Lista de primos entre a y b (a incluido, b no)
factorizar(n)                                - Descomposición en factores primos de n
mcd(a,b,...)                                 - Máximo común divisor de una serie de enteros a,b,...
coprimos(a,b)                                - Calcula si a y b son coprimos
pow(a,b,p)                                   - Calcula a^b (mod p)
inv(n,p)                                     - Inversa de n (mod p)
euler(n)                                     - Función phi de Euler de n
legendre(n,p)                                - Símbolo de Legendre de n (mod p)
resolverSistema([a1;b1;p1],[a2;b2;p2],...)   - Resuelve sistema de congruencias ai*x = bi (mod pi)
raiz(n,p)                                    - Raíz cuadrada de n (mod p)
ecCuadratica(a,b,c,p)                        - Raíces del polinomio ax^2 + bx + c (mod p)

Introduce una línea vacía para salir.
"""


# --- Funciones auxiliares ---

def enteros(m: re.Match) -> List[int]:
    """Convierte a enteros todos los grupos capturados por una expresión regular."""
    return [int(g.strip()) for g in m.groups()]


def unir(valores: List[int]) -> str:
    """Escribe una lista de valores separados por comas, que es el formato de salida de IMAT-LAB."""
    return ', '.join(str(v) for v in valores)


def si_no(condicion: bool) -> str:
    return 'Sí' if condicion else 'No'


# --- Un comando por función ---
# Cada función recibe el resultado del match y devuelve la línea de salida (sin salto de línea).
# Los errores no se tratan aquí: ValueError se traduce a NOP y ZeroDivisionError o
# IncompatibleEquationError a NE en procesar_linea.

def comando_primo(m: re.Match) -> str:
    n, = enteros(m)
    return si_no(modular.es_primo(n))


def comando_primos(m: re.Match) -> str:
    a, b = enteros(m)
    if a > b:  # en el comando se admite el intervalo en cualquier orden
        a, b = b, a
    lista = modular.lista_primos(a, b)
    if not lista:
        return 'NE'
    return unir(lista)


def comando_factorizar(m: re.Match) -> str:
    n, = enteros(m)
    if n in [-1, 0, 1]:  # no tienen factores primos
        return str(n)
    factores = modular.factorizar(n)
    return ', '.join(f'{p}: {e}' for p, e in factores.items())


def comando_mcd(m: re.Match) -> str:
    a, b = enteros(m)
    return str(modular.mcd(a, b))


def comando_mcd_n(m: re.Match) -> str:
    # los números llegan como un único texto separado por comas
    lista = [int(x.strip()) for x in m.group(1).split(',')]
    if len(lista) == 1:  # mcd(a) = a
        return str(lista[0])
    return str(modular.mcd_n(lista))


def comando_coprimos(m: re.Match) -> str:
    a, b = enteros(m)
    return si_no(modular.coprimos(a, b))


def comando_potencia(m: re.Match) -> str:
    base, exp, p = enteros(m)
    if p == 0:  # un módulo negativo se trata como su valor absoluto
        return 'NE'
    return str(modular.potencia_mod_p(base, exp, p))


def comando_inversa(m: re.Match) -> str:
    n, p = enteros(m)
    if p == 0:  # un módulo negativo se trata como su valor absoluto
        return 'NE'
    return str(modular.inversa_mod_p(n, p))


def comando_euler(m: re.Match) -> str:
    n, = enteros(m)
    if n <= 0:  # phi solo está definida para enteros positivos
        return 'NE'
    return str(modular.euler(n))


def comando_legendre(m: re.Match) -> str:
    n, p = enteros(m)
    if not modular.es_primo(p) or p == 2:  # el símbolo de Legendre necesita un primo impar
        return 'NE'
    return str(modular.legendre(n, p))


def comando_sistema(m: re.Match) -> str:
    # formato: [a1;b1;p1],[a2;b2;p2],...
    alist, blist, plist = [], [], []
    for ecuacion in m.group(1).split(','):
        coefs = ecuacion.strip().strip('[]').split(';')
        if len(coefs) != 3:  # cada ecuación debe tener exactamente a, b y p
            raise ValueError
        a, b, p = [int(c.strip()) for c in coefs]
        alist.append(a)
        blist.append(b)
        plist.append(p)
    # p = 0 lo rechaza modular (NE); un p negativo se trata como |p|
    r, mod = modular.resolver_sistema_congruencias(alist, blist, plist)
    return f'{r} (mod {mod})'


def comando_raiz(m: re.Match) -> str:
    n, p = enteros(m)
    if p <= 0:
        return 'NE'
    r = modular.raiz_mod_p(n, p)
    # si r es raíz, p - r también lo es: se muestran ordenadas y sin repetir
    raices = sorted({r % p, (p - r) % p})
    return unir(raices)


def comando_cuadratica(m: re.Match) -> str:
    a, b, c, p = enteros(m)
    if p <= 0:
        return 'NE'
    x1, x2 = modular.ecuacion_cuadratica(a, b, c, p)
    # raíz doble: se muestra una sola vez
    return unir(sorted({x1, x2}))


# Orden en que se prueban los comandos. mcd(a,b) va antes que mcd(a,b,...) porque las dos expresiones
# aceptan dos argumentos y se usa la primera que encaje.
COMANDOS = [
    (primo_rx, comando_primo),
    (lista_primos_rx, comando_primos),
    (factorizar_rx, comando_factorizar),
    (mcd_rx, comando_mcd),
    (mcd_n_rx, comando_mcd_n),
    (coprimos_rx, comando_coprimos),
    (potencia_rx, comando_potencia),
    (inversa_rx, comando_inversa),
    (euler_rx, comando_euler),
    (legendre_rx, comando_legendre),
    (sistema_rx, comando_sistema),
    (raiz_rx, comando_raiz),
    (cuadratica_rx, comando_cuadratica),
]


# --- Ejecución de comandos ---

def procesar_linea(linea: str) -> str:
    """
    Ejecuta un comando de IMAT-LAB y devuelve su salida.

    Devuelve 'NOP' si la línea no es un comando válido (o sus argumentos no son enteros) y 'NE' si el
    comando es válido pero no tiene solución.
    """
    for patron, comando in COMANDOS:
        m = patron.match(linea)
        if m:
            try:
                return comando(m)
            except ValueError:
                # argumentos que no son enteros, o ecuaciones de resolverSistema mal agrupadas
                return 'NOP'
            except (ZeroDivisionError, modular.IncompatibleEquationError):
                # las funciones de modular.py indican así que no existe solución
                return 'NE'
    return 'NOP'


def run_commands(fin: TextIO, fout: TextIO) -> None:
    """Lee comandos de fin, uno por línea, y escribe en fout el resultado de cada uno."""
    for linea in fin:
        fout.write(procesar_linea(linea.strip()) + '\n')


def modo_interactivo() -> None:
    """Pide comandos por teclado hasta que se introduce una línea vacía."""
    print(AYUDA)
    try:
        linea = input('Operación a realizar: ')
        while linea.strip() != '':
            print(procesar_linea(linea.strip()))
            linea = input('Operación a realizar: ')
    except EOFError:  # fin de la entrada (Ctrl+D / Ctrl+Z)
        pass


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        modo_interactivo()
    elif len(args) == 2:
        # el argumento puede ser un fichero de entrada o un comando suelto
        try:
            with open(args[1], 'r', encoding='utf-8') as fin:
                run_commands(fin, sys.stdout)
        except OSError:
            run_commands(StringIO(args[1]), sys.stdout)
    elif len(args) == 3:
        # fichero de entrada y fichero de salida
        try:
            with open(args[1], 'r', encoding='utf-8') as fin:
                with open(args[2], 'w', encoding='utf-8') as fout:
                    run_commands(fin, fout)
        except OSError:
            print('Los argumentos deben ser imatlab.py fichero_entrada fichero_salida. Inténtelo de nuevo.')
    else:
        print('Los argumentos deben ser imatlab.py fichero_entrada fichero_salida. Inténtelo de nuevo.')
