"""
rsa.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP11B
Integrantes:
    - Jaime Tuesta de Simón
    - Ignacio Mascarell Agúndez

Descripción:
Librería para la realización de cifrado y descifrado usando el algoritmo RSA.
"""

import modular
import random
from typing import Tuple,List


def generar_claves(min_primo: int, max_primo: int) -> Tuple[int, int, int]:

    """
    Toma dos primos entre min_primo (incluido) y max_primo (excluido) y devuelve
    n,e,d
    donde (n,e) es la clave pública y d la clave privada para RSA

    Args:
        min_primo (int): Límite inferior para los primo p1 y p2 usados en la clave
        max_primo (int): Límite superior para los primo p1 y p2 usados en la clave
    
    Returns:
        n (int): Módulo para RSA, formado por el producto de dos primos p1 y p2 tales que
            min_primo<=p1, p2 < max_primo
        e (int): Exponente de la clave pública para RSA con módulo n=p1*p2
        d (int): Exponente de la clave privada para RSA con módulo n

    Raises:
        ValueError: Si no es posible encontrar una pareja de primos distintos p1,p2 entre min_primo y max_primo
    """
    
    #crear lista con todos los posibles primos
    lista_primos = modular.lista_primos(min_primo, max_primo)
    if len(lista_primos) <= 1:
        raise ValueError('No existen dos primos diferentes en el intervalo dado.')

    #seleccionar aleatoriamente los primos
    p1, p2 = 0, 0
    while p2 == 0:
        p1, p2 = random.choice(lista_primos), random.choice(lista_primos)
        if p2 == p1:
            p2 = 0

    #crear el valor n = p1*p2
    n = p1*p2

    #calcular fi_n de manera rápida aplicando las propiedades de la función de euler: fi_n = (p2-1)*(p1-1)
    fi_n = (p2-1)*(p1-1)

    #seleccionar un valor e aleatorio dentro de un intervalo
    e = 0
    while e == 0:
        selected_number = random.randint(2,fi_n-1)
        if modular.coprimos(selected_number, fi_n):
            e = selected_number

    #calcular d = e^-1 (mod fi_n)
    d = modular.inversa_mod_p(e, fi_n)

    return n, e, d


def aplicar_padding(m:int, digitos_padding:int) -> int:

    """
    Dado un mensaje y un número de dígitos de padding, añade
    digitos_padding cifras aleatorias a la derecha del mensaje
    
    Args:
        m (int): Mensaje sin padding
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero formado por los dígitos de m seguidos de digitos_padding cifras aleatorias.

    Raises: None

    Example:
        aplicar_padding(24,2)=2419
        aplicar_padding(24,2)=2403
        aplicar_padding(24,3)=24718
        aplicar_padding(24,3)=24845
        aplicar_padding(24,0)=24
    """
    
    #transformar el número a str
    m_str = str(m)

    #añadir a str las cifras de padding
    for i in range(digitos_padding):
        m_str += str(random.randint(0,9))
    
    #devolver cadena como entero
    return int(m_str)
    


def eliminar_padding(m:int, digitos_padding:int) -> int:

    """
    Dado un mensaje con padding de digitos_padding cifras al
    final del mismo, elimina dichas cifras aleatorias y devuelve
    el resto de cifras del mensaje

    Args:
        m (int): Mensaje con padding
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero resultante de eliminar las últimas digitos_padding cifras de m.

    Raises: None
    
    Example:
        eliminar_padding(2454,1)=245
        eliminar_padding(2454,2)=24
        eliminar_padding(2454,3)=2
        eliminar_padding(2432,2)=24
        eliminar_padding(2432,0)=2432
    """
    #si no hay padding, se devuelve el mensaje tal cual
    if digitos_padding == 0:
        return m
    
    #transformar a str
    m_str = str(m)
    if digitos_padding >= len(m_str):
        return 0

    #devolver entero quitando cifras de padding
    return int(m_str[:len(m_str)-digitos_padding])


