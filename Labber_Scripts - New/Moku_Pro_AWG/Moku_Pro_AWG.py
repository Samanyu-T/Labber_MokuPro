# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:45:21 2022

@author: Triton
"""


from moku.instruments import ArbitraryWaveformGenerator
import numpy as np
import math
from BaseDriver import LabberDriver, Error

class Driver(LabberDriver):
    

    def performOpen(self, options={}):
        '''Perform the operation of opening the instrument connection'''
        global Instrument
        Instrument = ArbitraryWaveformGenerator(self.getValue('IP'), force_connect = True)
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
       
        Instrument.relinquish_ownership()
        
    
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        quant.setValue(value)
        
        try:
            channel = quant.name[-1]
            txt = ' - ch' + channel
            channel = int(channel)
            if not self.getValue('Enable Output' + txt):
                Instrument.enable_output(channel, False)
            else:
                Instrument.enable_output(channel, True)
                
                if not self.getValue('Premade File?' + txt):
                    
                    x = eval(self.getValue('Range of x' + txt))
                    wave = eval(self.getValue('f(x) in Python' + txt))
                    
                elif self.getValue('Premade File?' + txt):
                    
                    
                    wave = np.genfromtxt(self.getValue('File Location' + txt) + 
                                         str(int(self.getValue('File Number' + txt))) +'.txt')
                    
                amp = self.getValue('Amplitude' + txt)
                freq = self.getValue('Frequency' + txt)
                sample_rate = self.getValue('Sample Rate' + txt)
                Instrument.generate_waveform(channel=channel, sample_rate= sample_rate, lut_data=list(wave), 
                                             frequency=freq, amplitude=amp)
                
                if self.getValue('Modulate' + txt) == 'Burst':
                    trigger_src = self.getValue('Trigger Source' + txt)
                    trigger_mode = self.getValue('Trigger Mode' + txt)
                    trigger_lvl = self.getValue('Trigger Level' + txt)
                    input_rng = self.getValue('Input Range' + txt)
                    burst_cycles = int(self.getValue('Burst Cycles' + txt))
        
                    Instrument.burst_modulate(channel = channel,
                                                 trigger_source = trigger_src,
                                                 trigger_mode=trigger_mode,
                                                 burst_cycles=burst_cycles,
                                                 trigger_level = trigger_lvl,
                                                 input_range = input_rng)
                    
                elif self.getValue('Modulate' + txt) == 'Pulse':
                    dead_cyc = int(self.getValue('Dead Cycles' + txt))
                    dead_volt = self.getValue('Dead Voltage' + txt)
                    Instrument.pulse_modulate(channel, dead_cycles=dead_cyc, dead_voltage=dead_volt)

                elif self.getValue('Modulate' + txt) == 'Off':
                    Instrument.disable_modulation(channel=channel)
        except:
            pass
                
            
        
        return value 
    
    def performGetValue(self, quant, options={}):
        return quant.getValue()
                
