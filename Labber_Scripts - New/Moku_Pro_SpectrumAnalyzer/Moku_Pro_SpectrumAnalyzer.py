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

from moku.instruments import SpectrumAnalyzer
import numpy as np
import InstrumentDriver

class Driver(InstrumentDriver.InstrumentWorker):
    
    # def __init__(self):
    #     self.IP = '[fe80:0000:0000:0000:7269:79ff:feb0:0470%13]'
    #     self.Instrument = WaveformGenerator(self.IP, force_connect = True)
    #     self.Instrument.relinquish_ownership()

    def performOpen(self, options={}):
        '''Perform the operation of opening the instrument connection'''
        global Instrument
        Instrument = SpectrumAnalyzer(self.getValue('IP'), force_connect = True)
        Instrument.sa_output(1, amplitude=2, frequency=10e3)
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
       
        Instrument.relinquish_ownership()
        
    
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        quant.setValue(value)
        if quant.name.startswith('Frequency'):
            f_lower = self.getValue('Frequency Lower Bound')
            f_higher = self.getValue('Frequency Upper Bound')
            Instrument.set_span(f_lower, f_higher)
            
        elif quant.name.startswith('Window'):
            Instrument.set_window(window = self.getValue('Window Function'))

        elif quant.name.startswith('Input'):
            for i in range(1,3) :
                coupling = self.getValue('Input Ch' + str(i) + ' - Coupling')
                impedance = self.getValue('Input Ch' + str(i) + ' - Impedance')
                inp_range = self.getValue('Input Ch' + str(i) + ' - Range')
                Instrument.set_frontend(i, impedance=impedance, coupling=coupling, range=inp_range)
                
        return value 
    
    def performGetValue(self, quant, options={}):
        
        if quant.name in ('Data - Ch1', 'Data - Ch2', 'Data - Ch3', 'Data - Ch4'):
            channel = int(quant.name[-1])
            data = Instrument.get_data()
            return quant.getTraceDict(value = np.asarray(data['ch%d' % channel]), x = np.asarray(data['frequency']))


        else:
            return quant.getValue()
            
                
