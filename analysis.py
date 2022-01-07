
# Built-in Modules
import os
import sys
import csv
from time import time as get_time
from math import floor
from pathlib import Path
from shutil import copyfile

# Dependencies
from scipy import signal
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook
from openpyxl.chart import ScatterChart, Reference, Series
import openpyxl

default_path = '../'; excel_template = 'excel_template.xlsx'
# ------------------------- Custom Settings -------------------------
# -------------------------------------------------------------------
custom_path = None
# Nombre directorios y archivos creados en el analisis
analysis_fname = 'last_analisis.txt'
analysis_dir_name = '__analysis__'
filt_dir_name = 'filtered_data'
norm_dir_name = 'normalized_data'
xcorr_dir_name = 'cross-correlations'
# -- Excels
excel_nt_pd_name = 'stats_vehiculos_PD.xlsx'
excel_t_pd_name = 'stats_tratados_PD.xlsx'
excel_nt_pi_name = 'stats_vehiculos_PI.xlsx'
excel_t_pi_name = 'stats_tratados_PI.xlsx'
excel_names = [excel_nt_pd_name, excel_t_pd_name, excel_nt_pi_name, excel_t_pi_name]
# Nombre directorios ratones
rigth_paw_dirs = ['pata-derecha_no-tratados', 'pata-derecha_tratados'] 
left_paw_dirs = ['pata-izquierda_no-tratados', 'pata-izquierda_tratados']
dir_basales = 'basales'; dir_72horas = '72-horas'; dir_2semanas = '2-semanas'
# Stat headers
mouse_header = "Raton"
amplitud_header = "Amplitud mean (uV)"
latency_header = "Latency (ms)"
area_header = "Absolute area"
pearson_header = 'Pearson Correlation'
# -------------------------------------------------------------------
# -------------------------------------------------------------------

if custom_path is not None:
    path = Path(custom_path).resolve()
else:
    path = Path(default_path).resolve()

paws_dir_names = rigth_paw_dirs + left_paw_dirs
tgroups = [dir_basales, dir_72horas, dir_2semanas]
stat_headers = [mouse_header, amplitud_header, latency_header, area_header, pearson_header]

reset_log = True

def timer(func):
    """Mide el tiempo que tarda en ejecutarse una funcion en minutos 
    y segundos

    Args:
        func: funcion a ejecutar
    """
    def f(*a, **ka):
        t0 = get_time()
        func(*a,**ka)
        tf = get_time()
        total_secs = round(tf-t0, 2)
        if total_secs < 60:
            print(f"Elapsed time: {total_secs} s")
        else: 
            mins = floor(total_secs/60)
            secs = int(total_secs - mins*60)
            print(f"Elapsed time: {mins} min {secs} s")
    return f

