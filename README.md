# Lector de Facturas XML con Tkinter

Este es un proyecto simple que consiste en una aplicación GUI desarrollada en Python utilizando Tkinter, diseñada para cargar y visualizar datos de facturas XML. 
Está creado especialmente para los requerimientos de un cliente específico

## Descripción

La aplicación permite al usuario seleccionar un archivo XML de factura, cargarlo, mostrar información relevante como fecha, folio, receptor, etc., y proporciona la opción de copiar ciertos datos al portapapeles.

## Funcionalidades

- **Cargar factura:** Permite seleccionar un archivo XML de factura desde el sistema.
- **Mostrar detalles:** Visualiza información como fecha, folio, receptor, número de pedido, número de remisión y total.
- **Copiar datos:** Permite copiar ciertos datos al portapapeles con un clic.
- **Mostrar conceptos:** Muestra los conceptos (productos) de la factura en un widget Treeview.

## Requisitos

El proyecto requiere Python 3.x y las siguientes bibliotecas Python:

- tkinter
- pyperclip

## Instalación
1. Clona el repositorio
```sh
git clone https://github.com/tu_usuario/tu_repositorio.git
```
3. Navega al directorio del proyecto
```sh
cd tu_repositorio
```
5. Instala las dependencias usando Pipenv
```sh
pipenv install
```

Esto instalará todas las dependencias necesarias, incluyendo `tkinter` y `pyperclip`.

## Uso

Para ejecutar la aplicación, activa el entorno virtual de Pipenv:
```sh
pipenv shell
```
Y luego corre el archivo `main.py`:
```sh
python main.py
```
