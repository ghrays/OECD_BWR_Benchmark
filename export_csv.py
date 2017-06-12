from os.path import dirname, join

import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, Button, DataTable, TableColumn, NumberFormatter
from bokeh.io import curdoc

df = pd.read_csv(join(dirname(__file__), 'salary_data.csv'))

source = ColumnDataSource(data=dict())
sourcex = TableDataSource()

def update():
    print('hi')
#    current = df[df['salary'] <= slider.value].dropna()
    current = df
    source.data = {
         'name'             : current.Code,
         'salary'           : current.Library,
         'years_experience' : current.Institute,
     }
    print(source.data)

slider = Slider(title="Max Salary", start=10000, end=250000, value=150000, step=1000)
slider.on_change('value', lambda attr, old, new: update())

button = Button(label="Download", button_type="success")
button.callback = CustomJS(args=dict(source=source),
                           code=open(join(dirname(__file__), "download.js")).read())

columns = [
    TableColumn(field="name", title="Employee Name"),
    TableColumn(field="salary", title="Income"),
    TableColumn(field="years_experience", title="Experience (years)")
]

data_table = DataTable(source=source, columns=columns, width=800)

controls = widgetbox(slider, button)
table = widgetbox(data_table)

curdoc().add_root(row(controls, table))
curdoc().title = "Export CSV"

update()