@timer
def main():
    print(f"[%] Analizando archivos de '{path}'")
   
    analysis_path = path/analysis_dir_name
    if not os.path.exists(analysis_path): os.mkdir(analysis_path)
    if not os.path.exists(analysis_path/norm_dir_name): os.mkdir(analysis_path/norm_dir_name)
    if not os.path.exists(analysis_path/filt_dir_name): os.mkdir(analysis_path/filt_dir_name)
    if not os.path.exists(analysis_path/xcorr_dir_name): os.mkdir(analysis_path/xcorr_dir_name)
    for excel in excel_names:
        if os.path.exists(analysis_path/excel): 
            os.remove(analysis_path/excel)
    
    log(f" + Analysing '{path}'")
    
    for ipaw, paw in enumerate(paws_dir_names):
        log(f" => {paw}")
        gcounter = 0
        for grp in tgroups:
            log(f" -> {grp}")
            grp_path = path/paw/grp
            files = [name for name in os.listdir(grp_path) if name.endswith('.txt')]
            headers = []
            for i, h in enumerate(stat_headers): 
                if i == 0: headers.append(h); continue
                if h == pearson_header:
                    if grp == dir_basales:
                        headers.append(h)
                    continue
                headers.append(h + " HD")
                headers.append(h + " HI")   
                
            table = [headers]
            fcounter = 0
            for ifile, fname in enumerate(files):
                print(f"Analizando => '{fname}'...")
                t = []; hd = []; hi = []; txt_headers = [] 
                with open(grp_path/fname, 'r') as file:
                    reader = csv.reader(file, delimiter='\t')
                    for i, line in enumerate(reader):
                        if i == 0: txt_headers.append(line); continue
                        if line[0] == "" or line[1] == "" or line[2] == "": continue
                        t.append(float(line[0])); hd.append(float(line[1])); hi.append(float(line[2]))
                print("   - Filtrando...")
                t, hd, hi = filt(t, hd, hi)
                assert len(t) == len(hd) and len(hd) == len(hi)
                # Guardamos datos filtrados (quitamos los ultimos 11 ms)
                save_data(t, hd, hi, analysis_path/filt_dir_name, f"{paw}/{grp}/{(fname.replace('.', '_filt.'))}", headers=txt_headers)
                print(f"   - Calculando {stat_headers}...")
                # HD
                hd_stats = calc_stats(t, hd)
                if '-s' in sys.argv:
                    plt.plot(t, hd)
                # HI
                hi_stats = calc_stats(t, hi)
                if '-s' in sys.argv:
                    plt.plot(t, hi)
                # all
                stats = [fname]
                for hd_stat, hi_stat in zip(hd_stats, hi_stats):
                    stats.append(hd_stat)
                    stats.append(hi_stat)
                if grp == dir_basales:
                    # Calculamos correlacion de Pearson
                    print("   - Calculando Coeficinete de Pearson...")
                    pearson = np.cov(hd,hi)[0][1]/(np.std(hd)*np.std(hi))
                    stats.append(pearson)
                table.append(stats)
                print(f"   - Actualizando excel...")
                # Updateamos el excel
                excel_path = analysis_path/excel_names[ipaw]
                if not os.path.exists(excel_path):
                    copyfile(excel_template, excel_path)
                wb = openpyxl.load_workbook(excel_path)
                ws = wb.active
                letters = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
                offset = 4; counter = fcounter + gcounter
                for i, stat in enumerate(stats):
                    if i == 0: continue
                    cell = letters[i-1]+str(counter+offset)
                    ws[cell] = stat
                if grp == dir_basales:
                    # Normalizamos la señal
                    print(f"   - Normalizando la señal...")
                    # ¿ norm_hd = normalize(np.array(hd)); norm_hi = normalize(np.array(hi)) ?
                    # assert max(norm_hd) <= 1 and min(norm_hi) >= 0 
                    norm_hd = hd/np.linalg.norm(hd); norm_hi = hi/np.linalg.norm(hi)
                    # Guardamos las normalizaciones
                    save_data(t, norm_hd, norm_hi, analysis_path/norm_dir_name, f"{paw}/{grp}/{(fname.replace('.', '_norm.'))}", headers=txt_headers)
                    # Realizamos la correlacion cruzada entre hemisferios
                    print(f"   - Realizando Correlacion Cruzada...")
                    chart_ws = Workbook.create_sheet(wb, title=f'Correlation-{ifile+1}')
                    xcorr = list(signal.correlate(norm_hd, norm_hi))
                    chart_ws.append(["Lags", "Cross Correlation"])
                    lags = signal.correlation_lags(norm_hd.size, norm_hi.size, mode="full")
                    # Guardmos la imagen
                    plt.plot(lags, xcorr)
                    plt.grid()
                    plt.xlabel("Lags"); plt.ylabel("Cross Correlation")         
                    save_graph(analysis_path/xcorr_dir_name, f"{paw}/{grp}/{(fname.replace('.txt', '_xcorr.png'))}")
                    plt.clf()
                    for lag, val in zip(lags, xcorr):
                        chart_ws.append([lag, val])
                    xvalues = Reference(chart_ws, min_col=1, min_row=2, max_row=len(lags))
                    values = Reference(chart_ws, min_col=2, min_row=2, max_row=len(xcorr))
                    series = Series(values, xvalues)
                    chart = ScatterChart()
                    chart.title = f"Correlacion Cruzada '{fname}'"
                    chart.x_axis.title = "Lags"
                    chart.y_axis.title = "Cross Correlation"
                    chart.series.append(series)
                    chart_ws.add_chart(chart, 'D2')
                wb.save(path/excel_path)
                # Argumento para plotear
                if '-s' in sys.argv:
                    print(f"   - Mostrando Grafica...")
                    plt.show()
                fcounter += 3
            gcounter += 1
            log(tabulate(table, headers='firstrow', tablefmt='fancy_grid', numalign='center'))
    print(f"[%] Se ha creado '/{analysis_fname}'")
    print("[%] Fin del analisis")
    
