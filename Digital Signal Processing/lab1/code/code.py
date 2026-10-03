##########
# 1

# 1.1
# Length = 256 (samples)
# N = 256 (window)


# necessary imports
import numpy as np 
import matplotlib.pyplot as plt
import math
import cmath
import scipy
from scipy import signal
from scipy.fft import fft, fftshift

# definitions
pi = np.pi
L = 256
N = 256
norm = (2*pi) / N 					# when plotting fft, x-axis is samples(k) and not frequency 
									# since w = (2pi/N)*k, I use norm to fix that

# make n 
n = np.linspace(0, L-1, L)			# 0,1,...,255 samples

# make x1[n]
A1 = 1
w1 = pi / 9
ph1 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x1 = np.cos(w1*n + ph1)
im_x1 = np.sin(w1*n + ph1)
x1 = A1*(re_x1 + 1j*im_x1)
# print(x1)

# make x2[n]
A2 = 0.9
w2 = np.pi / 5
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# print(x2)

# make w_hamn[n]
w_hamn = scipy.signal.windows.hamming(N, sym=True)


# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(norm*n, absY)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()
print(peaks)

# find minimum Dw 
# To find minimum Dw we start with w2 = w1 and we increase with step 0.005 until python undertands two different peaks
# make x2[n]
A2 = 0.9
i = 0.04
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)


# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(n, abs(Y))
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)						# prints the peaks of the DFT that are above 100
#print(np.argmax(np.abs(Y)))		# index that corresponds to the peak of the DFT of the sinusoid


# case in which peaks cannot be distinguished
# Dw = 0.04 < 0.05
A2 = 0.9
i = 0.03
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)


# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(norm*n, abs(Y)) 
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)						# prints the peaks of the DFT that are above 100
#print(np.argmax(np.abs(Y)))		# index that corresponds to the peak of the DFT of the sinusoid


# 1.2
# 512
# Length = 512


# necessary imports
import numpy as np 
import matplotlib.pyplot as plt
import math
import cmath
import scipy
from scipy import signal
from scipy.fft import fft, fftshift

# definitions
pi = np.pi
L = 256
N = 512
norm = (2*pi) / N 						# when plotting fft, x-axis is samples(k) and not frequency 
										# since w = (2pi/N)*k, I use norm to fix that

# make n 
n = np.linspace(0, L-1, L)				# 0,1,...,255 samples


# make x1[n]
A1 = 1
w1 = pi / 9
ph1 = np.random.uniform(0.1, 2*pi)		# random phase in [0, 2pi]
re_x1 = np.cos(w1*n + ph1)
im_x1 = np.sin(w1*n + ph1)
x1 = A1*(re_x1 + 1j*im_x1)
# zero padding
x1 = np.pad(x1, (0, L), 'constant')
# print(x1)

# make x2[n]
A2 = 0.9
w2 = np.pi / 5
ph2 = np.random.uniform(0.1, 2*pi)		# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# zero padding
x2 = np.pad(x2, (0, L), 'constant')
# print(x2)

# make w_hamn[n]
w_hamn = scipy.signal.windows.hamming(N, sym=True)

# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(absY)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()
print(peaks)

# find minimum Dw 
# To find minimum Dw we start with w2 = w1 and we increase with step 0.005 until python undertands two different peaks
# make x2[n]
A2 = 0.9
i = 0.05
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# zero padding
x2 = np.pad(x2, (0, L), 'constant')

# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(absY) 
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)							# prints the peaks of the DFT that are above 100
print(np.argmax(np.abs(Y)))				# index that corresponds to the peak of the DFT of the sinusoid

# case in which peaks cannot be distinguished
# Dw = 0.04 < 0.05
A2 = 0.9
i = 0.04
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)		# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# zero padding
x2 = np.pad(x2, (0, L), 'constant')

# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(absY) 
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)							# prints the peaks of the DFT that are above 100
print(np.argmax(np.abs(Y)))				# index that corresponds to the peak of the DFT of the sinusoid


# 1.2
# 1024
# Length = 1024


# necessary imports
import numpy as np 
import matplotlib.pyplot as plt
import math
import cmath
import scipy
from scipy import signal
from scipy.fft import fft, fftshift

# definitions
pi = np.pi
L = 256
N = 1024

# make n 
n = np.linspace(0, L-1, L)	# 0,1,...,255 samples

# make x1[n]
A1 = 1
w1 = pi / 9
ph1 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x1 = np.cos(w1*n + ph1)
im_x1 = np.sin(w1*n + ph1)
x1 = A1*(re_x1 + 1j*im_x1)
# zero padding
x1 = np.pad(x1, (0, 3*L), 'constant')
# print(x1)

