# -*- coding: utf-8 -*-
"""


@author: MY PC
"""
import time    
import numpy as np   # numpy is a popular library for numerical computations in Python.
import keithley_serial as ks
import pyvisa   #VISA is commonly used for controlling measurement instruments and other devices.
import matplotlib as plt
rm = pyvisa.ResourceManager()
print(rm.list_resources())
keithley=rm.open_resource('ASRL31::INSTR') #established connection with the ketithley device
keithley.set_visa_attribute(pyvisa.constants.VI_ATTR_ASRL_BAUD, 9600) 
keithley.timeout=None
print(keithley.query('*IDN?'))          #a command to ensure connection is established properly. Ideally returns the system names      
def send_command(self, command):
        '''

    Parameters 
    ----------
    command : The command that needs to be written to the keithley device to perform the specific function

    Returns
    -------
    None.

    '''
        response = ks.write(self, command)      
        
def set_sensor_type(self, sensor_type):
    '''
    

    Parameters
    ----------
    sensor_type : Pass as CURR , VOLT sets the keithleys sensing mode to current sensor or voltage sensor
    Returns
    -------
    None.

    '''
    sensor_type = sensor_type.lower()
    if sensor_type == 'current' or sensor_type == 'curr' or sensor_type == 'c':
        send_command(self,':SENS:FUNC "CURR"')
        
    elif sensor_type == 'voltage' or sensor_type == 'volt' or sensor_type == 'v':
          send_command(self,':SENS:FUNC "VOLT"')
        
    else:
        print("Unknown sensor setting!")
        return None


def set_source_type(self, source_type):
    '''
    

    Parameters
    ----------
    sensor_type : Pass as CURR , VOLT sets the keithleys source mode to current or voltage sources
    Returns
    -------
    None.
    '''
    source_type = source_type.lower()
    if source_type == 'current' or source_type == 'curr' or source_type == 'c':
        send_command(self,':SOUR:FUNC CURRENT')
    elif source_type == 'voltage' or source_type == 'volt' or source_type == 'v':
        send_command(self,':SOUR:FUNC VOLT')
    else:
        print("Unknown source setting!")
        
      
def read(self,sweeppoints):
    '''
    

    This function reads the values from the keithley device when it is called. This current voltage
    and time is measured and stored as array and the MPP for the IV curve is calculated.

    Returns
    -------
    None.
   '''
    send_command(self,':SENSE:CURR:PROT 0.2')  #this sets the protection value for the current, measured current does not exceed this value
    send_command(self,':OUTP ON') #turns output on
    send_command(self,':INIT')
    time.sleep(1)
    response=self.query(':READ?') #reads the value and stores it in response 
    time.sleep(1)
    send_command(self,':OUTP OFF')
    
    #the data processing, graph plotting and further calculations takes place from here
    data=[float(val) for val in response.split(',')]
    vvalues=data[0::3]
    cvalues=data[1::3]
    tvalues=data[2::3]
    return vvalues, cvalues
    print(tvalues)
    print('----------------------------')
    print(vvalues)
    print('----------------------------')
    print(cvalues)
    for v,i in zip(vvalues,cvalues):
        print(f' Voltage : {v: .3f} V , Current: {i:.6e} A')
    for i in range(len(cvalues)):
        cvalues[i]=cvalues[i]*-1
    plt.pyplot.plot(vvalues,cvalues) 
    plt.pyplot.xlabel("VOLTAGE(V)")
    plt.pyplot.ylabel("CURRENT(A)")
    p=[]
    for i in range(len(vvalues)):
        p.append(vvalues[i]*cvalues[i])
    mpp=p.index(max(p))
    k=vvalues[mpp]
    print('mpp = {:.2f}'.format(k))
    plt.pyplot.scatter(vvalues[mpp],cvalues[mpp], color='red', label='mpp = {:.2f}'.format(k))
    plt.pyplot.legend()
    plt.pyplot.grid()
    plt.pyplot.show()
    plt.pyplot.plot(vvalues,p)
    plt.pyplot.xlabel("VOLTAGE(V)")
    plt.pyplot.ylabel("Power")
    plt.pyplot.show()
    return response

