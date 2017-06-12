import pandas as pd
import sys, os, csv
import xlsxwriter, itertools
from collections import defaultdict

from bokeh.layouts import row, widgetbox, column, gridplot, layout, column
from bokeh.models import Select, MultiSelect, ColumnDataSource, HoverTool, CustomJS
from bokeh.palettes import Spectral11
from bokeh.palettes import Colorblind8, Category10, viridis
from bokeh.palettes import Category20_20 as palette

from bokeh.plotting import curdoc, figure
from bokeh.charts import TimeSeries, Scatter, marker
from os.path import dirname, join
from bokeh.models import HoverTool
from bokeh.models.widgets import  Button, DataTable, TableColumn

global top500

colors = itertools.cycle(palette)
top500 = list(itertools.islice(colors, 500))



#***************************************************

voidz = list()
files = list()                         
data = {}   
new_dict = {}    
sourcex = {}    
mass_spec = defaultdict(list)    
master_dict = {} 
xlsx = pd.ExcelFile('participants.xlsx')
dfxx = xlsx.parse(xlsx.sheet_names[0])
data_table_source = ColumnDataSource(dict(dfxx))
files = [file for file in data_table_source.data['Filename']]


#source = ColumnDataSource(data=dict(x=[], y=[], Legend = [], x_Actinide = [], y_Actinide=[], Actinide_Legend=[],x_FPs = [], y_FPs=[], FPs_Legend=[], x_Gd=[], y_Gd=[], Gd_Legend=[]))
kinf_source = ColumnDataSource(data=dict(x=[], y = [], Legend = [], color = []))
actinide_source = ColumnDataSource(data=dict(x=[], y = [], Legend = [], color = []))
fission_prdts_source = ColumnDataSource(data=dict(x=[], y = [], Legend = [], color = []))
Gd_istps_source = ColumnDataSource(data=dict(x=[], y = [], Legend = [], color = []))
source2 = ColumnDataSource(data=dict(files = []))

p = figure(width=500, height=400, title='k-inf', x_axis_label='Burnup [GWd/MTU]', y_axis_label='k-inf')
p.multi_line(xs='x', ys='y', line_color = 'color',
             source=kinf_source)
p.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))
p2 = figure(width=500, height=400, title='Actinides', x_axis_label='Burnup [GWd/MTU]', y_axis_label='[a/b-cm]')
p2.multi_line(xs='x', ys='y', line_color = 'color',
             source=actinide_source)
p2.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))
p3 = figure(width=500, height=400, title='Fission Products', x_axis_label='Burnup [GWd/MTU]', y_axis_label='[a/b-cm]')
p3.multi_line(xs='x', ys='y', line_color = 'color',
             source=fission_prdts_source)
p3.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))
p4 = figure(width=500, height=400, title='Gd Isotopes', x_axis_label='Burnup [GWd/MTU]', y_axis_label='[a/b-cm]')
p4.multi_line(xs='x', ys='y', line_color = 'color',
             source=Gd_istps_source)
p4.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))


# this iterates through each file and reads each sheet (Sheets 2,3,4). Python indexing beings with 0, so that's sheets 1,2,3. 
# the restuls are saved as a dictionary
for file in files:
     xls = pd.ExcelFile(file)
     dfx1 = xls.parse(xls.sheet_names[1], parse_cols=3, parse_rows=62 )
# following two lines, when uncommented, prints the Burnup of peak reactivity at maximum X% void
#     xxy = pd.DataFrame.from_dict(dfx1)
#     print(file, xxy.loc[ xxy['70% void'] == max(xxy['70% void']), ['Burnup', '70% void']].values)
#**********
     dfx2 = xls.parse(xls.sheet_names[2])
     dfx3 = xls.parse(xls.sheet_names[3])
     dfx4 = xls.parse(xls.sheet_names[4])
     data[file + '_' + 'k-inf'    ] = dfx1
     data[file + '_' + 'Actinides'] = dfx2 
     data[file + '_' + 'FPs'      ] = dfx3
     data[file + '_' + 'Gd'       ] = dfx4

void_axis_map = {
    "0% void": "0% void",
    "40% void": "40% void",
    "70% void": "70% void",
}


#*************************************************** 

current = dfxx
data_table_source.data = {
                              'code'   : current.Code,
                              'xs_lib' : current.Library,
                              'Institute' : current.Institute,
                              'filename'  : current.Filename,
                              'no_grps'   : current.no_grps,
                              }   

columns = [
           TableColumn(field="code", title = "Code"),
           TableColumn(field="xs_lib", title = "XS Library"),
           TableColumn(field="no_grps", title="# Groups"),
           TableColumn(field="Institute", title="Institute"),
           ]


