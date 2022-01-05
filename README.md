# Herramienta para LSB Práctica 2 (Pensado para los directorios de los ratones vehículo)

### Modo de Uso:
- Descargar carpeta y poner donde quieras
- Abrir el archivo 'anaylysis.py' y ver las posibles configuraciones de los nombres de las carpetas por si las tuyas se llaman distinto. También es importante configurar el PATH (variable 'custom_path') de la carpeta donde se encuentran los registros de las patas derecha e izquierda. Por defecto, si pones la carpeta del programa en el mismo directorio que los directorios de los registros funciona directamente sin tocar el PATH.
- Ejecutar el archivo 'analyze.bat' que instalará las dependencias del programa de forma local en la carpeta del programa y luego ejecutará el programa (solo se instalan una vez en al carpeta 'venv'). Este archivo '.bat' solo funciona en Windows, por lo que si se usa en otro dispositivo se tendrá que instalar las dependencias del requirements.txt a mano y ejecutar de la forma tradicional 'python analysis.py'
- El archivo del análisis se guarda siempre en la carpeta <root> (En la carpeta que se haya especificado en la variable 'custom_path' o si no se usará la 'default_path')
Ej: Estructura de carpetas que funciona por defecto:
```
+ <root>
    + LSB-P2-analyzer
        + <venv> (Cuando se instalen las dependencias)
        - analysis.py
        - analyze.bat
        - requirements.txt
    + pata-derecha_tratados
        + basales
            - <Ficheros.txt de cada raton (da igual el nombre)>
            - ...
        + 72-horas
            - ...
        + 2-semanas
            - ...
    + pata-izquierda_tratados
        <igual que el de pata derecha> 
        ...
    - <last_analysis.txt> (Cuando se realize algún análisis se guardará aquí)
```  
Ejemplo del archivo creado tras el analisis:
```
 + Analysing '<path>'
 => pata-derecha_tratados
 -> basales
 + HI:
╒═══════════════════════════════╤══════════════════════╤════════════════╤═════════════════╕
│ Raton                         │  Amplitud mean (uV)  │  Latency (ms)  │  Absolute area  │
╞═══════════════════════════════╪══════════════════════╪════════════════╪═════════════════╡
│ raton-1_vehiculo_basal_PD.txt │       0.285298       │    17.0898     │     982.796     │
├───────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-2_vehiculo_basal_PD.txt │       0.264627       │    21.3623     │     2966.88     │
├───────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-3_vehiculo_basal_PD.txt │      -0.240643       │    52.4292     │     470.299     │
├───────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-4_vehiculo_basal_PD.txt │      -0.342778       │    27.0386     │     921.833     │
╘═══════════════════════════════╧══════════════════════╧════════════════╧═════════════════╛
 + HD:
╒═══════════════════════════════╤══════════════════════╤════════════════╤═════════════════╕
│ Raton                         │  Amplitud mean (uV)  │  Latency (ms)  │  Absolute area  │
╞═══════════════════════════════╪══════════════════════╪════════════════╪═════════════════╡
│ raton-1_vehiculo_basal_PD.txt │       -1.78488       │     12.085     │     1031.94     │
├───────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-2_vehiculo_basal_PD.txt │       -1.67319       │    23.6206     │     906.977     │
├───────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-3_vehiculo_basal_PD.txt │       1.36438        │    42.5415     │     693.883     │
├───────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-4_vehiculo_basal_PD.txt │       -1.26201       │     22.522     │     580.783     │
╘═══════════════════════════════╧══════════════════════╧════════════════╧═════════════════╛
 -> 72-horas
 + HI:
╒══════════════════════════════════╤══════════════════════╤════════════════╤═════════════════╕
│ Raton                            │  Amplitud mean (uV)  │  Latency (ms)  │  Absolute area  │
╞══════════════════════════════════╪══════════════════════╪════════════════╪═════════════════╡
│ raton-1_vehiculo_72-horas_PD.txt │       -5.38692       │    50.4761     │     1105.97     │
├──────────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-2_vehiculo_72-horas_PD.txt │        -1.63         │    18.4326     │     2707.26     │
├──────────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-3_vehiculo_72-horas_PD.txt │       1.12222        │    21.9727     │     731.655     │
├──────────────────────────────────┼──────────────────────┼────────────────┼─────────────────┤
│ raton-4_vehiculo_72-horas_PD.txt │      0.0801913       │    20.0195     │     1029.35     │
╘══════════════════════════════════╧══════════════════════╧════════════════╧═════════════════╛

...
```

