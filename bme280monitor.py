import sys
import datetime as dt
import ctypes 
import os
import time
import collections as clts
import threading
import netifaces
import plotly 
import dash 
import dash.dependencies as dd
import dash_core_components as dcc 
import dash_html_components as html 

# To execute this script at startup update /etc/rc.local with:
# 1. reference to the directory where script is saved
# cd /home/pi/progetti/bme280monitor 
# 2. sleep some seconds so interfaces go up
# sleep 30
# 3. set up script execution
# sudo -u pi /usr/bin/python3 /home/pi/progetti/bme280monitor/bme280monitor.py > $

# bme280_calib_data "Python" class definition needed to import bme280_calib_data "C" structure
class bme280_calib_data(ctypes.Structure):
    _fields_ = [('dig_t1', ctypes.c_uint16),
                ('dig_t2', ctypes.c_int16),
                ('dig_t3', ctypes.c_int16),
                ('dig_p1', ctypes.c_uint16),
                ('dig_p2', ctypes.c_uint16),
                ('dig_p3', ctypes.c_int16),
                ('dig_p4', ctypes.c_int16),
                ('dig_p5', ctypes.c_int16),
                ('dig_p6', ctypes.c_int16),
                ('dig_p7', ctypes.c_int16),
                ('dig_p8', ctypes.c_int16),
                ('dig_p9', ctypes.c_int16),
                ('dig_h1', ctypes.c_uint8),
                ('dig_h2', ctypes.c_int16),
                ('dig_h3', ctypes.c_uint8),
                ('dig_h4', ctypes.c_int16),
                ('dig_h5', ctypes.c_int16),
                ('dig_h6', ctypes.c_int8),
                ('t_fine', ctypes.c_int32)]
    
    def __repr__(self):
        return '({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18})'.format(self.dig_t1, self.dig_t2, self.dig_t3, self.dig_p1, self.dig_p2, self.dig_p3, self.dig_p4, self.dig_p5, self.dig_p6, self.dig_p7, self.dig_p8, self.dig_p9, self.dig_h1, self.dig_h2, self.dig_h3, self.dig_h4, self.dig_h5, self.dig_h6, self.t_fine)

# bme280_settings "Python" class definition needed to import bme280_settings "C" structure
class bme280_settings(ctypes.Structure):
	_fields_ = [('osr_p', ctypes.c_uint8),
	            ('osr_t', ctypes.c_uint8),
	            ('osr_h', ctypes.c_uint8),
	            ('filter', ctypes.c_uint8),
	            ('standby_time', ctypes.c_uint8)]
	            
	def __repr__(self):
		return '({0}, {1}, {2}, {3}, {4})'.format(self.osr_p, self.osr_t, self.osr_h, self.filter, self.standby_time)


# bme280_data "Python" class definition needed to import bme280_data "C" structure
class bme280_data(ctypes.Structure):
	_fields_ = [('pressure', ctypes.c_double), ('temperature', ctypes.c_double), ('humidity', ctypes.c_double)]
	
	def __repr__(self):
		return '({0}, {1}, {2})'.format(self.pressure, self.temperature, self.humidity)

# bme280_dev "Python" class definition needed to import bme280_dev "C" structure
class bme280_dev(ctypes.Structure):
	_fields_ = [('chip_id', ctypes.c_uint8),
	            ('intf_ptr', ctypes.c_void_p),
	            ('intf', ctypes.c_int),
	            ('read', ctypes.POINTER(ctypes.c_int8)),
	            ('write', ctypes.POINTER(ctypes.c_int8)),
	            ('delay_us', ctypes.POINTER(ctypes.c_int8)),
	            ('calib_data', bme280_calib_data),
	            ('settings', bme280_settings),
	            ('intf_rslt', ctypes.c_int8)]
	            
	def __repr__(self):
		return '({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})'.format(self.chip_id, self.intf_ptr, self.intf, self.read, self.write, self.delay_us, self.calib_data, self.settings, self.intf_rslt)

# Function for wrapping "C" functions in "Python"
def wrap_function(lib, funcname, restype, argtypes):
    #Simplify wrapping ctypes functions
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func

# Print data sample on standrd output
def print_data(ciclo, data):
    s = ('Ultimo campione - Numero: %i ' % (ciclo)) + ' - Orario: ' + dt.datetime.now().strftime('%H:%M:%S') + ' - %.2f degC, %.2f hPa, %.2f%%' % (data.temperature, 0.01*data.pressure, data.humidity)
    print(s)
    
# Function to be executed as indipendent thread to acquire samples every 'sec' seconds 
def AcquisitionThread(sec):
	global hum
	global pres
	
	c=0
	while True:
		x = dt.datetime.now().replace(microsecond=0)
		# Read data from BME280
		get_data_forced_mode(dev, data)
		print_data(c, data)
		temp = round(data.temperature, 2)
		hum = round(data.humidity, 2)
		pres = round(data.pressure, 2)
		X.append(x)
		Y.append(temp) 
		time.sleep(sec)
		c+=1

