##########
# Imports
##########
import math
import cmath
from scipy import signal
import scipy
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from pydub import AudioSegment
import wave

##############
# Definitions
##############
N = 512				# samples per window 
fs = 44100			# sampling frequency
PN = 90.302			# just a constant 
old_size = 603285
e = math.e 			# Euler's constant



###########
# Step 1.0
###########

# Stereo -> Mono
# ---------------
# To  convert stereo to mono, 
# I find the average of the channels
stereo_audio = AudioSegment.from_file("music.wav", format="wav")	# two channels
mono_audios = stereo_audio.split_to_mono()
mono_left = mono_audios[0].export("mono_left.wav", format="wav")
mono_right = mono_audios[1].export("mono_right.wav", format="wav")
# mono_audio = (mono_audios[0] + mono_audios[1]) / 2
music_left, fs = sf.read('mono_left.wav')
music_right, fs = sf.read('mono_right.wav')
music = (music_left + music_right) / 2		# one channel, average of two

# plt.plot(music)
# plt.xlabel('samples')
# plt.ylabel('signal')
# plt.show()


# Normalization
# ------------- 
# To normalize the signal s[n]. I follow steps:
# 1) Find |s[n]|
# 2) Find max = maximum(|s[n]|)
# 3) x[n] = s[n] / max
abso = np.absolute(music)
amp = np.max(abso)
norm_music = music / amp
# plot the signal in 2 windows
# plt.plot(norm_music[N:3*N])
# plt.xlabel('samples')
# plt.ylabel('signal')
# plt.show()

# Zero Padding
# ------------
# print(np.size(norm_music))
# The size of the signal is 603285 samples (using np.size())
# In order to take windows of 512 samples I add zeros to the signal
# such as new_size mod 512 = 0. I must add old_size mod 512 zeros
zeros_to_add = N - old_size % N 
norm_music = np.pad(norm_music, (0, zeros_to_add), 'constant')	# zero padding
new_size = np.size(norm_music)
# print(np.size(norm_music))
# print(np.size(norm_music) / 512)
# Now, I have 1179 windows each one of 512 samples 
wind_num = int(np.size(norm_music) / N) 		# = int(1179.0) = 1179


# make bark function 
# Hz -> barks
def bf(f):
	c = 13*np.arctan(0.00076*f) + 3.5*np.arctan((f/7500)*(f/7500))
	return c  
# print(bf(15000))
# make bark function
# samples -> barks
def bk(k):
	f = fs * (k / N) 
	return bf(f)

# b function neebs a lot of time
# I save the values in an array
b = []
for i in range(0,256):
	b.append(bk(i))


###########
# Step 1.1
###########

# Windowing
# ---------
# I want:
# 1) hamming windows 
# 2) of 512 samples
w = np.hamming(N)		# hamming window of N = 512 samples
# print(np.size(w))		# check that size = 512
# I want 1179 windows
x_w = []		# has the after windowing samples
for i in range(0, new_size):
	x_w.append(w[i % N] * norm_music[i])
# print(x_w[0])
# print(x_w[256])

x_w_array = []		# it is a matrix of submatrices. Each submatrix is one window
for i in range(0, wind_num):
	helper = []
	for j in range(i, N+i):
		helper.append(x_w[j])
	x_w_array.append(helper)


# Power Spectrum
# --------------
P = []
for i in range(0, wind_num):
	helper = x_w_array[i]				# one window of 512 samples
	Helper = np.fft.fft(helper)
	Ampl = abs(Helper)
	helper = []
	for i in range(0, int(N/2)):		# each matrix has 512 samples, but I need 256
		helper.append(Ampl[i])
	P.append(PN + 10 * np.log10(helper) * np.log10(helper))	

######################
# plot power spectrum
# plt.plot(P[100])
# plt.xlabel('samples')
# plt.ylabel('Power Spectrum')
# plt.show()

###########
# Step 1.2
###########

def check(P, k):
	if k < 3 or k > 250: return 0
	if P[k] <= P[k+1] or P[k] <= P[k-1]: return 0
	if 2 < k and k < 63: 
		if P[k] > P[k+2] and P[k] > P[k-2]: return 1
		else: return 0 
	elif 63 <= k and k < 127:
		for i in range(2,4):
			if P[k] <= (P[k+i] + 7) or P[k] <= (P[k-i] + 7): return 0
		return 1
	elif 127 <= k and k <=250:
		for i in range(2,7):
			if (P[k] <= P[k+i] + 7) or (P[k] <= P[k-i] + 7): return 0
		return 1