def table_select_callback(attr, old, new):
    selected_row = new['1d']['indices']
    files = dfxx['Filename'][selected_row] 
    files_selected = [z for z in files]
    source2.data = dict(
                       files = files_selected,
                       )
    update_all()

def kinf_figure():
    mass_spec.clear()   
    files_selected = [z for z in source2.data['files']]
    voidz = [z for z in voids.value]
    for x in range(0, len(files_selected)):
        for y in range(0, len(voids.value)):
         mass_spec["x"].append(data[files_selected[x] + '_' + xls.sheet_names[1]]['Burnup'])
         mass_spec["y"].append(data[files_selected[x] + '_' + xls.sheet_names[1]][voidz[y]])
         mass_spec["Legend"].append(files_selected[x] + '_' + voids.value[y])               
    num_kinf_plots = len(files_selected) * len(voids.value)
    mass_spec['kinf_color'] = top500[0:num_kinf_plots]
    return mass_spec


def fission_figure():
    mass_spec.clear()
    actinide_axis_map = {
                "0% void": 0,
                "40% void": 40,
                "70% void": 70,
    }    
    files_selected = [z for z in source2.data['files']]
    voidz = [z for z in voids.value]
    for x in range(0, len(files_selected)):
        for y in range(0, len(voids.value)):
         for z in range(0, len(fission_prdts.value)):
             try: 
                 mass_spec["y_FPs"].append(data[files_selected[x] + '_' + 'FPs'][fission_prdts.value[z]][(data[files_selected[x] + '_' + 'FPs']['Void Fraction'] == actinide_axis_map[voids.value[y]]) & (data[files_selected[x] + '_' + 'FPs']['Cooling Time'] == 0 ) ])
                 mass_spec["x_FPs"].append(data[files_selected[x] + '_' + 'FPs']['Burnup'][(data[files_selected[x] + '_' + 'FPs']['Void Fraction'] == actinide_axis_map[voids.value[y]]) & (data[files_selected[x] + '_' + 'FPs']['Cooling Time'] == 0 ) ])
                 mass_spec["FPs_Legend"].append(files_selected[x] + '_' + fission_prdts.value[z] +'_' + voids.value[y])
             except KeyError:
                print("WARNING:", fission_prdts.value[z], "data missing from", files_selected[x])                 
    num_fission_prdts_plots = len(files_selected) * len(voids.value) * len(fission_prdts.value)
    mass_spec['fission_prdts_color'] = top500[0:num_fission_prdts_plots]
    return mass_spec
    
    
def gd_figure():
    mass_spec.clear()
    actinide_axis_map = {
                "0% void": 0,
                "40% void": 40,
                "70% void": 70,
    }    
    files_selected = [z for z in source2.data['files']]
    voidz = [z for z in voids.value]
    for x in range(0, len(files_selected)):
        for y in range(0, len(voids.value)):
         for z in range(0, len(gd_istps.value)):
             try:             
                 mass_spec["y_Gd"].append(data[files_selected[x] + '_' + 'Gd'][gd_istps.value[z]][(data[files_selected[x] + '_' + 'Gd']['Void Fraction'] == actinide_axis_map[voids.value[y]]) & (data[files_selected[x] + '_' + 'Gd']['Cooling Time'] == 0 ) & (data[files_selected[x] + '_' + 'Gd']['Ring'] == int(rings.value)) ])
                 mass_spec["x_Gd"].append(data[files_selected[x] + '_' + 'Gd']['Burnup'][(data[files_selected[x] + '_' + 'Gd']['Void Fraction'] == actinide_axis_map[voids.value[y]]) & (data[files_selected[x] + '_' + 'Gd']['Cooling Time'] == 0 ) & (data[files_selected[x] + '_' + 'Gd']['Ring'] == int(rings.value)) ])
                 mass_spec["Gd_Legend"].append(files_selected[x] + '_' + gd_istps.value[z] +'_' + voids.value[y])
             except KeyError:
                print("WARNING:", gd_istps.value[z], "data missing from", files_selected[x])                 
    num_Gd_istps_plots = len(files_selected) * len(voids.value) * len(gd_istps.value)
    mass_spec['Gd_istps_color'] = top500[0:num_Gd_istps_plots]
    return mass_spec
 