# Main program 

# Section 1: load libbme280.so library
shared_lib_path = "./libbme280.so"
try:
    # load libbme280.so library
    libc = ctypes.CDLL(shared_lib_path)
    print("Successfully loaded ", libc)
    # wrap "C" function 'get_one_sample' in a Python function 
    get_data_forced_mode = wrap_function(libc, 'get_one_sample', ctypes.c_uint8, [ctypes.POINTER(bme280_dev), ctypes.POINTER(bme280_data)])
    # instantiate bme280_dev object
    dev = bme280_dev()
    # instantiate bme280_data object
    data = bme280_data()
except Exception as e:
    print(e)
   
# Section 2: queues initialization for temperature and time
nsamples = 144
interval_btw_samples_s = 600
X = clts.deque(maxlen = nsamples) 
Y = clts.deque(maxlen = nsamples) 
d = dt.datetime.now().replace(second=0, microsecond=0) - dt.timedelta(milliseconds=nsamples*interval_btw_samples_s*1000)
for i in range(nsamples):
    X.append(d + dt.timedelta(milliseconds=i*interval_btw_samples_s*1000))
    Y.append(0) 
hum = 0
pres = 0
  
# Section 3: create dash app
refresh_interval_s = 60
app = dash.Dash(__name__) 
  
# define dash app layout
app.layout = html.Div( 
    html.Div([
        dcc.Graph(id = 'live-graph'), 
        dcc.Interval( 
            id = 'graph-update', 
            interval = refresh_interval_s*1000,  
            n_intervals = 0
        ),
	html.P(id='last-update')
    ])
)     

# define dash app callback used to update 'last-update' html.P
@app.callback(dd.Output('last-update', 'children'),
              dd.Input('graph-update', 'n_intervals')
)
def update_metrics(n):
    d = X[-1]
    t = Y[-1]
    style = {'padding': '2px', 'fontSize': '14px', 'font-family': 'Arial'}
    return [
	html.Span('Ultima lettura', style=style),
	html.Span('Orario: {0}'.format(d), style=style),
	html.Span('Temperatura: {0:.2f}'.format(t), style=style)
    ]  
  
# define dash app callback to update 'live-graph' html.Div
@app.callback( 
    dd.Output(component_id='live-graph', component_property='figure'), 
    [ dd.Input(component_id='graph-update', component_property='n_intervals') ] 
) 
def update_graph_scatter(n):

    datatemp = plotly.graph_objs.Scatter( 
            x=list(X), 
            y=list(Y), 
            name='Scatter', 
            mode= 'lines+markers'
    ) 

    datahum = plotly.graph_objs.Indicator( 
            value=hum, 
            gauge={'bar': {'color': '#335EFF'}, 'axis': { 'range': [0, 100] }, 'steps': [{ 'range': [0, 250], 'color': "lightgray" }, { 'range': [0, 50], 'color': "gray" }]},
            mode= 'gauge+number',
            title={'text' : 'Umidità (%)'}
    ) 

    datapres = plotly.graph_objs.Indicator( 
            value=pres, 
            gauge={'bar': {'color': '#335EFF'}, 'axis': { 'range': [0, 120000] }, 'steps': [{ 'range': [0, 120000], 'color': "lightgray" }, { 'range': [0, 60000], 'color': "gray" }], 'threshold': {'line': { 'color': "red", 'width': 4 }, 'thickness': 0.75, 'value': 101325}},
            mode= 'gauge+number',
            title={'text' : 'Pressione (hPa)'}
    )

    # Create the graph with subplots
    d = X[-1]
    t = Y[-1]
    fig = plotly.subplots.make_subplots(rows=2, cols=2, specs=[[{"colspan": 2, "type": "xy"}, None], 
           [{"type": "domain"}, {"type": "domain"}]], subplot_titles=('Ultima lettura - Orario: {0} - Temperatura: {1:.2f} (degC)'.format(d,t), "", ""))

    # Update sublots temp
    fig.append_trace(datatemp, 1, 1)
    fig.layout.annotations[0].update(font={'size': 20})
    
    #Update layout
    fig.update_layout(height=600, xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [-10,40]),title=dict(text='<b>BME280 Monitor</b>', x=0.5, y=0.95, font=dict(family="Arial", size=20, color='#000000')))
    # Update subplot hum
    fig.append_trace(datahum, 2, 1)
    # Update subplot pressure
    fig.append_trace(datapres, 2, 2)

    return fig
    
# Section 4: Define and start thread for data acquisition
th = threading.Thread(target=AcquisitionThread, args=(interval_btw_samples_s,))
th.daemon = True
th.start()

# Section 5: Retrive raspberry wlan0 ip address 
addrs = netifaces.ifaddresses('wlan0')
ipaddr = addrs[netifaces.AF_INET][0]['addr']

# Section 6: Start web server
if __name__ == '__main__': 
    app.run_server(host= ipaddr, port='9090', debug=True, use_reloader=False)
    

