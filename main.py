'''
This code was written to serve as an interface to analyze the submittals for 
the "Comparison of Gd2O3-Bearig BWR Fuel Rods"  benchmark for for a bechmark for: 
The Expert Group on Used Nuclear Fuel (EGUNF) of the Working Party on 
Nuclear Criticality Safety (WPNCS) under the Nuclear Science Committee 
(NSC) of the Organisation for Economic Co-operation and Development/Nuclear
Energy Agency (OECD/NEA)

This interface successfully run using:
Bokeh 0.12.6*
Python 3.6.1

*This is the latest Bokeh version and is required for full functionality of the interface
(Use: "pip install bokeh" to download latest version)


Interface written by Shadi Ghrayeb of the U.S. Nuclear Regulatory Commission (USNRC) in collobration
with Oak Ridge National Laboratory (ORNL)

contact: 
Shadi Ghrayeb
Shadi.Ghrayeb@nrc.gov / ghrays@gmail.com

ORNL: 
Ian Gauld (gauldi@ornl.gov)
William "BJ" Marshall (marshallwj@ornl.gov)

Easiest way to run this interface is to download ANACONDA from www.continuum.io/downloads
Open a terminal to the directory where this file exists and enter following command: 
    
    bokeh serve --show main.py
    
After entering the above command a browser should appear displaying the interface using the following url: 
    
    http://localhost:5006/main
    
When running on windows machine there have been issues using Internet Explorer browser. Try alternative browsers by 
entering the above url into Chrome, FireFox, etc. 

'''
import pandas as pd
import sys, os, csv
import pprint
import numpy as np
import xlsxwriter, itertools
from collections import defaultdict

from bokeh.layouts import row, widgetbox, column, gridplot, layout, column
from bokeh.models import Select, MultiSelect, ColumnDataSource, HoverTool, CustomJS
from bokeh.palettes import Spectral11
from bokeh.palettes import Category20_20 as palette

from bokeh.plotting import curdoc, figure
from bokeh.charts import TimeSeries, Scatter, marker
from os.path import dirname, join
from bokeh.models.widgets import  Button, DataTable, TableColumn

global top500

# the colors used for the plots are stored in list named top500, 20 different colors are repeated
# for the first 500 allocations. Any future plot with greater than 500 lines may produce an error. 
colors = itertools.cycle(palette)
top500 = list(itertools.islice(colors, 500))


voidz = list()
files = list()                         
data = {}     
mass_spec = defaultdict(list)    

master_dict = {} 
# the participants.xlsx is where all the data is read into the code. The highlighted colors in that 
# excel file are the required entries. The headers highlighted in yellow will be displayed on the interface (try to minimize as much as possible so that it can fit to screen)
xlsx = pd.ExcelFile('participants.xlsx')
participant_file = xlsx.parse(xlsx.sheet_names[0])
data_table_source = ColumnDataSource(dict(participant_file))
files = [file for file in data_table_source.data['Filename']]

kinf_source = ColumnDataSource(data=dict(x=[], y = [], Legend = [], color = []))          # this is source data for plotting the kinf plot (top left)
actinide_source = ColumnDataSource(data=dict(x=[], y = [], Legend = [], color = []))      # this is source data for plotting the actinide plot (top right)
fission_prdts_source = ColumnDataSource(data=dict(x=[], y = [], Legend = [], color = [])) # this is source data for plotting the fission plot (bottom left)
Gd_istps_source = ColumnDataSource(data=dict(x=[], y = [], Legend = [], color = []))      # this is source data for plotting the Gd isotopes plot (bottom right)
active_DataTable_files = ColumnDataSource(data=dict(files = []))

# here the figures are defined before the data is actually defined
# p is k-inf plot (top left), p2=actinide plot (top right), p3=fission product plot (bottom left), p4=Gd isotope plot (bottom right)
p = figure(width=500, height=400, title='k-inf', x_axis_label='Burnup [GWd/MTU]', y_axis_label='k-inf')
p.multi_line(xs='x', ys='y', line_color = 'color', source=kinf_source)
p.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))
p2 = figure(width=500, height=400, title='Actinides', x_axis_label='Burnup [GWd/MTU]', y_axis_label='[a/b-cm]')
p2.multi_line(xs='x', ys='y', line_color = 'color', source=actinide_source)
p2.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))
p3 = figure(width=500, height=400, title='Fission Products', x_axis_label='Burnup [GWd/MTU]', y_axis_label='[a/b-cm]')
p3.multi_line(xs='x', ys='y', line_color = 'color', source=fission_prdts_source)
p3.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))
p4 = figure(width=500, height=400, title='Gd Isotopes', x_axis_label='Burnup [GWd/MTU]', y_axis_label='[a/b-cm]')
p4.multi_line(xs='x', ys='y', line_color = 'color', source=Gd_istps_source)
p4.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
     ('file:', '@Legend'),
     ('Burnup:', '$x'),
     ('k-inf', ' $y'),
     ]))


