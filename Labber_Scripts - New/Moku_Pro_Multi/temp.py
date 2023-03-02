# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 19:39:55 2022

@author: Triton
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 15:44:28 2022

@author: Triton
"""

from moku.instruments import (MultiInstrument, Oscilloscope, WaveformGenerator,
ArbitraryWaveformGenerator,  SpectrumAnalyzer, LockInAmp, FrequencyResponseAnalyzer)
import time
import numpy as np
from BaseDriver import LabberDriver, Error
import json
import InstrumentDriver

class Driver(InstrumentDriver.InstrumentWorker):
    
    # def __init__(self):
    #     self.IP = '[fe80:0000:0000:0000:7269:79ff:feb0:0470%13]'
    #     self.Instrument = WaveformGenerator(self.IP, force_connect = True)
    #     self.Instrument.relinquish_ownership()

    def performOpen(self, options={}):
        '''Perform the operation of opening the instrument connection'''
        global Moku
        Moku = MultiInstrument('[fe80:0000:0000:0000:7269:79ff:feb0:0470%13]', platform_id=4,force_connect = True)
        global Instrument
        Instrument = [[], [] , [] ,[]]
        with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/connections.txt') as f:
            data = f.read()
        global connections
        connections = json.loads(data)
        
        global Current_Instr
        Current_Instr = ['','','','']

        for i in range(len(Instrument)):
            Instrument[i] = Moku.set_instrument(slot=i+1, 
                                                instrument = eval(self.getValue('Instrument - Slot' + str(i+1))))
            Current_Instr[i] = self.getValue('Instrument - Slot' + str(i+1))


        with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
            f.write(json.dumps(Moku.get_instruments()))
            f.write('Start \n') 
            
        Moku.set_connections(connections = connections)
            
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
        Moku.relinquish_ownership()
        
    
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        
        
        quant.setValue(value)
        
        
        slot = int(quant.name[-1])
        text_slt = ' - Slot' + str(slot)
        
        
        
        ''' Set up the Instruments in their desired Slots and allocate their 
            respective connections using the connections.txt file'''
            
        if quant.name.startswith('Instrument') and self.getValue('Instrument' + text_slt) != Current_Instr[slot-1]:
            
            for i in range(len(Instrument)):
                Instrument[i] = Moku.set_instrument(slot=i+1, 
                                                    instrument = eval(self.getValue('Instrument - Slot' + str(i+1))))
                Current_Instr[i] = self.getValue('Instrument - Slot' + str(i+1))
                
            with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
                f.write(json.dumps(Moku.get_instruments()))
                f.write('Change \n')
            Moku.set_connections(connections = connections)
                
        #Set up the parameters for the Oscilloscope
        elif quant.name.startswith('OSC') and self.getValue('Instrument' + text_slt) == 'Oscilloscope':
            
            timebase = self.getValue('OSC TimeSpan - ' + str(slot))
            Instrument[slot-1].set_timebase(0, timebase)
            
            
        #Set up the parameters for the Waveform Generator
        elif quant.name.startswith('WVG') and self.getValue('Instrument' + text_slt) == 'WaveformGenerator':
            
            channel = int(quant.name[6])
            text_wvg1 = 'WVG Ch' + str(channel) + ' '
            text_wvg2 = ' - ' + str(slot)
            
            func = self.getValue(text_wvg1 + 'Function' + text_wvg2)
            modulation = self.getValue(text_wvg1 + 'Modulation' + text_wvg2)
            
            if func == 'Off':
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func)
            
            elif func == 'Sine':
                amp = self.getValue(text_wvg1 + 'Amplitude' + text_wvg2)
                freq = self.getValue(text_wvg1 + 'Frequency' + text_wvg2)
                phase = self.getValue(text_wvg1 + 'Phase' + text_wvg2)
                dc_offset = self.getValue(text_wvg1 + 'DC Offset' + text_wvg2)
                Instrument[slot-1].generate_waveform(channel = channel,
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
                Instrument[slot-1].generate_waveform(channel = channel,
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
                Instrument[slot-1].generate_waveform(channel = channel,
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
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase = phase,
                                             edge_time=edg_time,
                                             offset = dc_offset,
                                             pulse_width = pulse_width)
                
                
            elif func == 'DC':
                dc = self.getValue(text_wvg1 + 'DC Level' + text_wvg2)
                Instrument[slot-1].generate_waveform(channel = channel,
                                             type = func,
                                             dc_level=dc)

            '''MODULATION SECTION'''
            
            if modulation == 0:
                Instrument[slot-1].disable_modulation(channel = channel)
                
            else:
                
                modulation_type = self.getValue(text_wvg1 + 'Mod Type' + text_wvg2)
                modulation_freq = self.getValue(text_wvg1 + 'Mod Freq' + text_wvg2)
                
                if modulation_type == 'Amplitude':
                    am_depth = self.getValue(text_wvg1 + 'AM Depth' + text_wvg2)
                    Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Amplitude', 
                                              source='Internal', 
                                              depth=am_depth,
                                              frequency= modulation_freq)
                    
                elif modulation_type == 'Frequency':
                    fm_depth = self.getValue(text_wvg1 + 'FM Depth' + text_wvg2)
                    freq = self.getValue('Frequency' + text_wvg2)

                    if fm_depth > freq:
                        fm_depth = freq
                        
                    Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Frequency', 
                                              source='Internal', 
                                              depth=fm_depth,
                                              frequency= modulation_freq)
                    
                elif modulation_type == 'Phase':
                    pm_depth = self.getValue(text_wvg1 + 'PM Depth' + text_wvg2)               
                    Instrument[slot-1].set_modulation(channel=channel, 
                                              type='Phase', 
                                              source='Internal', 
                                              depth=pm_depth,
                                              frequency= modulation_freq)          
                    
                elif modulation_type == 'Burst':
                    pass
                
                elif modulation_type == 'Sweep':
                    pass
        
        #Set up the parameters for the Arbritrary Waveform Generator
        elif quant.name.startswith('AWG') and self.getValue('Instrument' + text_slt) == 'ArbitraryWaveformGenerator':
            
            channel = int(quant.name[6])
            text_1 = 'AWG Ch' + str(channel) + ' '
            text_2 = ' - ' + str(slot)
            
            if not self.getValue(text_1 +'Premade File?'+ text_2):
                
                x = eval(self.getValue(text_1 +'Range of x'+ text_2))
                wave = eval(self.getValue(text_1 + 'f(x) in Python'+ text_2))
                
            elif self.getValue(text_1 +'Premade File?'+ text_2):
                wave = np.genfromtxt(self.getValue(text_1 +'Filename'+ text_2))
                
            amp = self.getValue(text_1 + 'Amplitude' + text_2)
            freq = self.getValue(text_1 + 'Frequency' + text_2)
            sample_rate = self.getValue(text_1 +'Sample Rate'+ text_2)
            Instrument[slot-1].generate_waveform(channel=channel, sample_rate= sample_rate, lut_data=list(wave), 
                                         frequency=freq, amplitude=amp)

            if self.getValue(text_1 +'Modulate'+ text_2) == 'Burst':
                trigger_src = self.getValue(text_1 + 'Trigger Source' + text_2)
                trigger_mode = self.getValue(text_1 + 'Trigger Mode' + text_2)
                trigger_lvl = self.getValue(text_1 + 'Trigger Level' + text_2)
                input_rng = self.getValue(text_1 + 'Input Range' + text_2)
                burst_cycles = int(self.getValue(text_1 + 'Burst Cycles' + text_2))
    
                Instrument[slot-1].burst_modulate(channel = channel,
                                             trigger_source = trigger_src,
                                             trigger_mode=trigger_mode,
                                             burst_cycles=burst_cycles,
                                             trigger_level = trigger_lvl,
                                             input_range = input_rng)

                
            elif self.getValue(text_1 +'Modulate'+ text_2) == 'Pulse':
                dead_cyc = int(self.getValue(text_1 +'Dead Cycles'+ text_2))
                dead_volt = self.getValue(text_1 +'Dead Voltage'+ text_2)
                Instrument[slot-1].pulse_modulate(channel = channel, dead_cycles=dead_cyc, dead_voltage=dead_volt)
                time.sleep(0.5)


            elif self.getValue(text_1 +'Modulate'+ text_2) == 'Off':
                Instrument[slot-1].disable_modulation(channel=channel)
        
        #Set up the parameters for the Arbritrary Waveform Generator
        elif quant.name.startswith('SPA') and self.getValue('Instrument' + text_slt) == 'SpectrumAnalyzer':
            if quant.name.startswith('SPA Freq'):
                f_lower = self.getValue('SPA Freq Lower Bound - ' + str(slot))
                f_higher = self.getValue('SPA Freq Upper Bound - ' + str(slot))
                Instrument[slot-1].set_span(f_lower, f_higher)
                
            elif quant.name.startswith('SPA Window'):
                Instrument[slot-1].set_window(window = self.getValue('SPA Window Function - ' + str(slot)))
 
        elif quant.name.startswith('FRA') and self.getValue('Instrument' + text_slt) == 'FrequencyResponseAnalyzer':
        

            if quant.name.startswith('FRA Output'):
                amp = self.getValue('FRA Output Amplitude - ' + str(slot))
                off = self.getValue('FRA Output Offset - ' + str(slot))
                phase = self.getValue('FRA Output Phase - ' + str(slot))
                for i in range(1,3) :
                    Instrument[slot-1].set_output(i,amp, off)
                    Instrument[slot-1].set_output_phase(i,phase)
            
            elif quant.name.startswith('FRA Sweep'):
                freq1 = self.getValue('FRA Sweep Start Freq - ' + str(slot))
                freq2 = self.getValue('FRA Sweep End Freq - '+ str(slot))
                n_pts = int(self.getValue('FRA Sweep Num-Points - '+ str(slot)))
                avg_t = self.getValue('FRA Sweep Averaging-Time - '+ str(slot))
                avg_cyc = int(self.getValue('FRA Sweep Averaging-Cycles - '+ str(slot)))
                set_t = self.getValue('FRA Sweep Settling-Time - '+ str(slot))
                set_cyc = int(self.getValue('FRA Sweep Settling-Cycles - '+ str(slot)))
                swp_linear = self.getValue('FRA Sweep Linear - '+ str(slot))
                Instrument[slot-1].set_sweep(start_frequency=freq1, stop_frequency=freq2,
                                     num_points=n_pts , averaging_time=avg_t,
                                     settling_time=set_t, averaging_cycles=avg_cyc,
                                     settling_cycles=set_cyc, linear_scale=swp_linear)
                Instrument[slot-1].start_sweep()

                with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
                    f.write(json.dumps(Instrument[slot-1].get_sweep()))
                    f.write('Set \n') 
            elif quant.name.startswith('FRA Harmonic'):
                Instrument[slot-1].set_harmonic_multiplier(int(self.getValue('FRA Harmonic Multiplier - '+ str(slot))))
                
            elif quant.name.startswith('FRA Measurement'):
                Instrument[slot-1].measurement_mode(self.getValue('FRA Measurement Mode - '+ str(slot)) )
                
        elif quant.name.startswith('LIA') and self.getValue('Instrument' + text_slt) == 'LockInAmp':
            if quant.name.startswith('LIA Aux'):
                aux_freq = self.getValue('LIA Aux Frequency - ' + str(slot))
                aux_amp  = self.getValue('LIA Aux Amplitude - ' + str(slot))
                Instrument[slot-1].set_aux_output(frequency = aux_freq, amplitude = aux_amp)
                
                
            elif quant.name.startswith('LIA LPF'):
                lpf_freq = self.getValue('LIA LPF Cutoff Freq - '+ str(slot))
                lpf_slope = self.getValue('LIA LPF Slope - ' + str(slot))
                Instrument[slot-1].set_filter(corner_frequency=lpf_freq , slope=lpf_slope)
            
            elif quant.name.startswith('LIA Output'):
                main_out = self.getValue('LIA Output - Main - ' + str(slot))
                aux_out = self.getValue('LIA Output - Aux - ' + str(slot))
                main_off = self.getValue('LIA Output - Main Offset - ' + str(slot))
                aux_off = self.getValue('LIA Output - Aux Offset - ' + str(slot))
                if main_out == 'X' and aux_out == 'Y or Theta':
                    aux_out = 'Y'
                elif main_out == 'R' and aux_out == 'Y or Theta':
                    aux_out = 'Theta'
                Instrument[slot-1].set_outputs(main=main_out, main_offset=main_off, aux = aux_out, aux_offset = aux_off)
                
        return value 
    
    
    def performGetValue(self, quant, options={}):
        
        slot = int(quant.name[-1])
        text_slt = ' - Slot' + str(slot)   
        
        if quant.name.startswith('OSC Ch') and self.getValue('Instrument' + text_slt) == 'Oscilloscope':
            
            with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
                f.write(json.dumps(Moku.get_instruments()))
                f.write('Read \n') 

            channel = int(quant.name[6])
            data_osc = Instrument[slot-1].get_data()

                
            return quant.getTraceDict(value = np.asarray(data_osc['ch%d' % channel]), x = np.asarray(data_osc['time']))

        elif quant.name.startswith('SPA Ch') and self.getValue('Instrument' + text_slt) == 'SpectrumAnalyzer':
            
            with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
                f.write(json.dumps(Moku.get_instruments()))
                f.write('Read \n') 
                
                
            channel = int(quant.name[6])
            data_sa = Instrument[slot-1].get_data()

            return quant.getTraceDict(value = np.asarray(data_sa['ch%d' % channel]), x = np.asarray(data_sa['frequency']))
            
        elif quant.name.startswith('FRA Ch1 Magnitude') and self.getValue('Instrument' + text_slt) == 'FrequencyResponseAnalyzer':

            with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
                f.write(json.dumps(Instrument[slot-1].get_sweep()))
                f.write('Read \n') 
            with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/debug.txt', 'a') as f:
                f.write(json.dumps(Moku.get_instruments()))
                f.write('Read \n') 
                

            channel = int(quant.name[6])
            time.sleep(Instrument[slot-1].get_sweep()['estimated_sweep_time'])
            data_fra = Instrument[slot-1].get_data()
            
            with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/data.txt', 'a') as f:
                f.write(json.dumps(Instrument[slot-1].get_data()))
                f.write('Read \n') 
         
            magnitude_fra = quant.getTraceDict(value = np.asarray(data_fra['ch%d' % channel]['magnitude']), 
                                       x = np.asarray(data_fra['ch%d' % channel]['frequency']))
            
            phase_fra  = quant.getTraceDict(value = np.asarray(data_fra['ch%d' % channel]['phase']) , 
                                       x = np.asarray(data_fra['ch%d' % channel]['frequency']))
            
            #self.setValue('FRA Ch' + str(channel) + ' Phase - ' + str(slot), magnitude_fra)
            #self.setValue('FRA Ch' + str(channel) + ' Phase - ' + str(slot), phase_fra)
            return magnitude_fra

        else:
            
            return quant.getValue()
            
                