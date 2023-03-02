# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:09:51 2022

@author: Triton
"""
import json

connections = [dict(source = "Input1", destination = "Slot1InA"),
               dict(source = "Slot4OutA", destination = "Slot1InB"),

               
               dict(source = "Input2", destination = "Slot2InA"),
               dict(source = "Slot4OutA", destination = "Slot2InB"),
               
               dict(source = "Slot3OutA", destination = "Output1"),
               dict(source = "Slot3OutB", destination = "Output2"),
               
               dict(source = "Slot4OutA", destination = "Output3"),
               dict(source = "Slot4OutB", destination = "Output4")]

with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/connections.txt', 'w') as f:
    f.write(json.dumps(connections))
    
frontend = {}

frontend['Input1'] = dict(impedance = '1MOhm', coupling = 'DC', attenuation = '-20dB')
frontend['Input2'] = dict(impedance = '1MOhm', coupling = 'DC', attenuation = '-20dB')

with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/frontend.txt', 'w') as f:
    f.write(json.dumps(frontend))
    

output = {}

frontend['Output1'] = dict(output_gain = '0dB')
frontend['Output2'] = dict(output_gain = '0dB')
frontend['Output3'] = dict(output_gain = '0dB')
frontend['Output4'] = dict(output_gain = '0dB')

with open('C:/Users/Triton/Documents/Labber_Scripts/Moku_Pro_Multi/output.txt', 'w') as f:
    f.write(json.dumps(output))