def cifrar_rsa(m:int, n:int, e:int, digitos_padding:int) -> int:

    """
    Dado un mensaje m entero, un módulo y exponente que formen parte
    de una clave pública de RSA, con m<n*10^{-digitos_padding}, y un número
    de dígitos de padding, aplica el padding al mensaje y lo cifra
    usando RSA con módulo n y exponente e.
    
    Args:
        m (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA
        e (int): Exponente de la clave pública de RSA
        digitos_padding (int): Número no negativo de cifras de padding
    
    Returns:
        int: entero resultante de agregar el padding a m y aplicar RSA.

    Raises: None
    """

    #aplicar padding
    m_new = aplicar_padding(m, digitos_padding)

    #devolver c = m^e(mod n)
    return modular.potencia_mod_p(m_new,e,n)


def descifrar_rsa(c: int, n: int, d: int, digitos_padding: int) -> int:

    """
    Dado un cifrado c entero que haya sido cifrado con RSA usando
    digitos_padding cifras de padding al final del mensaje y el 
    módulo y exponente privado, n y d que formen la clave privada de RSA cuya pareja se
    utilizó para cifrar c, descifra c y elimina el padding, devolviendo
    el mensaje original.

    Args:
        c (int): Mensaje original claro (sin padding)
        n (int): Módulo de la clave pública de RSA usado para cifrar
        d (int): Exponente de la clave privada de RSA cuya pareja se utilizó para cifrar c
        digitos_padding (int): Número no negativo de cifras de padding usados para cifrar c
    
    Returns:
        int: entero resultante de descifrar c usando RSA con módulo m y exponente e y después eliminar el padding al resultado.

    Raises: None
    """

    #devolver el emnsaje descifrado sin los dígitos de padding
    return eliminar_padding(modular.potencia_mod_p(c, d, n), digitos_padding)


def codificar_cadena(s: str) -> List[int]:

    """
    Convierte una cadena de caracteres a la lista de
    enteros que representa el valor unicode cada uno de sus caracteres.

    Args:
        s (str): cadena en texto plano

    Returns:
        int: lista de enteros que representan el código unicode de cada carácter de la cadena s.

    Raises: None.

    Example:
        codificar_cadena("¡Hola mundo!")=[161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33]
    """
    
    #codificar la cadena con los valores ascii
    cadena_codificada = []
    for letra_cifrar in s:
        cadena_codificada.append(ord(letra_cifrar))

    return cadena_codificada


def decodificar_cadena(m: List[int]) -> str:

    """
    Convierte una lista de enteros que representen caracteres unicode
    en la cadena que representan.
    
    Args:
        m (List[int]): lisa de enteros que representan los códigos unicode de una cadena de caracteres.
    
    Returns:
        str: cadena que representan

    Raises:
        ValueError: Si alguno de los enteros no representa un caracter unicode válido.
    
    Example:
        decodificar_cadena([161, 72, 111, 108, 97, 32, 109, 117, 110, 100, 111, 33])="¡Hola mundo!"
    """
    
    try:
        #descifrar la cadena con los valores ascii
        cadena_descodificada = ''
        for valor_codificado in m:
            cadena_descodificada += chr(valor_codificado)
    except:
        raise ValueError('No se puede descodificar el mensaje, hay enteros que no representan caracteres válidos.')

    return cadena_descodificada


def cifrar_cadena_rsa(s: str, n: int, e: int, digitos_padding: int) -> List[int]:

    """
    Cifra carácter a carácter una cadena de caracteres usando RSA con clave púbica (n,e)
    y digitos_padding cifras de padding al final del mensaje y devuelve la lista de enteros
    que representan el mensaje cifrado correspondiente.
    Args:
        s (str): texto claro
        n (int): módulo para RSA
        e (int): clave pública para RSA
        digitos_padding (int): número no negativo de dígitos de padding que deben usarse para el cifrado del mensaje.
    
    Returns:
        List[int]: lista de enteros que representa el mensaje cifrado con RSA para la clave dada.

    Raises: None
    """
    
    #codificar
    cadena_codificada = codificar_cadena(s)

    #cifrar
    cadena_cifrada = []
    for valor_codificado in cadena_codificada:
        cadena_cifrada.append(cifrar_rsa(valor_codificado, n, e, digitos_padding))
    return cadena_cifrada


