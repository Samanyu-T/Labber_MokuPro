# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:48:05 2022

@author: Triton
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 16:52:19 2022

@author: Triton
"""

from moku.instruments import LockInAmp
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
        Instrument = LockInAmp(self.getValue('IP'), force_connect = True)
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
       
        Instrument.relinquish_ownership()
        
    
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        quant.setValue(value)
        
        if quant.name.startswith('Demodulation'):
            if self.getValue(quant.name) == 'Internal':
                freq = self.getValue('Demod Frequency')
                Instrument.set_demodulation(mode = 'Internal', frequency = freq)
            else:
                Instrument.set_demodulation(mode = self.getValue(quant.name))
                
        elif quant.name.startswith('Demod'):
            aux_freq = self.getValue('Demod Frequency')
            aux_amp  = self.getValue('Demod Amplitude')
            Instrument.set_aux_output(frequency = aux_freq, amplitude = aux_amp)
            
            
        elif quant.name.startswith('LPF'):
            lpf_freq = self.getValue('LPF Cutoff Freq')
            lpf_slope = self.getValue('LPF Slope')
            Instrument.set_filter(corner_frequency=lpf_freq , slope=lpf_slope)
            
            
        elif quant.name.startswith('Input'):
            for i in range(1,3) :
                coupling = self.getValue('Input Ch' + str(i) + ' - Coupling')
                impedance = self.getValue('Input Ch' + str(i) + ' - Impedance')
                attenuation = self.getValue('Input Ch' + str(i) + ' - Attenuation')
                Instrument.set_frontend(i, impedance=impedance, coupling=coupling, attenuation=attenuation)
                
                
        elif quant.name.startswith('Output'):
            main_out = self.getValue('Output - Main')
            aux_out = self.getValue('Output - Aux')
            main_off = self.getValue('Output - Main Offset')
            aux_off = self.getValue('Output - Aux Offset')
            gain = self.getValue('Output - Gain')
            if main_out == 'X' and aux_out == 'Y or Theta':
                aux_out = 'Y'
            elif main_out == 'R' and aux_out == 'Y or Theta':
                aux_out = 'Theta'
            Instrument.set_outputs(main=main_out, main_offset=main_off, aux = aux_out, aux_offset = aux_off)
            Instrument.set_gain(main = gain, aux = gain)
            
        elif quant.name.startswith('Time'):
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
        
        Instrument.set_monitor(1, 'MainOutput')
        Instrument.set_monitor(2, 'AuxOutput')


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
            
                
