from bokeh.plotting import curdoc
from bokeh.layouts import widgetbox
from bokeh.layouts import column as bokehCol
from bokeh.models.layouts import Column
from bokeh.models.widgets import DatePicker
from datetime import date
from datetime import timedelta as td
from datetime import datetime as dt
from bokeh.io import output_notebook
from bokeh.plotting import show
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler

output_notebook()

def modify_doc(doc):

    crnt_date=dt.now()

    dt_pckr_strt=DatePicker(title='Select start of sync date',min_date=date(2017,1,1),max_date=date.today())


    def callback(attr,old,new):
        print(type(old))
        print('old was {} and new is {}'.format(old,new))



    dt_pckr_strt.on_change('value',callback)

    doc.add_root(bokehCol(dt_pckr_strt))


app = Application(FunctionHandler(modify_doc))
show(app) #notebook_url="localhost:8888"