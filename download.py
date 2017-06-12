import numpy as np
import pandas as pd

from bokeh.io import show, output_file
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Category10
from bokeh.plotting import figure

# read in some stock data from the Yahoo Finance API
df = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])

source = ColumnDataSource.from_df(df)

p = figure(plot_width=800)
for y, c in zip(['b', 'c', 'd', 'e'], Category10[10]):
   p.line('a', y, color=c, legend=y, source=source)

p.add_tools(HoverTool(tooltips = [
   ("columan_name", "@{column_name}"),
   ("x-value", "$x"),
    ("y-value", "$y"),
        ]))

output_file("timeseries.html")

show(p)