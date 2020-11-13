# Tarea 3 - INF331 Pruebas de Software
Diego Moraga Araya - 201773035-8

### Especificaciones
Esta tarea está desarrollada en `Python 3.6`

### Instalación
Es necesario tener instalado `Python 3.6` y la librería `boto3`.

### Instrucciones de ejecución
Para ejecutar el programa, en la terminal se debe ingresar
~~~
$ python tarea.py -k AWS_ACCESS_KEY -i AWS_SECRET_KEY
~~~
donde `"AWS_ACCESS_KEY"` corresponde a la ID de clave de acceso y `"AWS_SECRET_KEY"` corresponde a la clave de acceso secreta. Luego seguir las instrucciones, pedirá ingresar el nombre del bucket y los nombres de las imágenes de control y de prueba (previamente cargadas en el bucket ingresado), por ejemplo:
~~~
$ python tarea.py -k AWS_ACCESS_KEY -i AWS_SECRET-KEY
$ Ingrese nombre del bucket: bucket-tarea-psw
$ Ingrese nombre de imagen de control: monday.png
$ Ingrese nombre de imagen de prueba: monday1.jpeg
~~~

Los logs se registran en el archivo `logs.txt`.