from moku.instruments import WaveformGenerator
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
        Instrument = WaveformGenerator(self.getValue('IP'), force_connect = True)
        
        #for i in range(1,5):
        #    text = ' - (Ch ' + str(i) + ')'        
        #    self.setValue('Function' + text, 'Off')        
        # for i in range(1,5):
        #     Instrument.generate_waveform(channel = i,
        #                                  type = 'Off')
        
        
    def performClose(self, bError=False, options={}):
        '''Perform the close instrument connection operation'''
        for i in range(1,5):
            Instrument.generate_waveform(channel = i,
                                        type = 'Off')
        Instrument.relinquish_ownership()

    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation. This function should
        return the actual value set by the instrument"""

        quant.setValue(value)
        try:
            channel = int(quant.name[-1])
            
            text = ' - Ch' + str(channel)
            
            func = self.getValue('Function' + text)
            modulation = self.getValue('Modulation' + text)
            
            if func == 'Off':
                Instrument.generate_waveform(channel = channel,
                                             type = func)
            
            elif func == 'Sine':
                amp = self.getValue('Amplitude' + text)
                freq = self.getValue('Frequency' + text)
                phase = self.getValue('Phase' + text)
                dc_offset = self.getValue('DC Offset' + text)
                Instrument.generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             offset = dc_offset,
                                             phase = phase)
            
            elif func == 'Square':
                amp = self.getValue('Amplitude' + text)
                freq = self.getValue('Frequency' + text)
                phase = self.getValue('Phase' + text)
                duty = self.getValue('Duty Cycle' + text)
                dc_offset = self.getValue('DC Offset' + text)
                Instrument.generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase= phase,
                                             offset = dc_offset,
                                             duty=duty)
                
            elif func == 'Ramp':
                amp = self.getValue('Amplitude' + text)                        
                freq = self.getValue('Frequency' + text)
                phase = self.getValue('Phase' + text)
                symm = self.getValue('Ramp Symmetry' + text)
                dc_offset = self.getValue('DC Offset' + text)
                Instrument.generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase = phase,
                                             offset = dc_offset,
                                             symmetry=symm)
                
            elif func == 'Pulse':
                amp = self.getValue('Amplitude' + text)
                freq = self.getValue('Frequency' + text)
                phase = self.getValue('Phase' + text)
                edg_time = self.getValue('Edge Time' + text)
                dc_offset = self.getValue('DC Offset' + text)
                pulse_width = self.getValue('Pulse Width' + text)
                Instrument.generate_waveform(channel = channel,
                                             type = func,
                                             amplitude=amp,
                                             frequency=freq,
                                             phase = phase,
                                             edge_time=edg_time,
                                             offset = dc_offset,
                                             pulse_width = pulse_width)
                
                
            elif func == 'DC':
                dc = self.getValue('DC Level' + text)
                Instrument.generate_waveform(channel = channel,
                                             type = func,
                                             dc_level=dc)
    
            '''MODULATION SECTION'''
            
            if modulation == 0:
                Instrument.disable_modulation(channel = channel)
                
            else:
                
                modulation_type = self.getValue('Mod Type' + text)
                modulation_freq = self.getValue('Mod Freq' + text)
                
                if modulation_type == 'Amplitude':
                    am_depth = self.getValue('AM Depth' + text)
                    Instrument.set_modulation(channel=channel, 
                                              type='Amplitude', 
                                              source='Internal', 
                                              depth=am_depth,
                                              frequency= modulation_freq)
                    
                elif modulation_type == 'Frequency':
                    fm_depth = self.getValue('FM Depth' + text)
                    freq = self.getValue('Frequency' + text)
    
                    if fm_depth > freq:
                        fm_depth = freq
                        
                    Instrument.set_modulation(channel=channel, 
                                              type='Frequency', 
                                              source='Internal', 
                                              depth=fm_depth,
                                              frequency= modulation_freq)
                    
                elif modulation_type == 'Phase':
                    pm_depth = self.getValue('PM Depth' + text)               
                    Instrument.set_modulation(channel=channel, 
                                              type='Phase', 
                                              source='Internal', 
                                              depth=pm_depth,
                                              frequency= modulation_freq)          
                    
                elif modulation_type == 'Burst':
                    pass
                
                elif modulation_type == 'Sweep':
                    pass
                
                
            # if quant.name.startswith('Function'):
            #     new_value = output_func['type']
            #     return new_value
            
            
            # elif quant.name.startswith('Frequency'):
            #      new_value = output_func['frequency']
            #      quant.setValue(new_value)
            #      return new_value
             
                
            # elif quant.name.startswith('Amplitude'):
            #     new_value = output_func['amplitude']
            #     quant.setValue(new_value)
            #     return new_value
            
            
            # elif quant.name.startswith('Phase'):
            #     new_value = output_func['phase']      
            #     quant.setValue(new_value)
            #     return new_value
            # else:
        except:
            pass
        
        return value

  

    def performGetValue(self, quant, options={}):
        
        '''Using the Summary() Function to determine the various parameters set
'''
        value = quant.getValue()
        return value
if __name__ == '__main__':
    pass