# this iterates through each file and reads each sheet (Sheets 2,3,4). Python indexing beings with 0, so that's equivalent to sheets 1,2,3. 
# all the data from all the sheets are saved as a dictionary named 'data'
for file in files:
     xls = pd.ExcelFile('data/{}'.format(file))
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
# preparing the DataTable data (top left portion of interface)
#***************************************************
current = participant_file
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

# Once user makes selections/changes to DataTable this function is called and updated
def table_select_callback(attr, old, new):
    selected_row = new['1d']['indices']
    files = current['Filename'][selected_row] 
    files_selected = [z for z in files]
    active_DataTable_files.data = dict(
                       files = files_selected,
                       )
    update_all()       # once a file name is selected/changed this is called this calls all functions to update plots

# Once user makes selection/changes regarding void value this function is called
def kinf_figure():
    mass_spec.clear()   
    files_selected = [z for z in active_DataTable_files.data['files']]
    voidz = [z for z in voids.value]
    for x in range(0, len(files_selected)):
        for y in range(0, len(voids.value)):
         mass_spec["x"].append(data[files_selected[x] + '_' + xls.sheet_names[1]]['Burnup'])
         mass_spec["y"].append(data[files_selected[x] + '_' + xls.sheet_names[1]][voidz[y]])
         mass_spec["Legend"].append(files_selected[x] + '_' + voids.value[y])               
    num_kinf_plots = len(files_selected) * len(voids.value)
    mass_spec['kinf_color'] = top500[0:num_kinf_plots]
    return mass_spec

# Once user makes selection/changes regarding actinide to be plotted  this function is called
def actinide_figure():
    mass_spec.clear()
    actinide_axis_map = {
                "0% void": 0,
                "40% void": 40,
                "70% void": 70,
    }    
    files_selected = [z for z in active_DataTable_files.data['files']]
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


# Once user makes selection/changes regarding fission product to be plotted  this function is called
def fission_figure():
    mass_spec.clear()
    actinide_axis_map = {
                "0% void": 0,
                "40% void": 40,
                "70% void": 70,
    }    
    files_selected = [z for z in active_DataTable_files.data['files']]
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
    
 # Once user makes selection/changes regarding Gd isotope to be plotted  or ring this function is called   
def gd_figure():
    mass_spec.clear()
    actinide_axis_map = {
                "0% void": 0,
                "40% void": 40,
                "70% void": 70,
    }    
    files_selected = [z for z in active_DataTable_files.data['files']]
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
        

def update_kinf():
    df = kinf_figure()
    kinf_source.data = dict(
                x  = df['x'],
                y  = df['y'],  
            Legend = df['Legend'],  
            color  = df['kinf_color'],
                      ) 
    xf = pd.DataFrame(df)
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
      
def update_all():
    update_kinf()
    update_actinides()
    update_fission()
    update_gd_istps()


#def printout():

#*****************************************************************
# Below are the widgets that appear in left column of interface 
#*****************************************************************
data_table = DataTable(source = data_table_source, columns = columns, width=300, height=350)
data_table_source.on_change('selected', table_select_callback) 

voids = MultiSelect(title="At what void[s]", value=["0% void"], options=sorted(void_axis_map.keys()))
voids.on_change('value', lambda attr, old, new: update_all())

actinides = MultiSelect(title="Choose Actinide[s]", value=["U-235"], options=open(join(dirname(__file__), 'widget_files/actinides.txt')).read().split())
actinides.on_change('value', lambda attr, old, new: update_actinides())

fission_prdts = MultiSelect(title="Choose Fission Product[s]", value=["Tc-99"], options=open(join(dirname(__file__), 'widget_files/fission_products.txt')).read().split())
fission_prdts.on_change('value', lambda attr, old, new: update_fission())

gd_istps = MultiSelect(title="Choose Gadolinium Isotope[s]", value=["Gd-154"], options=open(join(dirname(__file__), 'widget_files/gd_istps.txt')).read().split())
gd_istps.on_change('value', lambda attr, old, new: update_gd_istps())

rings = Select(title="Choose at what ring Gd Isotope[s] are measured", value="1", options=open(join(dirname(__file__), 'widget_files/rings.txt')).read().split())
rings.on_change('value', lambda attr, old, new: update_gd_istps())
#button = Button(label="Download", button_type="success")
#button.on_click(printout)
#*****************************************************************
# End of widgets
#*****************************************************************

controls = [ voids, actinides, rings]
for control in controls:
    control.on_change('value', lambda attr, old, new: update_all())


sizing_mode = 'scale_both'  # 'scale_width' also looks nice with this example
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
# below is the order in which the widgets and plots appear in the interface
l = row(column(widgetbox(data_table), widgetbox(voids, actinides, fission_prdts, gd_istps, rings)), column(p, p3), column(p2, p4)) 
curdoc().add_root(l)
curdoc().title = "OECD Benchmark"
