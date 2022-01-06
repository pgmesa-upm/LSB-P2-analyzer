
# Built-in Modules
import os
import sys
import csv
from pathlib import Path
from shutil import copyfile

# Dependencies
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook
import openpyxl

default_path = '../'; excel_template = 'excel_template.xlsx'
# ------------------------- Custom Settings -------------------------
# -------------------------------------------------------------------
custom_path = None
analisis_fname = 'last_analisis.txt'
excel_pd_name = 'stats_vehiculo_PD.xlsx'
excel_pi_name = 'stats_vehiculo_PI.xlsx'
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
    for ipaw, paw in enumerate(paws_dir_names):
        log(f" => {paw}")
        analisis[paw] = {}; gcounter = 0
        for grp in tgroups:
            log(f" -> {grp}")
            analisis[paw][grp] = {}
            grp_path = path/paw/grp
            files = [name for name in os.listdir(grp_path) if name.endswith('.txt')]
            headers = []
            for i, h in enumerate(stat_headers): 
                if i == 0: headers.append(h); continue
                headers.append(h + " HD")
                headers.append(h + " HI")
            table = [headers]
            fcounter = 0
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
                plt.plot(t_hd, hd)
                # HI
                hi_stats = calc_stats(t_hi, hi)
                plt.plot(t_hi, hi)
                # all
                stats = [fname]
                for hd_stat, hi_stat in zip(hd_stats, hi_stats):
                    stats.append(hd_stat)
                    stats.append(hi_stat)
                table.append(stats)
                # Updateamos el excel
                if ipaw == 0:
                    excel_path = path/excel_pd_name
                else: 
                    excel_path = path/excel_pi_name
                if not os.path.exists(excel_path):
                    copyfile(excel_template, excel_path)
                wb = openpyxl.load_workbook(excel_path)
                ws = wb.active
                letters = ['D', 'E', 'F', 'G', 'H', 'I']
                offset = 4; stats.pop(0); counter = fcounter + gcounter
                for i, stat in enumerate(stats):
                    cell = letters[i]+str(counter+offset)
                    ws[cell] = stat
                wb.save(path/excel_path)
                # Argumento para plotear
                if '-s' in sys.argv:
                    plt.show()
                fcounter += 3
            gcounter += 1
            log(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign='center'))
    print(f"[%] Se ha creado '{excel_pd_name}'")
    print(f"[%] Se ha creado '{excel_pi_name}'")
    print(f"[%] Se ha creado '{analisis_fname}'")
    print("[%] Fin del analisis")
    
def log(msg:str):
    global reset_log
    mode = 'ab'
    if reset_log:
        mode = 'wb'; reset_log = False
    with open(path/analisis_fname, mode) as file:
        file.write((msg+"\n").encode('utf-8'))

filt_time = 11 
def filt(t, hd, hi):
    end_index_limit = None;
    for i, time in enumerate(t):
        if time > filt_time:
            end_index_limit = i
            break
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
            
    if t[end_index_hd] > filt_time: end_index_hd = end_index_limit
    if t[end_index_hi] > filt_time: end_index_hi = end_index_limit
            
    return t[end_index_hd:], hd[end_index_hd:], t[end_index_hi:], hi[end_index_hi:]    
    
ampl_threshold = 10 # uV
def calc_stats(t:list, array:list) -> list:
    stats = []
    # Amplitud media
    mean = np.mean(array)
    stats.append(round(mean,8))
    # Latencia
    max_ = max(array); min_ = min(array)
    # print(abs(max_) + abs(min_))
    # if abs(max_) + abs(min_) < ampl_threshold:
    #     latency = 0
    # else:
    if abs(max_) >= abs(min_):
        latency = t[array.index(max_)]
    else:
        latency = t[array.index(min_)]
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