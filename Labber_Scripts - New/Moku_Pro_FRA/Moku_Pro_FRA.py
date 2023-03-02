# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:43:26 2022

@author: Triton
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:18:37 2022

@author: Triton
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 16:52:19 2022

@author: Triton
"""

from moku.instruments import FrequencyResponseAnalyzer
import numpy as np
import time
import InstrumentDriver
import json
import math
class Driver(InstrumentDriver.InstrumentWorker):
    
    # def __init__(self):
    #     self.IP = '[fe80:0000:0000:0000:7269:79ff:feb0:0470%3]'
    #     self.Instrument = WaveformGenerator(self.IP, force_connect = True)
    #     self.Instrument.relinquish_ownership()

    def performOpen(self, options={}):
        '''Perform the operation of opening the instrument connection'''
        global Instrument
        Instrument = FrequencyResponseAnalyzer(self.getValue('IP'), force_connect = True)
        
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
       
        Instrument.relinquish_ownership()
        
    
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        
        #Initialize the Instrument Settings
        
        quant.setValue(value)

        if quant.name.startswith('Output'):
            amp = self.getValue('Output Amplitude')
            off = self.getValue('Output Offset')
            phase = self.getValue('Output Phase')
            for i in range(1,3) :
                Instrument.set_output(i,amp, off)
                Instrument.set_output_phase(i,phase)
        
        elif quant.name.startswith('Sweep'):
            freq1 = self.getValue('Sweep Start Freq')
            freq2 = self.getValue('Sweep End Freq')
            n_pts = int(self.getValue('Sweep Num-Points'))
            avg_t = self.getValue('Sweep Averaging-Time')
            avg_cyc = int(self.getValue('Sweep Averaging-Cycles'))
            set_t = self.getValue('Sweep Settling-Time')
            set_cyc = int(self.getValue('Sweep Settling-Cycles'))
            swp_linear = self.getValue('Sweep Linear')
            Instrument.set_sweep(start_frequency=freq1, stop_frequency=freq2,
                                 num_points=n_pts , averaging_time=avg_t,
                                 settling_time=set_t, averaging_cycles=avg_cyc,
                                 settling_cycles=set_cyc, linear_scale=swp_linear)

            Instrument.start_sweep()
            
        elif quant.name.startswith('Input'):
            for i in range(1,3) :
                coupling = self.getValue('Input Ch' + str(i) + ' - Coupling')
                impedance = self.getValue('Input Ch' + str(i) + ' - Impedance')
                inp_range = self.getValue('Input Ch' + str(i) + ' - Range')
                Instrument.set_frontend(i, impedance=impedance, coupling=coupling, range=inp_range)
        
        elif quant.name.startswith('Harmonic'):
            Instrument.set_harmonic_multiplier(int(self.getValue('Harmonic Multiplier')))
        elif quant.name.startswith('Measurement'):
            Instrument.measurement_mode(self.getValue('Measurement Mode'))
                
        return value 
    
    def performGetValue(self, quant, options={}):
        
        if quant.name.startswith('Magnitude - Ch1'):
            #Wait for the sweeping to be done before collecting the data.
            #time.sleep(Instrument.get_sweep()['estimated_sweep_time'])
            #Collect the data from the Moku
            data = Instrument.get_data()
            
            #Update Labber
                
            for channel in data:
                
                data[channel]['magnitude'] = [0 if x == 'nan' else x for x in data[channel]['magnitude']]
                data[channel]['phase'] = [0 if x == 'nan' else x for x in data[channel]['phase']]

                trace_magnitude = quant.getTraceDict(value = np.asarray(data[channel]['magnitude']), 
                                           x = np.asarray(data[channel]['frequency']))

                trace_phase  = quant.getTraceDict(value = np.asarray(data[channel]['phase']) , 
                                           x = np.asarray(data[channel]['frequency']))
                
                self.setValue('Phase - Ch' + channel[-1], trace_phase)
                self.setValue('Magnitude - Ch' + channel[-1], trace_magnitude)        
            
            return quant.getValue()       
        
        return quant.getValue()
            
                
