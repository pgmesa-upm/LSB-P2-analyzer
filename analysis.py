
# Built-in Modules
import os
import sys
import csv
from pathlib import Path

# Dependencies
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

default_path = '../'
# ------------------------- Custom Settings -------------------------
# -------------------------------------------------------------------
custom_path = None
analisis_fname = 'last_analisis.txt'
rigth_paw_dir = 'pata-derecha_no-tratados'; left_paw_dir = 'pata-izquierda_no-tratados'
dir_basales = 'basales'; dir_72horas = '72-horas'; dir_2semanas = '2-semanas'
# Stat headers
mouse_header = "Raton"
amplitud_header = "Amplitud mean (uV)"
latency_header = "Latency (ms)"
area_header = "Absolute area"
# -------------------------------------------------------------------
# -------------------------------------------------------------------

if custom_path is not None:
    path = Path(custom_path).resolve()
else:
    path = Path(default_path).resolve()

paws_dir_names = [rigth_paw_dir, left_paw_dir]
tgroups = [dir_basales, dir_72horas, dir_2semanas]
stat_headers = [mouse_header, amplitud_header, latency_header, area_header]

reset_log = True

def main():
    print(f"[%] Analizando archivos de '{path}'")
    log(f" + Analysing '{path}'")
    analisis = {}
    for paw in paws_dir_names:
        log(f" => {paw}")
        analisis[paw] = {}
        for grp in tgroups:
            log(f" -> {grp}")
            analisis[paw][grp] = {}
            grp_path = path/paw/grp
            files = [name for name in os.listdir(grp_path) if name.endswith('.txt')]
            table_hd = [stat_headers]; table_hi = [stat_headers]
            for fname in files:
                print(f"Analizando => '{fname}'...")
                t = []; hd = []; hi = []
                with open(grp_path/fname, 'r') as file:
                    reader = csv.reader(file, delimiter='\t')
                    for i, line in enumerate(reader):
                        if i == 0: continue
                        t.append(float(line[0])); hd.append(float(line[1])); hi.append(float(line[2]))
                t_hd, hd, t_hi, hi = filt(t, hd, hi)
                # HD
                hd_stats = calc_stats(t_hd, hd)
                hd_stats.insert(0, fname)
                table_hd.append(hd_stats)
                plt.plot(t_hd, hd)
                # HI
                hi_stats = calc_stats(t_hi, hi)
                hi_stats.insert(0, fname)
                table_hi.append(hi_stats)
                plt.plot(t_hi, hi)
                if '-s' in sys.argv:
                    plt.show()
            log(" + HI:")
            log(tabulate(table_hd, headers='firstrow', tablefmt='fancy_grid', numalign='center'))
            log(" + HD:")
            log(tabulate(table_hi, headers='firstrow', tablefmt='fancy_grid', numalign='center'))
    print("[%] Fin del analisis")
    
def log(msg:str):
    global reset_log
    mode = 'ab'
    if reset_log:
        mode = 'wb'; reset_log = False
    with open(path/analisis_fname, mode) as file:
        file.write((msg+"\n").encode('utf-8'))

def filt(t, hd, hi):
    end_index_hd = None; changed_polarity = False
    init_polarity = True if hd[0] >= 0 else False
    for i, val in enumerate(hd):
        polarity = True if val >= 0 else False
        if polarity == init_polarity and changed_polarity:
            end_index_hd = i; break
        elif polarity != init_polarity:
            changed_polarity = True
    
    end_index_hi = None; changed_polarity = False
    init_polarity = True if hi[0] >= 0 else False
    for i, val in enumerate(hi):
        polarity = True if val >= 0 else False
        if polarity == init_polarity and changed_polarity:
            end_index_hi = i; break
        elif polarity != init_polarity:
            changed_polarity = True
            
    return t[end_index_hd:], hd[end_index_hd:], t[end_index_hi:], hi[end_index_hi:]    
    

def calc_stats(t:list, array:list) -> list:
    stats = []
    # Amplitud media
    mean = np.mean(array)
    stats.append(round(mean,8))
    # Latencia
    latency = t[array.index(max(array))]
    stats.append(round(latency,8))
    # Area absoluta
    area = np.trapz(np.abs(array), dx=abs(t[1]-t[0]))
    stats.append(round(area,8))
    # Fatan algunas estadísticas
    ...
    return stats

if __name__ == "__main__":
    try:
        print("[%] Program started")
        main()
        print("[%] Program finished successfully")
    except KeyboardInterrupt:
        print("[!] Exit")
        exit(1)
    except Exception as err:
        print(f"[!] Unexpected Error: {err}")