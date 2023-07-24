# solarsimulator
#Keithly.py This Python script provides a way to control a Keithley instrument over a serial connection using the Keithley's SCPI (Standard Commands for Programmable Instruments) command set.The script includes functions for sending commands to the instrument, setting up the instrument for different modes of operation, reading data from the instrument, running the instrument through a voltage sweep, and resetting the instrument to its default settings.

The script includes the following functions:

send_command(self, command) - Sends an SCPI command to the instrument. set_sensor_type(self, sensor_type) - Sets the sensor type (either current or voltage). set_source_type(self, source_type) - Sets the source type (either current or voltage). read(self, sweeppoints) - Reads measurement data from the instrument. sweep(self, start=-0.2, stop=1.2, step=0.05, num_sweeps=1) - Runs a voltage sweep and collects measurement data. run_start_up_commands(self) - Runs a set of start-up commands to reset the instrument to its default settings. constantvoltagemeasureself(self,k) - Measures current at a fixed voltage value across time. constantcurrentmeasureself(self,k) - Measures voltage at a fixed current value across time. The script also contains the code to perform the following steps:

Establish a connection with the Keithley device.

Reset the Keithley instrument to its default settings. Set the Keithley instrument to use voltage as the source and current as the sensor. Run a voltage sweep and collect measurement data. Close the connection with the Keithley instrument.

#muxgui.py

This is a Python script that provides a graphical user interface (GUI) for controlling a multiplexer switch.