def sweep(self, start=-0.2, stop=1.2, step=0.05, num_sweeps=1):
    '''
    

    Parameters
    ----------
    start : TYPE, optional
        DESCRIPTION. The default is -0.2. Gives the starting value of voltage to sweep
    stop : TYPE, optional
        DESCRIPTION. The default is 1.2. Gives the end value for voltage to sweep
    step : TYPE, optional
        DESCRIPTION. The default is 0.05. The sweep step size
    num_sweeps : TYPE, optional
        DESCRIPTION. The default is 1. The number of times the sweep should take place

    Returns
    -------
    None.

    '''
    voltage_values_list = []
    current_values_list = []
    # mpp_voltages = []
    # mpp_currents =[]
    mpp_powers =[]
    for n in range(1, num_sweeps + 1):
        source_delay = n / 28  # Calculate the source delay for each sweep
        print(f"Sweep {n}/{num_sweeps} with Source Delay: {source_delay:.2f} seconds")

        sweep_points = int((stop - start) / step) + 1
        print(sweep_points)
        num_trigs = sweep_points
        print(num_trigs)
        send_command(self,':FORM:ELEM VOLT, CURR,TIME') #indicates that Voltage, current and Time is to be masured.
        send_command(self,':SOUR:FUNC VOLT')   #sets the source to voltage
        time.sleep(.1)
        send_command(self,':SENS:FUNC "CURR"') #sets the sensing to current
        time.sleep(.1)
        send_command(self,':SENS:VOLT:PROT 0.18') #protection value for votlage
        time.sleep(.1)
        send_command(self,':SOUR:VOLT:MODE SWE') #sets the device to sweeping mode
        time.sleep(.1)
        send_command(self,':SOUR:SWE:RANG AUTO') 
        time.sleep(.1)
        send_command(self,':SOUR:SWE:SPAC LIN') #sets to linear sweep mode
        time.sleep(.1)
        send_command(self,':SOUR:SWE:DIR DOWN')  #sets sweeping direction to downwards
        #commands below gives the sweeping commands
        send_command(self,':SOUR:VOLT:START %s' %start)
        time.sleep(.1)
        send_command(self,':SOUR:VOLT:STEP %s' %step)
        time.sleep(.1)
        send_command(self,':SOUR:VOLT:STOP %s' %stop)
        time.sleep(.1)
        send_command(self,':SOUR:SWE:POIN %s' %sweep_points)
        time.sleep(.1)
        send_command(self,':TRIG:COUN %s' %num_trigs) 
        time.sleep(.1)
        send_command(self, f':SOUR:DEL {source_delay}') #the delay between each sweep point
        time.sleep(.1)
        volt,current=read(keithley,sweep_points)
        vvalues, cvalues = read(keithley, sweep_points)
        voltage_values_list.append(vvalues)
        current_values_list.append(cvalues)
        # Calculate MPP for the current sweep
        power = [v * i for v, i in zip(volt, current)]
        mpp_power = max(power)
        mpp_powers.append(mpp_power)
     
        # Plot MPP Power for each sweep
    sweep_numbers = list(range(1, num_sweeps + 1))
    plt.pyplot.plot(sweep_numbers, mpp_powers, marker='o', linestyle='-', color='b')
    plt.pyplot.xlabel("Sweep Number")
    plt.pyplot.ylabel("MPP Power (W)")
    plt.pyplot.grid()
    plt.pyplot.show()    
    return voltage_values_list, current_values_list  # Return the lists containing voltage and current data

def run_start_up_commands(self):
    '''
    
     Function to run when the device is startup. It sets all device paramters to its default value

    Returns
    -------
    None.

    '''
    for com in start_up_commands:
        send_command(self,com)
        time.sleep(.01)

def constantvoltagemeasureself(self,k):
    '''
    
    Function to measure current at a fixed voltage value accross time.
    Parameters
    ----------
    k : TYPE
        DESCRIPTION. The voltage to be fixed

    Returns
    -------
    None.

    '''
    send_command(self,':SOUR:FUNC VOLT')
    send_command(self,':SENS:FUNC "CURR"')
    send_command(self,':SENSE:CURR:PROT 0.2')
    send_command(self,':SOUR:VOLT:MODE FIX')
    send_command(self,':SOUR:VOLT:LEV %f' %k)
    send_command(self,':FORM:ELEM CURR,TIME')
    send_command(self,':OUTP ON')
    send_command(self,':INIT')
    send_command(self,':TRIG:COUN 5')
    send_command(self,':SOUR:DEL 0.1')
    response=self.query(':READ?')
    time.sleep(1)
    send_command(self,':OUTP OFF')
    print(response)
    data=[float(val) for val in response.split(',')]
    cvalues=data[0::2]
    tvalues=data[1::2]
    plt.pyplot.plot(tvalues,cvalues) 
    plt.pyplot.xlabel("TIME(s)")
    plt.pyplot.ylabel("CURRENT(A)")            
    plt.pyplot.show()
    
    
def constantcurrentmeasureself(self,k):
    '''
    
    Function to measure voltage at a fixed current value accross time.
    Parameters
    ----------
    k : TYPE
        DESCRIPTION. The voltage to be fixed

    Returns
    -------
    None.

    '''
    send_command(self,':SOUR:FUNC CURR')
    send_command(self,':SENS:FUNC "VOLT"')
    send_command(self,':SENSE:VOLT:PROT 10')
    send_command(self,':SOUR:CURR:MODE FIX')
    send_command(self,':SOUR:CURR:%f' %k)
    send_command(self,':FORM:ELEM VOLT,TIME')

    send_command(keithley, ':SYST:RSEN ON')
    send_command(self,':OUTP ON')
    send_command(self,':INIT')
    send_command(self,':TRIG:COUN 10')
    send_command(self,':SOUR:DEL 1')
    response=self.query(':READ?')
    time.sleep(1)

    send_command(keithley, ':SYST:RSEN OFF')
    send_command(self,':OUTP OFF')
    print(response)
    data=[float(val) for val in response.split(',')]
    vvalues=data[0::2]
    tvalues=data[1::2]
    plt.pyplot.plot(tvalues,vvalues) 
    plt.pyplot.xlabel("TIME(s)")
    plt.pyplot.ylabel("VOLT(v)")            
    plt.pyplot.show()
#the various startup commands that need to be excecuted at the start of the system. 
start_up_commands = ["*RST",
                     ":SYST:TIME:RES:AUTO 1",
                     ":SYST:BEEP:STAT 1",
                     ":SOUR:FUNC CURR",
                     ":SENS:FUNC:CONC OFF",
                     ":SENS:AVER:STAT OFF",
                     ":SENS:CURR:NPLC 0.01",
                     ":SENS:VOLT:NPLC 0.01",
                     ":SENS:RES:NPLC 0.01",
                     ":SENS:FUNC 'VOLT'",
                     ":SENS:VOLT:RANG 1e1",
                     ":TRIG:DEL 0.0",
                     ":SYST:AZER:STAT OFF",
                     ":SOUR:DELAY 0.0",
                     ":DISP:ENAB ON"]

run_start_up_commands(keithley)
print('start done')
set_source_type(keithley, 'voltage')
set_sensor_type(keithley, 'current')
sweep(keithley)
keithley.close()
