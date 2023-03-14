# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:44:28 2022

@author: Anirvinya Samanyu Tirumala
"""

from moku.instruments import (MultiInstrument, Oscilloscope, WaveformGenerator,
ArbitraryWaveformGenerator, SpectrumAnalyzer, LockInAmp, FrequencyResponseAnalyzer)
import time
import numpy as np
from BaseDriver import LabberDriver, Error
import json
import InstrumentDriver
import math
import pandas as pd

class Driver(LabberDriver):

    def set_WVG(self,name,slot):
        
        #If we are initializing then 
        n_channels = []
        if name == 'init':
            n_channels = [1, 2]
        else:
            n_channels = [int(name[6])]
        
        for channel in n_channels:
            text_wvg1 = 'WVG Ch' + str(channel) + ' '
            text_wvg2 = ' - ' + str(slot)
            
            func = self.getValue(text_wvg1 + 'Function' + text_wvg2)
            modulation = self.getValue(text_wvg1 + 'Modulation' + text_wvg2)
            
            if func == 'Off':
                self.Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func)
            
            elif func == 'Sine':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                self.Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             offset = dc_offset,
                                             phase = phase)
            
            elif func == 'Square':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                duty = self.getValue(text_wvg1 + 'Duty Cycle' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                self.Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase= phase,
                                             offset = dc_offset,
                                             duty=duty)
                
            elif func == 'Ramp':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                symm = self.getValue(text_wvg1 + 'Ramp Symmetry' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                self.Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase = phase,
                                             offset = dc_offset,
                                             symmetry=symm)
                
            elif func == 'Pulse':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                edg_time = self.getValue(text_wvg1 + 'Edge Time' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                pulse_width = self.getValue(text_wvg1 + 'Pulse Width' + text_wvg2)
                self.Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase = phase,
                                             edge_time=edg_time,
                                             offset = dc_offset,
                                             pulse_width = pulse_width)
                
                
            elif func == 'DC':
                dc = self.getValue(text_wvg1 + 'DC Level' + text_wvg2)
                self.Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             dc_level=dc)
        
            '''MODULATION SECTION'''
            
            if modulation == 0:
                self.Instrument[slot-1].disable_modulation(channel = channel)
                
            else:
                
                modulation_type = self.getValue(text_wvg1 + 'Mod Type' + text_wvg2)
                modulation_freq = self.getValue(text_wvg1 + 'Mod Freq' + text_wvg2)
                
                if modulation_type == 'Amplitude':
                    am_depth = self.getValue(text_wvg1 + 'AM Depth' + text_wvg2)
                    self.Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Amplitude', 
                                              source='Internal', 
                                              depth=am_depth,
                                              frequency= modulation_freq)
                    
                elif modulation_type == 'Frequency':
                    fm_depth = self.getValue(text_wvg1 + 'FM Depth' + text_wvg2)
                    freq = self.getValue('Frequency' + text_wvg2)
        
                    if fm_depth > freq:
                        fm_depth = freq
                        
                    self.Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Frequency', 
                                              source='Internal', 
                                              depth=fm_depth,
                                              frequency= modulation_freq)
                    
                elif modulation_type == 'Phase':
                    pm_depth = self.getValue(text_wvg1 + 'PM Depth' + text_wvg2)               
                    self.Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Phase', 
                                              source='Internal', 
                                              depth=pm_depth,
                                              frequency= modulation_freq)          
                    
                elif modulation_type == 'Burst':
                    pass
                
                elif modulation_type == 'Sweep':
                    pass
    
    def set_AWG(self,name,slot):
        
        n_channels = []
        if name == 'init':
            n_channels = [1, 2]
        else:
            n_channels = [int(name[6])]
        
        for channel in n_channels:
            
            text_1 = 'AWG Ch' + str(channel) + ' '
            text_2 = ' - ' + str(slot)
            
            #Initialize the AWG with the desired waveform
            if self.getValue(text_1 +'Enable Output'+ text_2) == True or name == 'init':
                self.Instrument[slot-1].enable_output(channel, enable = True)
                if not self.getValue(text_1 +'Premade File?'+ text_2):
                    
                    x = eval(self.getValue(text_1 +'Range of x'+ text_2))
                    wave = eval(self.getValue(text_1 + 'f(x) in Python'+ text_2))
                    
                elif self.getValue(text_1 +'Premade File?'+ text_2):
                    wave = np.genfromtxt(self.getValue(text_1 +'File Location'+ text_2) 
                                         + str(int(self.getValue(text_1 +'File Number'+ text_2))) + '.txt')
                    
                amp = self.getValue(text_1 + 'Amplitude' + text_2)
                freq = self.getValue(text_1 + 'Frequency' + text_2)
                sample_rate = self.getValue(text_1 +'Sample Rate'+ text_2)
                self.Instrument[slot-1].generate_waveform(channel=channel, sample_rate= sample_rate, lut_data=list(wave), 
                                             frequency=freq, amplitude=amp)
                
                if self.getValue(text_1 +'Modulate'+ text_2) == 'Burst':
                    trigger_src = self.getValue(text_1 + 'Trigger Source' + text_2)
                    trigger_mode = self.getValue(text_1 + 'Trigger Mode' + text_2)
                    trigger_lvl = self.getValue(text_1 + 'Trigger Level' + text_2)
                    input_rng = self.getValue(text_1 + 'Input Range' + text_2)
                    burst_cycles = int(self.getValue(text_1 + 'Burst Cycles' + text_2))
        
                    self.Instrument[slot-1].burst_modulate(channel = channel,
                                                 trigger_source = trigger_src,
                                                 trigger_mode=trigger_mode,
                                                 burst_cycles=burst_cycles,
                                                 trigger_level = trigger_lvl,
                                                 input_range = input_rng)
        
                    
                elif self.getValue(text_1 +'Modulate'+ text_2) == 'Pulse':
                    dead_cyc = int(self.getValue(text_1 +'Dead Cycles'+ text_2))
                    dead_volt = self.getValue(text_1 +'Dead Voltage'+ text_2)
                    self.Instrument[slot-1].pulse_modulate(channel = channel, dead_cycles=dead_cyc, dead_voltage=dead_volt)
                    time.sleep(0.5)
        
        
                elif self.getValue(text_1 +'Modulate'+ text_2) == 'Off':
                    self.Instrument[slot-1].disable_modulation(channel=channel)
                  
            # If the input is meant to be turned off then this if statement will turn it off
            if not self.getValue(text_1 +'Enable Output'+ text_2):
                self.Instrument[slot-1].enable_output(channel, enable = False)
            

    def set_SPA(self,name,slot):
        if name.startswith('SPA Freq') or name == 'init':
            f_lower = self.getValue('SPA Freq Lower Bound - ' + str(slot))
            f_higher = self.getValue('SPA Freq Upper Bound - ' + str(slot))
            self.Instrument[slot-1].set_span(f_lower, f_higher)
            
        if name.startswith('SPA Window') or name == 'init':
            self.Instrument[slot-1].set_window(window = self.getValue('SPA Window Function - ' + str(slot)))
            
            
    def set_FRA(self,name,slot):
        if name.startswith('FRA Output') or name == 'init':
            amp = self.getValue('FRA Output Amplitude - ' + str(slot))
            off = self.getValue('FRA Output Offset - ' + str(slot))
            phase = self.getValue('FRA Output Phase - ' + str(slot))
            for i in range(1,3) :
                self.Instrument[slot-1].set_output(i,amp, off)
                self.Instrument[slot-1].set_output_phase(i,phase)
        
        if name.startswith('FRA Sweep') or name == 'init':
            freq1 = self.getValue('FRA Sweep Start Freq - ' + str(slot))
            freq2 = self.getValue('FRA Sweep End Freq - '+ str(slot))
            n_pts = int(self.getValue('FRA Sweep Num-Points - '+ str(slot)))
            avg_t = self.getValue('FRA Sweep Averaging-Time - '+ str(slot))
            avg_cyc = int(self.getValue('FRA Sweep Averaging-Cycles - '+ str(slot)))
            set_t = self.getValue('FRA Sweep Settling-Time - '+ str(slot))
            set_cyc = int(self.getValue('FRA Sweep Settling-Cycles - '+ str(slot)))
            swp_linear = self.getValue('FRA Sweep Linear - '+ str(slot))
            self.Instrument[slot-1].set_sweep(start_frequency=freq1, stop_frequency=freq2,
                                 num_points=n_pts , averaging_time=avg_t,
                                 settling_time=set_t, averaging_cycles=avg_cyc,
                                 settling_cycles=set_cyc, linear_scale=swp_linear)
            self.Instrument[slot-1].start_sweep()

            with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
                f.write(json.dumps(self.Instrument[slot-1].get_sweep()))
                f.write('Set \n') 
                
        if name.startswith('FRA Harmonic') or name == 'init':
            self.Instrument[slot-1].set_harmonic_multiplier(int(self.getValue('FRA Harmonic Multiplier - '+ str(slot))))
            
        if name.startswith('FRA Measurement') or name == 'init':
            self.Instrument[slot-1].measurement_mode(self.getValue('FRA Measurement Mode - '+ str(slot)) )
        

    def set_LIA(self,name,slot):
    
        if name.startswith('LIA Demodulation') or name == 'init':
            if self.getValue('LIA Demodulation - ' + str(slot)) == 'Internal':
                aux_freq = self.getValue('LIA Demodulation Frequency - ' + str(slot))
                aux_amp  = self.getValue('LIA Demodulation Amplitude - ' + str(slot))
                self.Instrument[slot-1].set_demodulation('Internal', frequency = aux_freq)
                self.Instrument[slot-1].set_aux_output(frequency = aux_freq, amplitude = aux_amp)
            else: 
                self.Instrument[slot-1].set_demodulation(mode = self.getValue('LIA Demodulation - ' + str(slot)))
            
            
        if name.startswith('LIA LPF') or name == 'init':
            lpf_freq = self.getValue('LIA LPF Cutoff Freq - '+ str(slot))
            lpf_slope = self.getValue('LIA LPF Slope - ' + str(slot))
            self.Instrument[slot-1].set_filter(corner_frequency=lpf_freq , slope=lpf_slope)
        
        if name.startswith('LIA Output') or name == 'init':
            main_out = self.getValue('LIA Output - Main - ' + str(slot))
            aux_out = self.getValue('LIA Output - Aux - ' + str(slot))
            main_off = self.getValue('LIA Output - Main Offset - ' + str(slot))
            aux_off = self.getValue('LIA Output - Aux Offset - ' + str(slot))
            if main_out == 'X' and aux_out == 'Y or Theta':
                aux_out = 'Y'
            elif main_out == 'R' and aux_out == 'Y or Theta':
                aux_out = 'Theta'
            self.Instrument[slot-1].set_outputs(main=main_out, main_offset=main_off, aux = aux_out, aux_offset = aux_off)
            
            gain = self.getValue('LIA Output - Gain - ' + str(slot))
            self.Instrument[slot-1].set_gain(main = gain, aux = gain)
            
            self.Instrument[slot-1].set_monitor(1, 'MainOutput')
            self.Instrument[slot-1].set_monitor(2, 'AuxOutput')

            
        if name.startswith('LIA Time') or name == 'init':
            timebase = self.getValue('LIA Timespan - ' + str(slot))
            self.Instrument[slot-1].set_timebase(-timebase, timebase)
        
        if name.startswith('LIA Trigger') or name == 'init':
            
            source = self.getValue('LIA Trigger Source - ' + str(slot))
            level = self.getValue('LIA Trigger Level - ' + str(slot))
            mode = self.getValue('LIA Trigger Mode - ' + str(slot))
            edge = self.getValue('LIA Trigger Edge Type - ' + str(slot))
            nth_event = self.getValue('LIA Trigger Nth Event - ' + str(slot))
            holdoff = self.getValue('LIA Trigger Holdoff Time - ' + str(slot))
            noise_reject = self.getValue('LIA Trigger Noise Reject - ' + str(slot))
            hf_reject = self.getValue('LIA Trigger HF Reject - ' + str(slot))

            self.Instrument[slot-1].set_trigger(type = 'Edge', source = source, level = level, 
                                                mode = mode, edge = edge, nth_event = int(nth_event),
                                                holdoff = holdoff, noise_reject = bool(noise_reject),
                                                hf_reject = bool(hf_reject))
            
        if name.startswith('LIA Acquisition') or name == 'init':
            
            mode = self.getValue('LIA Acquisition Mode - ' + str(slot))
            self.Instrument[slot-1].set_acquisition_mode(mode = mode)
            
    def set_OSC(self,name,slot):
        if name.startswith('OSC Timespan') or name == 'init':
            timebase = self.getValue('OSC Timespan - ' + str(slot))
            
            self.Instrument[slot-1].set_timebase(0, timebase)
            
        if name.startswith('OSC Trigger') or name == 'init':
            
            source = self.getValue('OSC Trigger Source - ' + str(slot))
            level = self.getValue('OSC Trigger Level - ' + str(slot))
            mode =  self.getValue('OSC Trigger Mode - ' + str(slot))
            edge = self.getValue('OSC Trigger Edge Type - ' + str(slot))
            nth_event = self.getValue('OSC Trigger Nth Event - ' + str(slot))
            holdoff = self.getValue('OSC Trigger Holdoff Time - ' + str(slot))
            noise_reject = self.getValue('OSC Trigger Noise Reject - ' + str(slot))
            hf_reject = self.getValue('OSC Trigger HF Reject - ' + str(slot))

            self.Instrument[slot-1].set_trigger(type = 'Edge', source = source, level = level, 
                                                mode = mode, edge = edge, nth_event = int(nth_event),
                                                holdoff = holdoff, noise_reject = bool(noise_reject),
                                                hf_reject = bool(hf_reject))
            
        if name.startswith('OSC Acquisition') or name == 'init':
            
            mode = self.getValue('OSC Acquisition Mode - ' + str(slot))
            self.Instrument[slot-1].set_acquisition_mode(mode = mode)


    
    def performOpen(self, options={}):
        '''Perform the operation of opening the instrument connection'''
        self.Moku = {}
        self.Instrument = [[], [] , [] ,[]]  
        self.Instrument_names = [[], [] , [] ,[]] 
        self.init = True
        
        # Connect to the Moku 
        self.Moku = MultiInstrument(self.getValue('IP'), platform_id=4,force_connect = True)
        
        # Load the connections file 
        with open(self.getValue('Connections File')) as f:
            data = f.read()
        connections = json.loads(data)
        
        #Loop through the slots and assign an instrument to each slot
        for i in range(len(self.Instrument)):
            txt_instr = self.getValue('Instrument - Slot' + str(i+1))
            self.Instrument[i] = self.Moku.set_instrument(slot=i+1, 
                                                instrument = eval(txt_instr))
        # #Just a debug method
        # with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
        #     f.write(json.dumps(self.Moku.get_instruments()))
        #     f.write('Start \n') 
        
        #Initialize the ports of the Moku
        self.Moku.set_connections(connections = connections)
        
        with open(self.getValue('Inputs File')) as f:
            data = f.read()
        frontend = json.loads(data)
        
        for i in frontend:
            self.Moku.set_frontend(channel = int(i[-1]), impedance = frontend[i]['impedance'],
                                   coupling = frontend[i]['coupling'], attenuation = frontend[i]['attenuation'])
            
        
        with open(self.getValue('Outputs File')) as f:
            data = f.read()
        output = json.loads(data)
        
        for i in output:
            self.Moku.set_output(channel = int(i[-1]), output_gain = output[i]['output_gain'])
            
        #Loop through each slot and initialize each slot
        for i in range(len(self.Instrument)):
            
            #The init name is passed to ensure that every setting is initialized correctly i.e in the correct order.
            
            name = 'init'
            slot = i+1
            
            if self.getValue('Instrument - Slot' + str(i+1)) == 'WaveformGenerator':
                self.set_WVG(name, slot)
            elif self.getValue('Instrument - Slot' + str(i+1)) == 'ArbitraryWaveformGenerator':
                self.set_AWG(name , slot)
            elif self.getValue('Instrument - Slot' + str(i+1)) == 'SpectrumAnalyzer':
                self.set_SPA(name , slot)         
            elif self.getValue('Instrument - Slot' + str(i+1)) == 'LockInAmp':
                self.set_LIA(name , slot)
            elif self.getValue('Instrument - Slot' + str(i+1)) == 'Oscilloscope':
                self.set_OSC(name , slot)    
            elif self.getValue('Instrument - Slot' + str(i+1)) == 'FrequencyResponseAnalyzer':
                self.set_FRA(name , slot)  
                
        self.Moku.sync()

                
        self.init = False
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
        #self.Moku.relinquish_ownership()
        pass
    
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        
        #This needs to be here not sure why but it breaks if its not here
        quant.setValue(value)
        try:
            slot = int(quant.name[-1])
            text_slt = ' - Slot' + str(slot)
            
            
            ''' Set up the Instruments in their desired Slots and allocate their 
                respective connections using the connections.txt file'''
                
            #Set up the parameters for the Oscilloscope
            if quant.name.startswith('OSC') and self.getValue('Instrument' + text_slt) == 'Oscilloscope':
                
                self.set_OSC(quant.name, slot)
                
                
            #Set up the parameters for the Waveform Generator
            elif quant.name.startswith('WVG') and self.getValue('Instrument' + text_slt) == 'WaveformGenerator':
                
                self.set_WVG(quant.name,slot)
                
            
            #Set up the parameters for the Arbritrary Waveform Generator
            elif quant.name.startswith('AWG') and self.getValue('Instrument' + text_slt) == 'ArbitraryWaveformGenerator':
                
                self.set_AWG(quant.name,slot)
            
            #Set up the parameters for the Arbritrary Waveform Generator
            elif quant.name.startswith('SPA') and self.getValue('Instrument' + text_slt) == 'SpectrumAnalyzer':
                self.set_SPA(quant.name,slot)
                
            #Set up the parameters for the Frequency Response Analyzer
            elif quant.name.startswith('FRA') and self.getValue('Instrument' + text_slt) == 'FrequencyResponseAnalyzer':
            
                self.set_FRA(quant.name,slot)
               
            #Set up the parameters for the Lock In Amplifier
            elif quant.name.startswith('LIA') and self.getValue('Instrument' + text_slt) == 'LockInAmp':
                self.set_LIA(quant.name,slot)
        except:
            pass
        
        return value 
    

    
    def performGetValue(self, quant, options={}):
        
        slot = int(quant.name[-1])
        text_slt = ' - Slot' + str(slot)   
        
        if quant.name.startswith('OSC Ch1') and self.getValue('Instrument' + text_slt) == 'Oscilloscope':
            
            data = self.Instrument[slot-1].get_data()
            
            for channel in ['ch1', 'ch2']:
                trace = quant.getTraceDict(value = np.asarray(data[channel]), x = np.asarray(data['time']))
                self.setValue(quant.name[:6] + channel[-1] + quant.name[7:], trace)
    
            return quant.getValue()
        
        elif quant.name.startswith('LIA Ch1') and self.getValue('Instrument' + text_slt) == 'LockInAmp':
            data = self.Instrument[slot-1].get_data()
            
            for channel in ['ch1', 'ch2']:
                trace = quant.getTraceDict(value = np.asarray(data[channel]), x = np.asarray(data['time']))
                self.setValue(quant.name[:6] + channel[-1] + quant.name[7:], trace)
    
            return quant.getValue()
        
        elif quant.name.startswith('FRA Ch1 Magnitude') and self.getValue('Instrument' + text_slt) == 'FrequencyResponseAnalyzer':
            
            #Wait for the sweeping to be done before collecting the data.
            time.sleep(self.Instrument[slot - 1].get_sweep()['estimated_sweep_time'])
            
            #Get the data from the Moku
            data = self.Instrument[slot-1].get_data()
            
            #The 'data' dict will contain the data from all the channels so you can update in parallel
            for channel in data:
                
                data[channel]['magnitude'] = [0 if x == 'nan' else x for x in data[channel]['magnitude']]
                data[channel]['phase'] = [0 if x == 'nan' else x for x in data[channel]['phase']]
                
                trace_magnitude = quant.getTraceDict(value = np.asarray(data[channel]['magnitude']), 
                                           x = np.asarray(data[channel]['frequency']))
                
                trace_phase  = quant.getTraceDict(value = np.asarray(data[channel]['phase']) , 
                                           x = np.asarray(data[channel]['frequency']))
                
                self.setValue('FRA Ch' + channel[-1] + ' Phase - ' + str(slot) , trace_phase)
                self.setValue('FRA Ch' + channel[-1] + ' Magnitude - ' + str(slot), trace_magnitude)        
            
            return quant.getValue()
        
        elif quant.name.startswith('SPA Ch1') and self.getValue('Instrument' + text_slt) == 'SpectrumAnalyzer':
            
            data = self.Instrument[slot-1].get_data()
            
            for channel in ['ch1', 'ch2']:
                trace = quant.getTraceDict(value = np.asarray(data[channel]), x = np.asarray(data['frequency']))
                self.setValue(quant.name[:6] + channel[-1] + quant.name[7:], trace)
    
            return quant.getValue()
        
        else:
            return quant.getValue()
            
                
