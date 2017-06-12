import pandas as pd
import sys, os, csv
import xlsxwriter
from collections import defaultdict

from bokeh.layouts import row, widgetbox, column, gridplot, layout, column
from bokeh.models import Select, MultiSelect, ColumnDataSource, HoverTool, CustomJS
from bokeh.palettes import Spectral11
from bokeh.palettes import Colorblind8
from bokeh.plotting import curdoc, figure
from bokeh.charts import TimeSeries, Scatter, marker
from os.path import dirname, join
from bokeh.models import HoverTool
from bokeh.models.widgets import  Button, DataTable, TableColumn


data_dict = {}   
new_dict = {}  
mass_spec = defaultdict(list)  

void_axis_map = {
    "0% void": "0% void",
    "40% void": "40% void",
    "70% void": "70% void",
}

xlsx = pd.ExcelFile('salary_data.xlsx')
dfxx = xlsx.parse(xlsx.sheet_names[0])
data_table_source = ColumnDataSource(dict(dfxx))

files = [file for file in data_table_source.data['Filename']]





source = ColumnDataSource(data=dict(x=[], y=[], Legend = [], x_Actinide = [], y_Actinide=[], Actinide_Legend=[],x_FPs = [], y_FPs=[], FPs_Legend=[], x_Gd=[], y_Gd=[], Gd_Legend=[]))
source2 = ColumnDataSource(data=dict(files = []))

p = figure(width=400, height=400, title='k-inf', x_axis_label='Burnup', y_axis_label='k-inf')
p.multi_line(xs='x', ys='y', 
             source=source)
p.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))


# this iterates through each file and reads each sheet (Sheets 2,3,4). Python indexing beings with 0, so that's sheets 1,2,3. 
# the restuls are saved as a dictionary
for file in files:
     xls = pd.ExcelFile(file)
     dfx1 = xls.parse(xls.sheet_names[1], parse_cols=3 )
     dfx2 = xls.parse(xls.sheet_names[2])
     dfx3 = xls.parse(xls.sheet_names[3])
     dfx4 = xls.parse(xls.sheet_names[4])
     data = dfx1.to_dict() 
     data2 = dfx2.to_dict()
     data3 = dfx3.to_dict()
     data4 = dfx4.to_dict()
     data_dict[file + '_' + 'k-inf'    ] = data 
     data_dict[file + '_' + 'Actinides'] = data2 
     data_dict[file + '_' + 'FPs'      ] = data3 
     data_dict[file + '_' + 'Gd'       ] = data4 

# converting dictionary  to dataframe
#master_data is the data frame contains ALL the data. 
newdict = {(k1, k2):v2 for k1,v1 in data_dict.items() \
                       for k2,v2 in data_dict[k1].items()}
xxs = pd.DataFrame([newdict[i] for i in sorted(newdict)],
                  index=pd.MultiIndex.from_tuples([i for i in sorted(newdict.keys())]))  
master_data = xxs.transpose()



current = dfxx
data_table_source.data = {
                              'code'   : current.Code,
                              'xs_lib' : current.Library,
                              'Institute' : current.Institute,
                              'filename'  : current.Filename,
                              }   

columns = [
           TableColumn(field="code", title = "Code"),
           TableColumn(field="xs_lib", title = "XS Library"),
           TableColumn(field="Institute", title="Institute"),
           TableColumn(field="filename", title="filename")
           ]



def table_select_callback(attr, old, new):
    selected_row = new['1d']['indices']
    files = dfxx['Filename'][selected_row] 
    files_selected = [z for z in files]
    source2.data = dict(
                       files = files_selected,
                       )
    update()



def update():
    files_selected = [z for z in source2.data['files']]
    actinide_axis_map = {
                "0% void": 0,
                "40% void": 40,
                "70% void": 70,
    }
    voidz = [z for z in voids.value]
    for x in range(0, len(files_selected)): 
      for y in range(0, len(voids.value)):
             vary = files_selected[x] + '_' + voids.value[y]
             mass_spec["x"].append(master_data[files_selected[x] + '_' + xls.sheet_names[1]]['Burnup'])
             mass_spec["y"].append(master_data[files_selected[x] + '_' + xls.sheet_names[1]][voidz[y]])
             mass_spec["Legend"].append(files_selected[x] + '_' + voids.value[y])
    df = mass_spec
    source.data = dict(
                x = df['x'],
                y = df['y'],  
            Legend = df['Legend'],  
                      )     
    df.clear()

    
data_table = DataTable(source = data_table_source, columns = columns, width=300, height=100)
data_table_source.on_change('selected', table_select_callback) 

voids = MultiSelect(title="At what void[s]", value=["0% void"], options=sorted(void_axis_map.keys()))
voids.on_change('value', lambda attr, old, new: update())

#controls = [voids]
#for control in controls:
#    control.on_change('value', lambda attr, old, new: update())

   
sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example
#inputs = widgetbox(voids, sizing_mode=sizing_mode)
l = row( column(widgetbox(data_table), widgetbox(voids)), p)
curdoc().add_root(l)
curdoc().title = "OECD Benchmark"