def actinide_figure():
    mass_spec.clear()
    actinide_axis_map = {
                "0% void": 0,
                "40% void": 40,
                "70% void": 70,
    }    
    files_selected = [z for z in source2.data['files']]
    voidz = [z for z in voids.value]
    for x in range(0, len(files_selected)):
        for y in range(0, len(voids.value)):
         for z in range(0, len(actinides.value)):
             try: 
                 mass_spec["x_Actinide"].append(data[files_selected[x] + '_' + 'Actinides']['Burnup'][(data[files_selected[x] + '_' + 'Actinides']['Void Fraction'] == actinide_axis_map[voids.value[y]]) & (data[files_selected[x] + '_' + 'Actinides']['Cooling Time'] == 0 ) ])
                 mass_spec["y_Actinide"].append(data[files_selected[x] + '_' + 'Actinides'][actinides.value[z]][(data[files_selected[x] + '_' + 'Actinides']['Void Fraction'] == actinide_axis_map[voids.value[y]]) & (data[files_selected[x] + '_' + 'Actinides']['Cooling Time'] == 0 ) ])
                 mass_spec["Actinide_Legend"].append(files_selected[x] + '_' + actinides.value[z] +'_' + voids.value[y])
             except KeyError:
                 print("WARNING:", actinides.value[z], "data missing from", files_selected[x])            
    num_actinide_plots = len(files_selected) * len(voids.value) * len(actinides.value)
    mass_spec['actinide_color'] = top500[0:num_actinide_plots]
    return mass_spec    
    
    
def update_fission():
    df = fission_figure()    
    fission_prdts_source.data = dict(
                x  = df['x_FPs'],
                y  = df['y_FPs'],  
            Legend = df['FPs_Legend'],  
            color  = df['fission_prdts_color'],
                      ) 
    df.clear()
    return

def update_gd_istps():
    df = gd_figure()
    Gd_istps_source.data = dict(
                x  = df['x_Gd'],
                y  = df['y_Gd'],  
            Legend = df['Gd_Legend'],  
            color  = df['Gd_istps_color'],
                      ) 
    df.clear()
    return

def update_actinides():
    df = actinide_figure()
    actinide_source.data = dict(
                x  = df['x_Actinide'],
                y  = df['y_Actinide'],  
            Legend = df['Actinide_Legend'],  
            color  = df['actinide_color'],
                      ) 
    df.clear()
    return

def update_kinf():
    df = kinf_figure()
    kinf_source.data = dict(
                x  = df['x'],
                y  = df['y'],  
            Legend = df['Legend'],  
            color  = df['kinf_color'],
                      ) 
    xf = pd.DataFrame(df)
    print(xf)
    xf.to_csv('myfile.csv', cols=['x', 'y'], sep='\n', index=False, header=False)
    df.clear()
    return    
      
def update_all():
    update_kinf()
    update_actinides()
    update_fission()
    update_gd_istps()
    
def printout():
   print('hi')


#    pd.DataFrame(df).T.reset_index().to_csv('myfile.csv', header=False, index=False)


    
#******************************************
data_table = DataTable(source = data_table_source, columns = columns, width=300, height=350, selectable = True)
data_table_source.on_change('selected', table_select_callback) 

voids = MultiSelect(title="At what void[s]", value=["0% void"], options=sorted(void_axis_map.keys()))
voids.on_change('value', lambda attr, old, new: update_all())

actinides = MultiSelect(title="Choose Actinide[s]", value=["U-235"], options=open(join(dirname(__file__), 'actinides.txt')).read().split())
actinides.on_change('value', lambda attr, old, new: update_actinides())

fission_prdts = MultiSelect(title="Choose Fission Product[s]", value=["Tc-99"], options=open(join(dirname(__file__), 'fission_products.txt')).read().split())
fission_prdts.on_change('value', lambda attr, old, new: update_fission())

gd_istps = MultiSelect(title="Choose Gadolinium Isotope[s]", value=["Gd-154"], options=open(join(dirname(__file__), 'gd_istps.txt')).read().split())
gd_istps.on_change('value', lambda attr, old, new: update_gd_istps())

rings = Select(title="Choose at what ring Gd Isotope[s] are measured", value="1", options=open(join(dirname(__file__), 'rings.txt')).read().split())
rings.on_change('value', lambda attr, old, new: update_gd_istps())
button = Button(label="Download", button_type="success")
button.on_click(printout)
#******************************************

controls = [ voids, actinides, rings]
for control in controls:
    control.on_change('value', lambda attr, old, new: update_all())


sizing_mode = 'scale_both'  # 'scale_width' also looks nice with this example
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = row(column(widgetbox(data_table), widgetbox(voids, actinides, fission_prdts, gd_istps, rings), widgetbox(button)), column(p, p3), column(p2, p4)) 
curdoc().add_root(l)
curdoc().title = "OECD Benchmark"
