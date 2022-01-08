# Herramienta para LSB Práctica 2

Se requiere python 3.8 o superior (puede que python 3.7 también funcione pero no se ha probado)

### Modo de Uso:
- Descargar carpeta y poner donde quieras
- Abrir el archivo 'anaylysis.py' y ver las posibles configuraciones de los nombres de las carpetas por si las tuyas se llaman distinto. También es importante configurar el PATH (variable 'custom_path') de la carpeta donde se encuentran los registros de las patas derecha e izquierda de los ratones tratados y vehiculo (no tratados). Por defecto, si pones la carpeta del programa en el mismo directorio que los directorios de los registros funciona directamente sin tocar el PATH.
- Ejecutar el archivo 'analyze.bat' que instalará las dependencias del programa de forma local en la carpeta del programa y luego ejecutará el programa (solo se instalan una vez en al carpeta 'venv'). Este archivo '.bat' solo funciona en Windows, por lo que si se usa en otro dispositivo se tendrá que instalar las dependencias del requirements.txt a mano y ejecutar de la forma tradicional 'python analysis.py' o 'python3 analysis.py (Linux)'
- Los archivos del análisis se guardan siempre en la carpeta <root> (En la carpeta que se haya especificado en la variable 'custom_path' o si no se usará la 'default_path')
Ej: Estructura de carpetas que funciona por defecto:
```
+ <root>
    + LSB-P2-analyzer
        + <venv> (Cuando se instalen las dependencias)
        - analysis.py
        - analyze.bat
        - requirements.txt
    + pata-derecha_no-tratados
        + basales
            - <Ficheros.txt de cada raton (da igual el nombre)>
            - ...
        + 72-horas
            - ...
        + 2-semanas
            - ...
    + pata-izquierda_no-tratados
        <igual que el de pata derecha> 
        ...
    + pata-izquierda_tratados
        ...
    + pata-derecha_tratados
        ...
    - <__analysis__> (Cuando se realize algún análisis se guardará aquí)
```  
El programa realiza un analisis completo de los datos, creando un archivo .txt con toda la información del análisis y varios archivos excel rellenados con los datos y alguna que otra estadística. También se crean otras carpetas con otros análisis como las imágenes de la correlación cruzada, los datos filtrados ...
Ejemplo del archivo .txt creado tras el analisis:
```
+ Analysing '<path>'
 => pata-derecha_no-tratados
 -> basales
╒═══════════════════════════════╤═════════════════════════╤═════════════════════════╤═══════════════════╤═══════════════════╤════════════════════╤════════════════════╤═══════════════════════╕
│ Raton                         │  Amplitud mean (uV) HD  │  Amplitud mean (uV) HI  │  Latency (ms) HD  │  Latency (ms) HI  │  Absolute area HD  │  Absolute area HI  │ Pearson Correlation   │
╞═══════════════════════════════╪═════════════════════════╪═════════════════════════╪═══════════════════╪═══════════════════╪════════════════════╪════════════════════╪═══════════════════════╡
│ raton-1_vehiculo_basal_PD.txt │        0.251984         │        -1.91204         │      17.1509      │      18.5547      │      978.466       │      1019.95       │ R=-0.33099668 | P=0.0 │
├───────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┼───────────────────────┤
│ raton-2_vehiculo_basal_PD.txt │        -0.900935        │        -1.76338         │      21.3623      │      18.8599      │      3093.39       │      919.465       │ R=0.19634771 | P=0.0  │
├───────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┼───────────────────────┤
│ raton-3_vehiculo_basal_PD.txt │        -0.360253        │         1.32357         │      31.1279      │      22.4609      │      484.967       │      695.885       │ R=0.26605283 | P=0.0  │
├───────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┼───────────────────────┤
│ raton-4_vehiculo_basal_PD.txt │        -0.422226        │        -1.30541         │      45.9595      │      39.2456      │      932.041       │      570.129       │ R=0.79699274 | P=0.0  │
╘═══════════════════════════════╧═════════════════════════╧═════════════════════════╧═══════════════════╧═══════════════════╧════════════════════╧════════════════════╧═══════════════════════╛
 -> 72-horas
╒══════════════════════════════════╤═════════════════════════╤═════════════════════════╤═══════════════════╤═══════════════════╤════════════════════╤════════════════════╕
│ Raton                            │  Amplitud mean (uV) HD  │  Amplitud mean (uV) HI  │  Latency (ms) HD  │  Latency (ms) HI  │  Absolute area HD  │  Absolute area HI  │
╞══════════════════════════════════╪═════════════════════════╪═════════════════════════╪═══════════════════╪═══════════════════╪════════════════════╪════════════════════╡
│ raton-1_vehiculo_72-horas_PD.txt │       0.00707006        │       -0.0854647        │      20.9961      │      24.231       │      1639.31       │      2361.01       │
├──────────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┤
│ raton-2_vehiculo_72-horas_PD.txt │        -2.20442         │        -1.64111         │      18.4326      │      16.1743      │      2652.94       │      1175.63       │
├──────────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┤
│ raton-3_vehiculo_72-horas_PD.txt │        0.803767         │        -0.169551        │      33.8745      │      24.9634      │      762.119       │      595.708       │
├──────────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┤
│ raton-4_vehiculo_72-horas_PD.txt │       -0.0800966        │        0.161509         │      20.0195      │      30.7617      │      993.533       │      1006.59       │
╘══════════════════════════════════╧═════════════════════════╧═════════════════════════╧═══════════════════╧═══════════════════╧════════════════════╧════════════════════╛
 -> 2-semanas
╒═══════════════════════════════════╤═════════════════════════╤═════════════════════════╤═══════════════════╤═══════════════════╤════════════════════╤════════════════════╕
│ Raton                             │  Amplitud mean (uV) HD  │  Amplitud mean (uV) HI  │  Latency (ms) HD  │  Latency (ms) HI  │  Absolute area HD  │  Absolute area HI  │
╞═══════════════════════════════════╪═════════════════════════╪═════════════════════════╪═══════════════════╪═══════════════════╪════════════════════╪════════════════════╡
│ raton-1_vehiculo_2-semanas_PD.txt │         2.28452         │        -0.211824        │      25.4517      │      30.5786      │      1092.92       │      1178.84       │
├───────────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┤
│ raton-2_vehiculo_2-semanas_PD.txt │         2.30826         │         1.13552         │      20.6909      │      18.1274      │      2074.76       │      945.997       │
├───────────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┤
│ raton-3_vehiculo_2-semanas_PD.txt │         1.02629         │        0.174464         │      35.8276      │      27.1606      │      758.438       │       685.56       │
├───────────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┤
│ raton-4_vehiculo_2-semanas_PD.txt │        -2.48452         │        -1.57578         │      18.5547      │      33.3252      │       1122.6       │      822.957       │
╘═══════════════════════════════════╧═════════════════════════╧═════════════════════════╧═══════════════════╧═══════════════════╧════════════════════╧════════════════════╛
 => pata-derecha_tratados
 -> basales
╒══════════════════════════════╤═════════════════════════╤═════════════════════════╤═══════════════════╤═══════════════════╤════════════════════╤════════════════════╤═══════════════════════╕
│ Raton                        │  Amplitud mean (uV) HD  │  Amplitud mean (uV) HI  │  Latency (ms) HD  │  Latency (ms) HI  │  Absolute area HD  │  Absolute area HI  │ Pearson Correlation   │
╞══════════════════════════════╪═════════════════════════╪═════════════════════════╪═══════════════════╪═══════════════════╪════════════════════╪════════════════════╪═══════════════════════╡
│ raton-1_tratado_basal_PD.txt │        -1.03962         │       -0.0730489        │      23.1323      │      30.5176      │      1141.56       │      1592.85       │ R=0.23579851 | P=0.0  │
├──────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┼───────────────────────┤
│ raton-2_tratado_basal_PD.txt │        -0.861124        │        0.420578         │      21.0571      │      35.4004      │      1150.16       │      1238.55       │ R=-0.75571583 | P=0.0 │
├──────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┼───────────────────────┤
│ raton-3_tratado_basal_PD.txt │        -0.527559        │         1.27758         │      22.7661      │      25.0854      │      1733.79       │      1605.58       │ R=-0.88461992 | P=0.0 │
├──────────────────────────────┼─────────────────────────┼─────────────────────────┼───────────────────┼───────────────────┼────────────────────┼────────────────────┼───────────────────────┤
│ raton-4_tratado_basal_PD.txt │        -0.773486        │        0.967319         │      19.4092      │      40.4663      │      490.007       │      1378.08       │ R=0.28522314 | P=0.0  │
╘══════════════════════════════╧═════════════════════════╧═════════════════════════╧═══════════════════╧═══════════════════╧════════════════════╧════════════════════╧═══════════════════════╛
...
```