# make x2[n]
A2 = 0.9
w2 = np.pi / 5
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# zero padding
x2 = np.pad(x2, (0, 3*L), 'constant')
# print(x2)

# make w_hamn[n]
w_hamn = scipy.signal.windows.hamming(N, sym=True)

# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 50)
plt.plot(absY)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()
print(peaks)

# find minimum Dw 
# To find minimum Dw we start with w2 = w1 and we increase with step 0.005 until python undertands two different peaks
# make x2[n]
A2 = 0.9
i = 0.03
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# zero padding
x2 = np.pad(x2, (0, 3*L), 'constant')

# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 50)
plt.plot(absY) 
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)						# prints the peaks of the DFT that are above 100
print(np.argmax(np.abs(Y)))			# index that corresponds to the peak of the DFT of the sinusoid


# case in which peaks cannot be distinguished
# Dw = 0.04 < 0.05
A2 = 0.9
i = 0.023
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# zero padding
x2 = np.pad(x2, (0, 3*L), 'constant')

# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 50)
plt.plot(absY) 
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)						# prints the peaks of the DFT that are above 100
print(np.argmax(np.abs(Y)))			# index that corresponds to the peak of the DFT of the sinusoid

# 1.3
# 512
# Length = 512


# necessary imports
import numpy as np 
import matplotlib.pyplot as plt
import math
import cmath
import scipy
from scipy import signal
from scipy.fft import fft, fftshift

# definitions
pi = np.pi
L = 512
N = 512

# make n 
n = np.linspace(0, L-1, L)	# 0,1,...,511 samples

# make x1[n]
A1 = 1
w1 = pi / 9
ph1 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x1 = np.cos(w1*n + ph1)
im_x1 = np.sin(w1*n + ph1)
x1 = A1*(re_x1 + 1j*im_x1)
# print(x1)

# make x2[n]
A2 = 0.9
w2 = w1 + 0.045
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# print(x2)

# make w_hamn[n]
w_hamn = scipy.signal.windows.hamming(N, sym=True)

# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(n, absY)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()
print(peaks)

# find minimum Dw 
# To find minimum Dw we start with w2 = w1 and we increase with step 0.005 until python undertands two different peaks
# make x2[n]
A2 = 0.9
i = 0.027
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)


# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(n, abs(Y)) 
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)						# prints the peaks of the DFT that are above 100
print(np.argmax(np.abs(Y)))			# index that corresponds to the peak of the DFT of the sinusoid


# case in which peaks cannot be distinguished
# Dw = 0.02 < 0.027
A2 = 0.9
i = 0.02
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)


# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(n, abs(Y)) 
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)						# prints the peaks of the DFT that are above 100
print(np.argmax(np.abs(Y)))			# index that corresponds to the peak of the DFT of the sinusoid

# 1.3
# 1024
# Length = 1024


# necessary imports
import numpy as np 
import matplotlib.pyplot as plt
import math
import cmath
import scipy
from scipy import signal
from scipy.fft import fft, fftshift

# definitions
pi = np.pi
L = 1024
N = 1024

# make n 
n = np.linspace(0, L-1, L)	# 0,1,...,1023 samples

# make x1[n]
A1 = 1
w1 = pi / 9
ph1 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x1 = np.cos(w1*n + ph1)
im_x1 = np.sin(w1*n + ph1)
x1 = A1*(re_x1 + 1j*im_x1)
# print(x1)

# make x2[n]
A2 = 0.9
w2 = w1 + 0.045
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
# print(x2)

# make w_hamn[n]
w_hamn = scipy.signal.windows.hamming(N, sym=True)

# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(n, absY)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()
print(peaks)

# find minimum Dw 
# To find minimum Dw we start with w2 = w1 and we increase with step 0.005 until python undertands two different peaks
# make x2[n]
A2 = 0.9
i = 0.015
w2 = w1 + i
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)


# make y[n]
y = w_hamn * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
peaks = scipy.signal.find_peaks(absY, height = 100)
plt.plot(n, abs(Y)) 
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()			
print(peaks)						# prints the peaks of the DFT that are above 100
print(np.argmax(np.abs(Y)))			# index that corresponds to the peak of the DFT of the sinusoid

# 1.4
# hamming
# Length = 256
# N = 1024
# square window


# necessary imports
import numpy as np 
import matplotlib.pyplot as plt
import math
import cmath
import scipy
from scipy import signal
from scipy.fft import fft, fftshift

# definitions
pi = np.pi
L = 256
N = 1024

