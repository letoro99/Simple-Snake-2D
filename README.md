# snake_tarea1

*** v0.6 ***
 - Los archivos fueron agregados al git.

*** v0.7 ***
 - Se agrego la textura a la cabeza de la serpiente
 - Se creo la pantalla de Game Over con su textura y animacion
 - Se cereo el agloritmo de fondo cuadriculado pero pierde eficiencia cuando aumenta las dimensiones
 del entorno
 - Se agrego la rotación de la cabeza de la serpiente en los controles


*** v1.0 ***
 - Se paso a numpy las listas de numeros, la lista de objetos se dejo como lista de python por la
 comodidad
 - Se arreglo el error de los numeros impares, pero los N pares generan un campo de N-1 porque se incluye
 el borde como el mundo.
 - Se agrego una ventana de victoria al ser largo  (2*n-1)*(2*n-1)-2.
 - Se arreglo la pantalla de game over.
 - Se agrego un update a la posicion de la manzana antes de la iteraciónde la ventana para que 
 esta no se creara en el cuerpo de la serpiente.
 - Se cambio la ventana a una de 800x600

*** v1.1 *** Launch Version
 - Se agregaron comentarios en el codigo para entender, a grandes rasgo, que hace cada funcion y
 cada variable en los tres archivos principales del Juego
 - Se elimino la funcion de comer manzana para integrarla en la funcion de colision, de esa manera se revisa
 una vez la lista de posiciones del cuerpo.