St_array = []	# 1179 windows
for i in range(0, 1179):
	helper = P[i]
	St_help = []		# only one window
	for j in range(0, 256):
		St_help.append(check(helper, j))
	St_array.append(St_help)

########################
# plot St_array[100]
# plt.stem(St_array[100])
# plt.xlabel('samples')
# plt.ylabel('mask')
# plt.show()

# Find the average number of masks per window
mean = 0
for w in range(0, wind_num):
	helper = np.array(St_array[w])
	helper = np.where(helper > 0)
	helper = helper[0]
	mean = mean + np.size(helper)
mean = mean / wind_num
# print(mean)

# Find the variance from mean per window
variance = 0
for w in range(0, wind_num):
	helper = np.array(St_array[w])
	helper = np.where(helper > 0)
	helper = helper[0]
	variance = abs(mean - np.size(helper))
variance = variance / wind_num
# print(variance)

Ptm_array = []		# 1179 windows
for i in range(0 ,wind_num):
	Ptm = []
	for j in range(0, 256):
		if St_array[i][j] == 0: 
			Ptm.append(0)
		else: 
			Ptm.append(10 * np.log10(pow(10, 0.1*P[i][j-1]) + pow(10, 0.1*P[i][j]) + pow(10, 0.1*P[i][j-1])))
	Ptm_array.append(Ptm)

######################	
# plot Ptm_array[100]
# plt.stem(Ptm_array[100])
# plt.xlabel('samples')
# plt.ylabel('Power')
# plt.show()


