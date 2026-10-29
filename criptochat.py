"""
criptochat.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP11B
Integrantes:
    - Jaime Tuesta de Simón
    - Ignacio Mascarell Agúndez

Descripción:
Programa para el cifrado y descifrado de mensajes para dos usuarios.
"""

import sys
import os
import rsa

def ficheros_encontrados(usuario1: str, usuario2: str) -> bool:

	"""
	Recibe 2 nombres de usuarios y comprueba con la librería os que existen los ficheros de claves necesarios:
	las claves pública y privada de usuario1 (para descifrar) y la clave pública de usuario2 (para cifrar).

	Inputs:
		usuario1 (str): primer nombre de usuario.
		usuario2 (str): segundo nombre de usuario.

	Outputs:
		valid (bool): True si se encuentran los ficheros. False de lo contrario.
	"""

	#usa la librería os
	if (os.path.exists(f'Usuarios/pub_{usuario1}.txt') and os.path.exists(f'Usuarios/priv_{usuario1}.txt')
			and os.path.exists(f'Usuarios/pub_{usuario2}.txt')):
		return True
	
	if not (os.path.exists(f'Usuarios/pub_{usuario1}.txt') and os.path.exists(f'Usuarios/priv_{usuario1}.txt')):
		print(f'No se han encontrado los ficheros asociados a {usuario1}.')
	if not os.path.exists(f'Usuarios/pub_{usuario2}.txt'):
		print(f'No se han encontrado los ficheros asociados a {usuario2}.')
	return False


def preguntar_intencion() -> str:

	"""
	Esta función pregunta al usuario la opción que desea realizar. (S: Salir, C: Cifrar, D: Descifrar). Comprueba que
	la opción que la opción elegida sea válida.

	Inputs:
		None

	Outputs:
		opcion_elegida (str): la opción elegida entre las posibles.
	"""
	
	#opciones posibles
	opciones_posibles = ['C', 'D', 'S']

	#bucle que comprueba que la opción introducida es válida
	opcion_elegida = input('Introduce la opción que desees realizar (C - cifrar, D - descifrar, S - salir): ').upper()
	while opcion_elegida not in opciones_posibles:
		print('Debes elegir una de las opciones posibles.')
		opcion_elegida = input('\nIntroduce la opción que desees realizar (C - cifrar, D - descifrar, S - salir): ').upper()
		
	return opcion_elegida


def pedir_mensaje(intencion: str) -> str:

	"""
	Esta función pide el mensaje que se desea cifrar o descifrar.

	Inputs:
		intencion (str): la intención del usuario. Cifrar o descifrar. Según el valor variará el mensaje, pero es irrelevante para la función.
	
	Outputs:
		mensaje (str): el mensaje que se desea cifrar o descifrar.
	"""

	if intencion == 'C':
		obj = 'cifrar'
	elif intencion == 'D':
		obj = 'descifrar'

	mensaje = input(f'Introduce el mensaje que desees {obj}: ')

	return mensaje


def cifrar_texto_plano(texto_plano: str, usuario: str) -> list[int]:

	"""
	Recibe un texto plano. Saca las claves para el cifrado y realiza el mismo.

	Inputs:
		texto_plano (str): mensaje a cifrar
		usuario (str): nombre del usuario cuyas claves se van a obtener

	Outputs:
		mensaje_cifrado (list): mensaje cifrado como una lista de enteros.
	"""

	#sacar las claves necsarias para el cifrado
	n, e, cifras_padding = sacar_claves_pub(usuario)

	#cifrar el mensaje
	mensaje_cifrado = rsa.cifrar_cadena_rsa(texto_plano, n, e, cifras_padding)

	return mensaje_cifrado


def sacar_claves_pub(usuario: str) -> list[int, int, int]:

	"""
	Recibe el nombre de un usuario y saca sus claves públicas de un fichero.

	Inputs:
		usuario (str): nombre del usuario cuyas claves públicas se van a obtener.

	Outputs:
		lista_claves_pub (list): lista que contiene las claves públicas del usuario.
	"""

	lista_claves_pub = []

	#abrir ficherro
	fichero_claves_pub = open(f'Usuarios/pub_{usuario}.txt', 'r', encoding='utf-8')

	#recorrer fichero según la estructura dada en el enunciado
	for linea in fichero_claves_pub:
		lista_claves_pub.append(int(linea.strip()))
	fichero_claves_pub.close()

	return lista_claves_pub


