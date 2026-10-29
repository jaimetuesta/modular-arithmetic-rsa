"""
registrarusuario.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP11B
Integrantes:
    - Jaime Tuesta de Simón
    - Ignacio Mascarell Agúndez

Descripción:
Programa para la creación de usuarios con sus claves públicas y privadas de RSA.
"""

import rsa
import os

def pedir_nombre() -> str:

	"""
	Pide el nombre del usuario.

	Args:
		None

	Returns:
		nombre_usuario (str): nombre del usuario introducido desde la terminal.
	"""

	#pide por la terminal
	nombre_usuario = input('Introduce un nombre: ') 
	return nombre_usuario

def pedir_intervalo() -> tuple[int,int]:

	"""
	Pide los extremos del intervalo en el que se buscarán los primos de las claves. Llama a otra función para comprobar que los valores
	introducidos sean válidos (enteros y ordenados). 

	Inputs:
		None

	Outputs:
		a (int): extremo inferior del intervalo (incluido).
		b (int): extremo superior del intervalo (excluido).
	"""

	#bucle para pedir valores correctos
	valid = False
	while not valid:
		a = input('\nIntroduce el valor mínimo de cada primo usado para generar sus claves de RSA:  ')
		b = input('Introduce el valor máximo de cada primo usado para generar sus claves de RSA:  ')

		#comrpobar que son válidos
		valid = comprobar_validez_intervalo(a, b)  

	return int(a), int(b)

def comprobar_validez_intervalo(a: str, b: str) -> bool:

	"""
	Recibe dos valores y comprueba que cumplen unas condiciones (enteros y ordenados).

	Inputs:
		primo1 (str): el primer valor a comprobar.
		primo2 (str): el segundo valor a comprobar.

	Outputs:
		valid (bool): True en caso de cumplir las condiciones. De lo contrario False.
	"""

	#comprobar ints
	try:
		a, b = int(a), int(b)
	except ValueError:
		print('Los valores introducidos deben ser enteros.')
		return False

	#comprobar que el intervalo está ordenado (a < b)
	if a >= b:
		print('El segundo valor introducido debe ser mayor que el primero.')
		return False

	return True

def crear_ficheros(nombre: str, n: int, d: int, e: int, n_cifras_padding: int) -> None:

	"""
	Esta función recibe los valores para las claves y crea unos ficheros que los contienen.

	Inputs:
		nombre (str): nombre del usuario. Uso para nombre de ficheros.
		n (int): Clave para fichero público.
		d (int): Clave para fichero privado.
		e (int): Clave para fichero público.
		n_cifras_padding (int): Clave para fichero público.

	Outputs:
		None
	"""

	#crear carpeta si es necesario
	os.makedirs('Usuarios', exist_ok=True)

	#crear fichero público
	fichero_pub = open(f'Usuarios/pub_{nombre}.txt', 'w', encoding='utf-8')
	fichero_pub.write(f'{n}\n')
	fichero_pub.write(f'{e}\n')
	fichero_pub.write(f'{n_cifras_padding}\n')
	fichero_pub.close()

	#crear fichero privado
	fichero_pub = open(f'Usuarios/priv_{nombre}.txt', 'w', encoding='utf-8')
	fichero_pub.write(f'{d}\n')
	fichero_pub.close()


def pedir_cifras_padding() -> int:

	"""
	Esta función pide las cifras de padding. Comprueba que sean válidas (entero no negativo).

	Inputs:
		None

	Outputs:
		cifras_padding (int): el número de cifras de padding.
	"""

	#booleano para iniciar bucle
	valid = False
	while not valid:
		try:
			cifras_padding = int(input('\nIntroduce el número de cifras padding que deseas para la comunicación con el usuario:  '))
			if cifras_padding < 0:
				print('El número de cifras de padding no puede ser negativo.')   #continua en el bucle
			else:
				valid = True  #sale del bucle
		except ValueError as error:
			print('El valor introducido debe ser un entero.')   #continua en el bucle
	
	return cifras_padding

if __name__ == '__main__':

	#obtener datos
	nombre_usuario = pedir_nombre()
	a, b = pedir_intervalo()
	n_cifras_padding = pedir_cifras_padding()

	#obtener claves (si el intervalo no contiene dos primos distintos, se vuelve a pedir)
	claves_generadas = False
	while not claves_generadas:
		try:
			n, e, d = rsa.generar_claves(a, b)
			claves_generadas = True
		except ValueError as error:
			print(error)
			a, b = pedir_intervalo()

	#crear fichero
	crear_ficheros(nombre_usuario, n, d, e, n_cifras_padding)