def log(msg:str):
    global reset_log
    mode = 'ab'
    if reset_log:
        mode = 'wb'; reset_log = False
    with open(path/analysis_dir_name/analysis_fname, mode) as file:
        file.write((msg+"\n").encode('utf-8'))
        
def create_path(dir_base, fname):
    dirs = fname.split("/")
    fname = dirs.pop(len(dirs)-1)
    
    for dir_ in dirs:
        if not os.path.exists(dir_base/dir_):
            os.mkdir(dir_base/dir_)
        dir_base = dir_base/dir_
        
    file_path = dir_base/fname

    return file_path

def save_data(t, hd, hi, dir_base:Path, fname:str, headers:list=None):
    file_path = create_path(dir_base, fname)
    
    with open(file_path, 'w') as file:
        writer = csv.writer(file, delimiter='\t')
        if headers is not None: writer.writerow(*headers)
        for t_val, hd_val, hi_val in zip(t, hd, hi):
            writer.writerow([t_val, hd_val, hi_val])
        
def save_graph(dir_base:Path, fname:str):
    file_path = create_path(dir_base, fname)
    plt.savefig(file_path)

def filt(t, hd, hi, filt_time_ms=10):
    end_index_limit = None;
    for i, time in enumerate(t):
        if time >= filt_time_ms:
            end_index_limit = i
            break         
    return t[end_index_limit:], hd[end_index_limit:], hi[end_index_limit:]    

def normalize(array):
    if type(array) == list: ...
    else:
        # Numpy Array
        return (array - np.min(array))/(np.max(array)-np.min(array))
    
def calc_stats(t:list, array:list) -> list:
    stats = []
    # Amplitud media
    mean = np.mean(array)
    stats.append(round(mean,8))
    # Latencia
    # -- Realizamos un primer filtrado (hasta que la señal no pase de crecer/decrecer 
    # al contrario una vez, no empieza a contar)
    last_val = None; valid_t = None; valid_array = None; tendency = None
    for i, val in enumerate(np.abs(array)):
        if i == 0: last_val = array[0]; continue
        if last_val > val:
            tendency_val = 'decreasing'
        elif last_val < val:
            tendency_val = 'increasing'
        else:
            continue
        if tendency is None:
            tendency = tendency_val
        elif tendency_val != tendency:
            valid_t = t[i:]; valid_array = array[i:]
            break
        last_val = val 
    max_ = max(valid_array); min_ = min(valid_array)
    if abs(max_) >= abs(min_):
        latency = valid_t[valid_array.index(max_)]
    else:
        latency = valid_t[valid_array.index(min_)]
    stats.append(round(latency,8))
    # Area absoluta
    area = np.trapz(np.abs(array), dx=abs(t[1]-t[0]))
    stats.append(round(area,8))
    
    return stats

if __name__ == "__main__":
    try:
        print("[%] Program started")
        main()
        print("[%] Program finished successfully")
    except KeyboardInterrupt:
        print("[!] Exit")
        exit(1)
    # except Exception as err:
    #     print(f"[!] Unexpected Error: {err}")