# Noise Masker
# ------------
# The array for noises masks is given, so 
# just import it :)
Pnm_array = np.load('P_NM.npy')	
Pnm_array = np.reshape(Pnm_array, (wind_num, N // 2))
# print(np.size(Pnm_array))
# print(np.shape(Pnm_array))

mean = 0
for w in range(0, wind_num):
	helper = np.array(Ptm_array[w])
	helper = np.where(helper > 0)
	helper = helper[0]
	# if w == 50: print(np.size(helper))
	mean = mean + np.size(helper)
mean = mean / wind_num
# print(mean)

######################	
# plot Ptm_array[100]
# plt.stem(Pnm_array[100])
# plt.xlabel('samples')
# plt.ylabel('noise power')
# plt.show()
# print(Pnm_array[20])

##############
# TIME = 5.8s
##############

###########
# Step 1.3
###########
# Again, the arrays are given :) :)- 
# Import the arrays 
Pnmc = np.load('P_NMc.npy')		# array of shape 256 * number_of_frames	
Ptmc = np.load('P_TMc.npy')		# array of shape 256 * number_of_frames
# print(np.shape(Pnmc))

Pnmc = np.reshape(Pnmc, (wind_num, N // 2))
Ptmc = np.reshape(Ptmc, (wind_num, N // 2))

# helper = np.where(Ptmc[50] > 0)
# print(np.size(helper[0]))
# plt.stem(Ptmc[100])
# plt.xlabel('samples')
# plt.ylabel('Tonal Power')
# plt.plot()
# plt.show()

# plt.stem(Pnmc[100])
# plt.xlabel('samples')
# plt.ylabel('Noise Power')
# plt.plot()
# plt.show()

###########
# Step 1.4
###########

# Tonal Masker/Noise Thresholds
# -----------------------

# Make Sft(i, j) for tonal maskers
def Sft(i, j, w, Db):
	if -3 <= Db and Db < -1: return 17*Db - 0.4*Ptmc[w][j] + 11 
	elif -1 <= Db and Db < 0: return (0.4*Ptmc[w][j] + 6) * Db
	elif 0 <= Db and Db < 1: return -17*Db
	elif 1 <= Db and Db < 8: return (0.15*Ptmc[w][j] - 17)*Db - 0.15*Ptmc[w][j] 
	else: return 0 

# Make Sfn(i, j) for noise maskers
def Sfn(i, j, w, Db):
	if -3 <= Db and Db < -1: return 17*Db - 0.4*Pnmc[w][j] + 11 
	elif -1 <= Db and Db < 0: return (0.4*Pnmc[w][j] + 6) * Db
	elif 0 <= Db and Db < 1: return -17*Db
	elif 1 <= Db and Db < 8: return (0.15*Pnmc[w][j] - 17)*Db - 0.15*Pnmc[w][j] 
	else: return 0 


Ttm_array = []
for i in range (0, wind_num):
	Ttm_array.append(np.zeros([256,256]))

Tnm_array = []
for i in range (0, wind_num):
	Tnm_array.append(np.zeros([256,256]))

# Ttm_array = np.zeros([256, 256, wind_num])
# Tnm_array = np.zeros([256, 256, wind_num])

# print(Ttm_array[:,:,0])
# print(np.shape(Ttm_array))

# shape of St_array is (1179, 256)
# shape of Tmc = (256, 1179)
# shape of Tm_array = (1179, 256, 256)
# for every i we want to find the j's 
# in the window of Ptmc for which:
# 1) Ptmc[j] > 0
# 2) -3 <= Db < 8

# 1) To find the positions where Ptmc[j],
#	 I use the np.where() function 


x_tm_array = []
x_nm_array = []

for w in range(0, wind_num):
	helper_tm = np.where(Ptmc[w] > 0)	# helper[0] has the discrete frequencies (0-256) for the w-th 
	freq_tm = helper_tm[0]				# window for which Ptm[j] > 0  

	x_tm_array.append(freq_tm)				
	x_tm = np.size(freq_tm)				# x is the amount of freqs for which Ptm[j] > 0
										# As a result I do less repetitions because x is small
	b_tm_js = []												
	for k in range(0, x_tm):
		j = int(freq_tm[k])
		b_tm_js.append(bk(j))

	helper_nm = np.where(Pnmc[w] > 0)
	freq_nm = helper_nm[0]
	x_nm_array.append(freq_nm)
	x_nm = np.size(freq_nm)

	b_nm_js = []												
	for k in range(0, x_nm):
		j = int(freq_nm[k])
		b_nm_js.append(bk(j))


	for i in range(0,256):

		
		bi = b[i]

		for k in range(0, x_tm):

			bj = b_tm_js[k]
			j = int(freq_tm[k])
			Db = bi - bj


			if Db < -3 or Db >= 8: continue

			else:
				#print(Sft(i, j, w, Db))
				#print(Ptmc[w][j])
				Ttm_array[w][i][j] = Ptmc[w][j] - 0.275*bj + Sft(i, j, w, Db) - 6.025
				if Ttm_array[w][i][j] < 0: Ttm_array[w][i][j] = 0
				#print(Ttm_array[w][i][j])
		for k in range(0, x_nm):

			j = int(freq_nm[k])
			bj = b_nm_js[k]	
			Db = bi - bj

			if Db < -3 or Db >= 8: continue
			else:
				#print(j)
				Tnm_array[w][i][j] = Pnmc[w][j] - 0.275*bj + Sfn(i, j, w, Db) - 2.025
				if Tnm_array[w][i][j] < 0: Tnm_array[w][i][j] = 0
				#print(Tnm_array[w][i][j])

# l1 = plt.stem(Ptmc[50])
# l2 = plt.stem(Ttm_array[50][50])
# plt.setp(l1, color = 'r')
# plt.setp(l2, color = 'y')
# plt.show()

# l1 = plt.stem(Pnmc[100])
# l2 = plt.stem(Tnm_array[100][50])
# plt.setp(l1, color = 'r')
# plt.setp(l2, color = 'y')
# plt.show()



############
# Step 1.5
###########

# Absolute Threshold
# ------------------
def Tqf(f):
	if f == 0: return 40
	return 3.64 * pow((f/ 1000), -0.8) - 6.5 * pow(e, -0.6* ((f/1000 - 3.3)**2)) + pow(10, -3) * pow((f/1000), 4)

def Tqi(i):
	if i == 0: return 40
	f = fs * (i / N) 
	return Tqf(f)
#print(Tqi(0))

Tq_array = np.zeros([1179, 256])

for w in range(0, wind_num):
	
	helpl = x_tm_array[w]
	helpm = x_nm_array[w]


	L = np.size(x_tm_array[w])							
	M = np.size(x_nm_array[w])

	for i in range(0, 256):

		tq = Tqi(i)
		
		c = pow(10, 0.1*tq)

		suml = 0
		for l in range(0, L):
			j = helpl[l]
			suml = suml + pow(10, 0.1*Ttm_array[w][i][j])

		summ = 0
		for m in range(0, M):
			j = helpm[m]
			#print(Tnm_array[w][i][j])
			summ = summ + pow(10, 0.1*Tnm_array[w][i][j])

		Tq_array[w][i] = 10 * np.log10(c + suml + summ)


# plt.plot(Tq_array[30])
# plt.xlabel('samples')
# plt.ylabel('Global Masking Threshold')
# plt.show()


# save the Tq(i) array
np.save("Tg", Tq_array)

# for i in range(0,255):
# print(pow(10, 0.1*Tqi(i)))