def descifrar_cadena_rsa(cList: List[int], n: int, d: int, digitos_padding: int) -> str:

    """
    Dado un mensaje cifrado con RSA usando la clave pública cuya clave privada asociada es (n,d)
    y digitos_padding cifras de padding al final del mensaje, devuelve la cadena orignal.
    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        d (int): clave privada para RSA
        digitos_padding (int): número no negativo de dígitos de padding usados para el cifrado de cList.
    
    Returns:
        str: cadena que representa el texto claro correspondiente al mensaje cifrado cList.

    Raises:
        ValueError: Si, tras decodificar, alguno de los enteros del mensaje no representa un caracter unicode válido.    
    """
    
    #descifrar
    cadena_decodificar = []
    for valor_cifrado in cList:
        cadena_decodificar.append(descifrar_rsa(valor_cifrado, n, d, digitos_padding))
    
    #descodificar
    try:
        cadena_descodificada = decodificar_cadena(cadena_decodificar)
    except ValueError as error:
        raise ValueError(error)
    return cadena_descodificada



def romper_clave(n: int, e: int) -> int:

    """
    A partir de una clave pública válida (n,e), recupera la clave privada d tal que
    de = 1 (mod phi(n)).
    
    Args:
        n (int): módulo para RSA
        e (int): clave pública para RSA
    
    Returns:
        int: clave privada d

    Raises:
        ValueError: Si no existe ninguna clave privada d compatible con la clave pública (n,e).
    """
    #devolver la clave d = e^-1 (mod euler(n))
    try:
        d = modular.inversa_mod_p(e, modular.euler(n))
        return d
    except:
        raise ValueError('No existe ninguna clave privada d compatible con la clave pública (n, e)')

def ataque_texto_elegido(cList: List[int], n: int, e: int) -> str:

    """
    Ejecuta un ataque de texto claro elegido sobre un mensaje que ha sido cifrado
    con RSA plano sin usar padding a partir de su clave pública.

    Args:
        cList (List[int]): lisa de enteros que representan el mensaje cifrado
        n (int): módulo para RSA
        e (int): clave pública para RSA
    
    Returns:
        str: texto plano descifrado para el mensaje cifrado cList

    Raises:
        ValueError: Si el mensaje no se corresponde con ningún texto plano que haya sido codificado con RSA sin padding.

    Comentarios:
        No necesita la clave privada. Sin padding, el cifrado es determinista y cada carácter se cifra por separado,
        así que un mismo carácter produce siempre el mismo número. Basta con cifrar con la clave pública los posibles
        caracteres unicode (desde el código 0 en adelante) hasta encontrar todos los valores que aparecen en el mensaje,
        y sustituir cada valor cifrado por el carácter que lo genera. Normalmente el texto usa caracteres de código bajo,
        por lo que la búsqueda termina pronto. Con padding el cifrado deja de ser determinista y el ataque no funciona:
        devuelve un error o un texto sin sentido.
    """

    #valores cifrados distintos que hay que identificar
    pendientes = set(cList)
    tabla = {}

    #cifrar cada carácter posible con la clave pública y anotar los que aparecen en el mensaje
    codigo = 0
    while pendientes and codigo < 0x110000:  # 0x110000: número de códigos unicode
        c = cifrar_rsa(codigo, n, e, 0)
        if c in pendientes:
            tabla[c] = codigo
            pendientes.remove(c)
        codigo += 1

    if pendientes:
        raise ValueError('El mensaje no se corresponde con ningún texto cifrado con esta clave pública sin padding.')

    #sustituir cada valor cifrado por su carácter
    mensaje = []
    for c in cList:
        mensaje.append(tabla[c])
    return decodificar_cadena(mensaje)