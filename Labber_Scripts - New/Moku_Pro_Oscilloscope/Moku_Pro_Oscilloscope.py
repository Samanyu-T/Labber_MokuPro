# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 16:52:19 2022

@author: Triton
"""

from moku.instruments import Oscilloscope
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
        Instrument = Oscilloscope(self.getValue('IP'), force_connect = True)
        Instrument.generate_waveform(1, 'Sine', amplitude=0.5, frequency=10e3)
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
       
        Instrument.relinquish_ownership()
        
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        quant.setValue(value)


        
        if quant.name.startswith('Time'):
            time_span = self.getValue('Time Span')
            Instrument.set_timebase(-time_span, time_span)
        elif quant.name.startswith('Acquisition'):
            Instrument.set_acquisition_mode(self.getValue('Acquisition Mode'))
        
        elif quant.name.startswith('Trigger'):
            source = self.getValue('Trigger Source')
            level = self.getValue('Trigger Level')
            mode = self.getValue('Trigger Mode')
            edge = self.getValue('Trigger Edge Type')
            nth_event = self.getValue('Trigger Nth Event')
            holdoff = self.getValue('Trigger Holdoff Time')
            noise_reject = self.getValue('Trigger Noise Reject')
            hf_reject = self.getValue('Trigger HF Reject')

            Instrument.set_trigger(type = 'Edge', source = source, level = level, 
                                                mode = mode, edge = edge, nth_event = int(nth_event),
                                                holdoff = holdoff, noise_reject = bool(noise_reject),
                                                hf_reject = bool(hf_reject))
        
        if quant.name.startswith('Freq'):
            Instrument.generate_waveform(1, 'Sine', amplitude=0.5, frequency=value)

        return value 
    
    def performGetValue(self, quant, options={}):
        
       if quant.name.startswith('Data - Ch1'):
           data = Instrument.get_data()
           
           for channel in ['ch1', 'ch2']:
               trace = quant.getTraceDict(value = np.asarray(data[channel]), x = np.asarray(data['time']))
               self.setValue(quant.name[:-1] + channel[-1], trace)
   
           return quant.getValue()

       else:
           return quant.getValue()
            
                