def sacar_claves_priv(usuario: str) -> list[int, int, int]:

	"""
	Recibe el nombre de un usuario y saca sus claves privadas de un fichero.

	Inputs:
		usuario (str): nombre del usuario cuyas claves privadas se van a obtener.

	Outputs:
		lista_claves_priv (list): lista que contiene las claves privadas del usuario.
	"""

	lista_claves_priv = []

	#abrir el fichero
	fichero_claves_priv = open(f'Usuarios/priv_{usuario}.txt', 'r', encoding='utf-8')

	#recorrer fichero según la estructura dada en el enunciado
	for linea in fichero_claves_priv:
		lista_claves_priv.append(int(linea.rstrip('\n')))
	fichero_claves_priv.close()

	return lista_claves_priv


def imprimir_mensaje_cifrado(mensaje_imprimir: list[str|int]) -> None:

	"""
	Recibe un mensaje como lista, lo transforma en str y lo imprime.

	Inputs:
		mensaje_imprimir (list): mensaje como lista

	Outputs:
		None
	"""

	mensaje_final = '\nMENSAJE CIFRADO: '
	for element in mensaje_imprimir:
		mensaje_final += f'{element} '  #añadir al mensaje final

	print(mensaje_final[:-1])  #pintar sin último espacio

def imprimir_mensaje_descifrado(mensaje_imprimir: list[str|int]) -> None:

	"""
	Recibe un mensaje como lista, lo transforma en str y lo imprime.

	Inputs:
		mensaje_imprimir (list): mensaje como lista

	Outputs:
		None
	"""

	mensaje_final = '\nMENSAJE DESCIFRADO: '
	for element in mensaje_imprimir:
		mensaje_final += f'{element}'  #añadir al mensaje final

	print(mensaje_final)


def almacenar_mensaje_cifrado(mensaje_cifrado: str) -> list[int]:

	"""
	Recibe un mensaje cifrado como str y lo transforma en una lista de enteros para facilitar el descifrado.

	Inputs:
		mensaje_cifrado (str): mensaje como str

	Outputs:
		lista_int (list): mensaje como lista de enteros

	Raises:
		ValueError: si algún elemento del mensaje no es un entero.
	"""

	#usar método split para transformar en lista (admite varios espacios seguidos)
	lista_str = mensaje_cifrado.split()

	#convertir a una lista de enteros para facilitar el descifrado
	lista_int = []
	for caracter_str in lista_str:
		try:
			lista_int.append(int(caracter_str))
		except ValueError:
			raise ValueError('el mensaje cifrado debe ser una secuencia de enteros separados por espacios.')

	return lista_int

def descifrar_mensaje(mensaje_cifrado: list[int], usuario: str) -> str:

	"""
	Recibe un mensaje y un usuario. Descifra el mensaje según las claves del usuario. Se apoya en otras funciones.

	Inputs:
		mensaje_cifrado (list[int]): mensaje a descifrar

	Outputs:
		usuario (str): usuario del que se sacan las claves para el descifrado
	"""

	#sacar las claves públicas y privadas del usuario
	n, e, cifras_padding = sacar_claves_pub(usuario) 
	d = sacar_claves_priv(usuario)[0]

	#descifrar la lista de enteros que representa el mensaje
	cadena_descifrada = rsa.descifrar_cadena_rsa(mensaje_cifrado, n, d, cifras_padding)
	return cadena_descifrada


if __name__ == '__main__':

	#recibir argumentos
	argumentos = sys.argv
	args_valid = True
	if len(argumentos) != 3:
		print('Debe introducir exactamente dos usuarios para iniciar el criptochat.')
		args_valid = False

	if args_valid:
		usuario1, usuario2 = argumentos[1], argumentos[2]

		#buscar ficheros
		if ficheros_encontrados(usuario1, usuario2):
			finished = False
			while not finished:
				intencion = preguntar_intencion()

				#si es C -> cifrar
				if intencion == 'C':
					texto_plano = pedir_mensaje(intencion)
					mensaje_cifrado = cifrar_texto_plano(texto_plano, usuario2)
					imprimir_mensaje_cifrado(mensaje_cifrado)
					print('\nPuede realizar otra operación.')
				
				#si es D -> descifrar
				elif intencion == 'D':
					texto_cifrado = pedir_mensaje(intencion)
					try:
						lista_cifrada = almacenar_mensaje_cifrado(texto_cifrado)
						mensaje_descifrado = descifrar_mensaje(lista_cifrada, usuario1)
						imprimir_mensaje_descifrado(mensaje_descifrado)
					except ValueError as error:
						#mensaje no numérico o enteros que no corresponden a caracteres válidos
						print(f'\nNo se ha podido descifrar el mensaje: {error}')
					print('\nPuede realizar otra operación.')

				#si es S -> salir
				elif intencion == 'S':
					print('Saliendo del programa.')
					finished = True
			