# make n 
n = np.linspace(0, L-1, L)	# 0,1,...,255 samples

# make x1[n]
A1 = 1
w1 = 0.35*pi
ph1 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x1 = np.cos(w1*n + ph1)
im_x1 = np.sin(w1*n + ph1)
x1 = A1*(re_x1 + 1j*im_x1)
x1 = np.pad(x1, (0, 3*L), 'constant')
# print(x1)

# make x2[n]
A2 = 0.9
w2 = 0.4*pi
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
x2 = np.pad(x2, (0, 3*L), 'constant')
# print(x2)

# make w_square[n]
w_hamming = scipy.signal.windows.hamming(N, sym=True)

# make y[n]
y = w_hamming * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
plt.plot(absY)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()

# 1.4
# square
# Length = 256
# N = 1024
# square window


# necessary imports
import numpy as np 
import matplotlib.pyplot as plt
import math
import cmath
import scipy
from scipy import signal
from scipy.fft import fft, fftshift

# definitions
pi = np.pi
L = 256
N = 1024

# make n 
n = np.linspace(0, L-1, L)	# 0,1,...,255 samples

# make x1[n]
A1 = 1
w1 = 0.35*pi
ph1 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x1 = np.cos(w1*n + ph1)
im_x1 = np.sin(w1*n + ph1)
x1 = A1*(re_x1 + 1j*im_x1)
x1 = np.pad(x1, (0, 3*L), 'constant')
# print(x1)

# make x2[n]
A2 = 0.9
w2 = 0.4*pi
ph2 = np.random.uniform(0.1, 2*pi)	# random phase in [0, 2pi]
re_x2 = np.cos(w2*n + ph2)
im_x2 = np.sin(w2*n + ph2)
x2 = A2*(re_x2 + 1j*im_x2)
x2 = np.pad(x2, (0, 3*L), 'constant')
# print(x2)

# make w_square[n]
w_square = np.ones(N)
# w_square = np.pad(w_square, (0, 3*L), 'constant')
# make y[n]
y = w_square * (x1 + x2)

# calculate DFT of y[n]
Y = np.fft.fft(y)
absY = abs(Y)
plt.plot(absY)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()


##########
# 2
# Length = 1000

# necessary imports
import math
import cmath
from scipy import signal
import scipy
import os
import numpy as np
import scipy as sp
import librosa
import matplotlib.pyplot as plt
import IPython
import sounddevice as sd
import soundfile as sf
import IPython.display as ipd
import pyaudio
import wave

# definitions
L = 1000
N = 1000
pi = np.pi 

# make n 
n = np.linspace(0, L-1, L)	# 0,1,...,999 samples

# make di[n]
d0 = np.sin(0.7217*n) + np.sin(1.0247*n)
d1 = np.sin(0.5346*n) + np.sin(0.9273*n)
d2 = np.sin(0.5346*n) + np.sin(1.0247*n)
d3 = np.sin(0.5346*n) + np.sin(1.1328*n)
d4 = np.sin(0.5906*n) + np.sin(0.9273*n)
d5 = np.sin(0.5906*n) + np.sin(1.0247*n)
d6 = np.sin(0.5906*n) + np.sin(1.1328*n)
d7 = np.sin(0.6535*n) + np.sin(0.9273*n)
d8 = np.sin(0.6535*n) + np.sin(1.0247*n)
d9 = np.sin(0.6535*n) + np.sin(1.1328*n)

tones = np.array([d0, d1, d2, d3, d4, d5, d6, d7, d8, d9])


# 2.2
D5 = np.fft.fft(d5)
absD5 = abs(D5)
plt.plot(n, absD5)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()
peaks5 = scipy.signal.find_peaks(absD5, height = 400)
print(peaks5)

-D8 = np.fft.fft(d8)
absD8 = abs(D8)
plt.plot(n, absD8)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.show()
peaks8 = scipy.signal.find_peaks(absD8, height = 400)
print(peaks8)

# 2.3
d1_100 = np.pad(d0, (0, 100), 'constant')	# 1st digit is 0
d2_100 = np.pad(d3, (0, 100), 'constant')	# 2nd digit is 3
d3_100 = np.pad(d1, (0, 100), 'constant')	# 3d digit is 1
d4_100 = d3_100								# 4th digit is 1
d5_100 = np.pad(d9, (0, 100), 'constant')	# 5th digit is 9
d6_100 = np.pad(d2, (0, 100), 'constant')	# 6th digit is 2
d7_100 = d1_100								# 7th digit is 0
d8_lst = d4 								# last digit is 4

signal = np.concatenate((d1_100, d2_100, d3_100, d4_100, d5_100, d6_100, d7_100, d8_lst))

