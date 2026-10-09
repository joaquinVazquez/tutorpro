## Qué es una función
Una función es un bloque de código con nombre que se puede reutilizar. Se define con def: def saludar(): print("Hola"). Para ejecutarla se llama por su nombre: saludar().

## Parámetros y argumentos
Los parámetros son los datos que recibe la función. Ejemplo: def saludar(nombre): print("Hola", nombre). Al llamarla, saludar("Ana"), el valor "Ana" es el argumento.

## Valor de retorno
return devuelve un resultado a quien llamó la función. Ejemplo: def sumar(a, b): return a + b, y luego resultado = sumar(2, 3) deja resultado en 5. Si una función no tiene return, devuelve None. print muestra en pantalla; return entrega el valor.

## Valores por defecto
Un parámetro puede tener un valor por defecto: def saludar(nombre="amigo"). Si se llama saludar() sin argumento, usa "amigo".