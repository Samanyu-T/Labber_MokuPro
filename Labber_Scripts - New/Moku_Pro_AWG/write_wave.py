# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:57:25 2022

@author: Triton
"""
import numpy as np
import scipy.stats as stats


mu = 0
sigma = 1
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
wave = stats.norm.pdf(x, mu, sigma)
wave = wave*0
np.savetxt('zero_wave.txt', wave)