# print(np.shape(signal))

# print(np.shape(signal))
sf.write('tone sequence.wav', signal, 7000)

# 2.4
# rectangular
w_rect = np.ones(N)

d1_rect = d0 * w_rect
D1_rect = np.fft.fft(d1_rect)
D1_abs_rect = np.abs(D1_rect)
# plt.plot(D1_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d2_rect = d3 * w_rect
D2_rect = np.fft.fft(d2_rect)
D2_abs_rect = np.abs(D2_rect)
# plt.plot(D2_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d3_rect = d1 * w_rect
D3_rect = np.fft.fft(d3_rect)
D3_abs_rect = np.abs(D3_rect)
# plt.plot(D3_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d4_rect = d9 * w_rect
D4_rect = np.fft.fft(d4_rect)
D4_abs_rect = np.abs(D4_rect)
# plt.plot(D3_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d5_rect = d2 * w_rect
D5_rect = np.fft.fft(d5_rect)
D5_abs_rect = np.abs(D5_rect)
# plt.plot(D5_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d6_rect = d2 * w_rect
D6_rect = np.fft.fft(d6_rect)
D6_abs_rect = np.abs(D6_rect)
# plt.plot(D6_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d7_rect = d0 * w_rect
D7_rect = np.fft.fft(d7_rect)
D7_abs_rect = np.abs(D7_rect)
# plt.plot(D7_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d8_rect = d4 * w_rect
D8_rect = np.fft.fft(d8_rect)
D8_abs_rect = np.abs(D8_rect)
# plt.plot(D2_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()



# hamming
w_hamming = np.hamming(N)

d1_hamm = d0 * w_hamming
D1_hamm = np.fft.fft(d1_hamm)
D1_abs_hamm = np.abs(D1_hamm)
# plt.plot(D1_abs_hamm)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d2_hamm = d3 * w_hamming
D2_hamm = np.fft.fft(d2_hamm)
D2_abs_hamm = np.abs(D2_hamm)
# plt.plot(D2_abs_hamm)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d3_hamm = d1 * w_hamming
D3_hamm = np.fft.fft(d3_hamm)
D3_abs_hamm = np.abs(D3_hamm)
# plt.plot(D3_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d4_hamm = d9 * w_hamming
D4_hamm = np.fft.fft(d4_hamm)
D4_abs_hamm = np.abs(D4_hamm)
# plt.plot(D3_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d5_hamm = d2 * w_hamming
D5_hamm = np.fft.fft(d5_hamm)
D5_abs_hamm = np.abs(D5_hamm)
# plt.plot(D5_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d6_rect = d2 * w_rect
D3_rect = np.fft.fft(d6_rect)
D6_abs_rect = np.abs(D6_rect)
# plt.plot(D6_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d7_hamm = d0 * w_hamming
D7_hamm = np.fft.fft(d7_hamm)
D7_abs_hamm = np.abs(D7_hamm)
# plt.plot(D7_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()

d8_hamm = d4 * w_hamming
D8_hamm = np.fft.fft(d8_hamm)
D8_abs_hamm = np.abs(D8_hamm)
# plt.plot(D2_abs_rect)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()



# 2.5

# telephone frequencies 
#				 0 		  1  	 2 		 3 		 4 		 5  	 6
W = np.array([0.5346, 0.5906, 0.6535, 0.7217, 0.9273, 1.0247, 1.1328])
# compute k = N*W/2pi
k = N*W/(2*pi)
# print(np.shape(k))
k = np.around(k)
#					 0 			  1 			 2 			  3 			4 			  5 			 6			  7 			8  			 9	
index_tones = [(k[3], k[5]), (k[0], k[4]), (k[0], k[5]), (k[0], k[6]), (k[1], k[4]), (k[1], k[5]), (k[1], k[6]), (k[2], k[4]), (k[2], k[5]), (k[2], k[6])]

print(index_tones)

