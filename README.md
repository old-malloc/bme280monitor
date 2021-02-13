<body lang="it-IT" link="#000080" vlink="#800000" dir="ltr">
<div id="Frame1" dir="ltr" style="position: absolute; top: 0cm; left: 0cm; width: 19.69cm; height: 1.27cm; border: none; padding: 0cm; background: #ffffff">
	<ul><li><p align="center" style="margin-right: 0.11cm; margin-bottom: 0cm; line-height: 320%">
		</p>
	</ul>
</div>
<p align="center" style="margin-top: 0.42cm; margin-bottom: 0.21cm; line-height: 100%; page-break-after: avoid">
<font face="Liberation Sans, sans-serif"><font size="6" style="font-size: 28pt"><b>IOT
Lab - Data Monitoring</b></font></font></p>
<p style="margin-bottom: 0cm; line-height: 100%"><br/>

</p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif"><span style="font-style: normal"><span style="font-weight: normal">This
series of articles are intended to be an explanatory exposition
useful for understanding the general operation principles of IOT
(Internet Of Things) solutions.</span></span></font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">The article &quot;IOT Lab - Data
Acquisition&quot; described how to create a device for measuring
temperature, pressure and humidity environmental parameters using a
BME280 sensor and a Raspberry Pi.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">A shared library in “C”
language has been created with the functions useful for carrying out
a measurement and printing the acquired results then operation has
been verified with a simple test program.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">In this article, the goal is to
create a monitor of environmental values that allows the graphic
display through a web server that can be reached from any device
connected to the wi-fi network to which the Raspberry Pi is
connected.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">To achieve this goal, a Python
script was created that uses the Plotly and Dash modules respectively
for the creation of graphs and their display via the web.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
&nbsp;<font face="Source Serif Pro, serif"><span style="font-style: normal"><span style="font-weight: normal">The
script code is available at
https://github.com/old-malloc/bme280monitor/blob/main/bme280monitor.py
and a description of its operation is provided below.</span></span></font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">&quot;Section 1&quot; loads the
shared library &quot;libbme280.so&quot;, defines the
get_data_forced_mode function so that it calls the 'get_one_sample'
function in the shared library and instantiates the two variables
&quot;dev&quot; and &quot;data&quot; as objects of the &quot;bme280_dev&quot;
classes and &quot;bme280_data&quot;. The &quot;bme280_dev&quot; and
&quot;bme280_data&quot; classes are defined in order to map the C
structures that are used by the 'get_one_sample' function that have
to be called from the Python script.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">&quot;Section 2&quot; initializes the queue
of acquisition times, the queue of temperature values and the simple
variables to store the latest pressure and humidity values. As you
can see, for the temperature samples it was decided to store a
history of 144 samples while for humidity and pressure only the last
measurement is kept. This section also defines a variable to store
the time interval between one acquisition and the next.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">&quot;Section 3&quot; defines
the Dash application (&quot;app&quot; variable), the graphic aspect
(layout) that must be presented on the web pages and its updating
methods. Then an update interval of 60 seconds and two callback
functions are defined to refresh the 'last-update' section and the
'live-graph' section of the html page that makes up the layout.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">&quot;Section 4&quot; starts an independent
thread that calls the AcquisitionThread function. The
AcquisitionThread function acquires a sample every 600 seconds and
prints it to standard output.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">&quot;Section 5&quot; acquires
the IP address of the Raspberry Pi's Wi-Fi interface.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">&quot;Section 6&quot; starts a
web server associated with the Dash application on the Wi-Fi
interface at port 9090.</font></p>
<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
<font face="Source Serif Pro, serif">As you can see from the
following figure, the script can be launched through the command
“python3 ./bme280monitor.py”.</font></p>
<ul type="disc">
	<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
	<font face="Source Serif Pro, serif">The monitor can be viewed from
	the browser of any device on the same wi-fi network to which the
	Raspberry Pi is connected through the link http: // [IP address of
	the Raspberry Pi]: 9090.</font></p>
	<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
	<font face="Source Serif Pro, serif">The following figure shows the
	web page that realizes the monitor of the environmental parameters
	measured through the bme280 sensor.</font></p>
	<p align="left" style="margin-bottom: 0cm; border: none; padding: 0cm; font-variant: normal; letter-spacing: normal; font-style: normal; font-weight: normal; line-height: 320%; orphans: 2; widows: 2; background: #ffffff">
	<font face="Source Serif Pro, serif">The next article will address
	the integration of the acquisition system with an IOT service in the
	cloud.</font></p>
</ul>
<p style="margin-bottom: 0cm; line-height: 100%"><br/>

</p>
</body>