# 2.6
# print("2.6 START")
# print(index_tones)
def ttdecode(*input_signal):
	count_1000 = 0 
	output_digits = []
	samples_1000 = np.array(n)
	flag = 0
	for idx,sample in enumerate(input_signal):
		
		if (sample != 0.0 and flag == 0) or idx == 0:
			i = 0
			flag = 1
		
		if i == 999:
			# print(i)
			samples_1000[i] = sample
			# print(sample)
			# print(samples_1000[i])
			i = 0
			flag = 0
			samples_1000_fft = np.fft.fft(samples_1000)
			abs_samples = abs(samples_1000_fft)
			# plt.plot(abs_samples)
			# plt.show()
			peaks = scipy.signal.find_peaks(abs(samples_1000_fft), height = 300)
			useful = peaks[0]
			#print(useful)
			digit = index_tones.index((useful[0],useful[1]))
			output_digits.append(digit)
		
		if flag == 1:
			samples_1000[i] = sample
			# if i == 566:
			#	print(sample)
			#	print(samples_1000[i])
			i = i + 1 

	if i == 999:
		# print(i)
		samples_1000[i] = sample
		# print(sample)
		# print(samples_1000[i])
		i = 0
		flag = 0
		samples_1000_fft = np.fft.fft(samples_1000)
		abs_samples = abs(samples_1000_fft)
		# plt.plot(abs_samples)
		# plt.show()
		peaks = scipy.signal.find_peaks(abs(samples_1000_fft), height = 300)
		useful = peaks[0]
		#print(useful)
		digit = index_tones.index((useful[0],useful[1]))
		output_digits.append(digit)
	
	return output_digits

easy_sig = np.load('easy_sig.npy')
hard_sig = np.load('hard_sig.npy')
print(ttdecode(*signal))
print(ttdecode(*easy_sig))
print(ttdecode(*hard_sig))




##########
# 3

# 3.1
# necessary imports
import math
import cmath
from scipy import signal
import scipy
import os
import numpy as np
import scipy as sp
import librosa
import matplotlib.pyplot as plt
import IPython
import sounddevice as sd
import soundfile as sf
import IPython.display as ipd
import pyaudio
import wave

# definitions
pi = np.pi 



# read the file
why_do_you_think, fs = sf.read('speech_utterance.wav')	# fs = 16kHz


# plt.plot(why_do_you_think)
# plt.xlabel('x axis label')
# plt.ylabel('y axis label')
# plt.show()
# print(fs)
 
# Zero Crossing Rate
# make dirac 
d = np.array([])
d = np.append(d,[0])
d = np.append(d,[1])
# make x[m-1]
why_do_you_think_shift = np.convolve(why_do_you_think, d)
why_do_you_think = np.append(why_do_you_think, [0])						# to make sizes equal
diff = np.sign(why_do_you_think) - np.sign(why_do_you_think_shift)

t = 20*0.001
while t < 51*0.001:			# 20ms-50ms with step 5ms 
	
	N = int(t*fs) 			# samples
	# print(N)
	# Energy
	square_signal = np.square(abs(why_do_you_think))
	window_hamming = np.hamming(N)
	E = np.convolve(square_signal, window_hamming)
	plt.plot(E, color = 'red')
	plt.show()

	# Zero Crossing Rate
	# calculate x[m-1] = x[m] convolution d[m]
	window_rectangular = np.ones(N)
	Z = np.convolve(np.abs(diff), window_rectangular)
	plt.plot(Z, color = 'black')
	plt.show()

	t = t + 5*0.001


# 3.2
# necessary imports
import math
import cmath
from scipy import signal
import scipy
import os
import numpy as np
import scipy as sp
import librosa
import matplotlib.pyplot as plt
import IPython
import sounddevice as sd
import soundfile as sf
import IPython.display as ipd
import pyaudio
from pydub import AudioSegment
import wave

stereo_audio = AudioSegment.from_file("music.wav", format="wav")
mono_audios = stereo_audio.split_to_mono()
mono_left = mono_audios[0].export("mono_left.wav", format="wav")
mono_right = mono_audios[1].export("mono_right.wav", format="wav")
# mono_audio = (mono_audios[0] + mono_audios[1]) / 2
music_left, fs = sf.read('mono_left.wav')
music_right, fs = sf.read('mono_right.wav')
music = (music_left + music_right) / 2

# Zero Crossing Rate
# make dirac 
d = np.array([])
d = np.append(d,[0])
d = np.append(d,[1])
# make x[m-1]
music_shift = np.convolve(music, d)
music = np.append(music, [0])		# to make sizes equal
diff = np.sign(music) - np.sign(music_shift)

t = 20*0.001
while t < 51*0.001:			# 20ms-50ms with step 5ms 
	
	N = int(t*fs) 			# samples
	print(N)
	# Energy
	square_signal = np.square(abs(music))
	window_hamming = np.hamming(N)
	E = np.convolve(square_signal, window_hamming)
	plt.plot(E, color = 'red')
	plt.show()

	# Zero Crossing Rate
	# calculate x[m-1] = x[m] convolution d[m]
	window_rectangular = np.ones(N)
	Z = np.convolve(np.abs(diff), window_rectangular)
	plt.plot(Z, color = 'black')
	plt.show()

	t = t + 5*0.001
