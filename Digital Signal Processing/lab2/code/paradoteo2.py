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
N = 512							# samples per window 
fs = 44100						# sampling frequency
PN = 90.302						# just a constant 
bits_per_sample = 16
old_size = 603285
e = math.e 						# Euler's constant
M = 32 							# number of filters
L = 2 * M 						# duration of each filter
n = np.linspace(0, L-1, L)		# 0,1,...,L-1 => L samples
pi = math.pi 					# pi constant
conv_size = N + L - 1 			# size of convolution at step 2.1
B = 16							# number of bits of initial signal s[n]
R = pow(2, B)					# number of levels of initial signal s[n]
big_int = 1000000
conv_size2 = 638

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


# Zero Padding
# ------------
# print(np.size(norm_music))
# The size of the signal is 603285 samples (using np.size())
# In order to take windows of 512 samples I add zeros to the signal
# such as new_size mod 512 = 0. I must add old_size mod 512 zeros
zeros_to_add = N - old_size % N 
x = np.pad(music, (0, zeros_to_add), 'constant')	# zero padding
new_size = np.size(x)
# print(np.size(norm_music))
# print(np.size(norm_music) / 512)
# Now, I have 1179 windows each one of 512 samples 
wind_num = int(np.size(x) / N) 		# = int(1179.0) = 1179


###########
# Step 2.0
###########

# Make of hk's
# ------------
hk_arrays = []		# shape = (32, 64)

for k in range(0, M):
	helper = math.sqrt(2/M) * np.sin((n+0.5) * (pi / L)) * np.cos(((2*n + M + 1) * (2*k + 1) * pi) / (4*M))
	hk_arrays.append(helper)

# print(np.shape(hk_arrays))

#####################
# plot hk_arrays[10]
# plt.stem(hk_arrays[10])
# plt.xlabel('samples')
# plt.ylabel('hk[10]')
# plt.show()

# Make of gk's
# ------------
gk_arrays = []		# shape = (32, 64)

for k in range(0, M):
	helper = math.sqrt(2/M) * np.sin(((2*M - 1 - n) + 0.5) * (pi / L)) * np.cos(((2*(2*M - 1 -n) + M + 1) * (2*k + 1) * pi) / (4*M))
	# gk[n] = hk[2M - 1 - n]
	gk_arrays.append(helper)

#######################
# plt.stem(gk_arrays[10])
# plt.xlabel('samples')
# plt.ylabel('gk[10]')
# plt.show()

# l1 = plt.stem(hk_arrays[10])
# l2 = plt.stem(gk_arrays[10])
# plt.setp(l1, color = 'r')
# plt.setp(l2, color = 'y')
# plt.show()



# First, let's seperate x[n] to frames of 512 samples
x_array = []					# shape = (1179, 512)
for w in range(0, wind_num):
	sl = w * N 					# need for the slicing
	helper = x[sl : sl+N]
	x_array.append(helper)
# print(np.shape(x_array))


###########
# Step 2.1
###########

# Make of uk's
# ------------
# uk[n] = hk[n] ∗ x[n]
# x[n] is processed in frames of 512 samples
# As a result, I need an array of 32 (number of filters) * 1179 (number of windows) * (512 + 64 - 1) (size of convolution) 

uk_arrays = []		# shape = (32, 1179, 575), 575 = (512 + 64 - 1)

for k in range(0, M):
	helper1 = hk_arrays[k]
	helper2  = []
	for w in range(0, wind_num):
		helper2.append(np.convolve(x_array[w], helper1))
	uk_arrays.append(helper2)


##################
# plot uk[10][10]
# plt.plot(uk_arrays[10][10])
# plt.xlabel('samples')
# plt.ylabel('uk')
# plt.show()

# Downsampling
# ------------
# Since size of convolved windows  = 575, 
# and the signal is downsampled by 32, each frame
# will have 18 samples (0, 32, 64, ..., 544)
# As a result, I need an array of shape (32, 1179, 18)

yk_arrays = []			# shape = (32, 1179, 18)

for k in range(0, M):
	helper1 = []
	for w in range(0, wind_num):
		helper2 = uk_arrays[k][w]
		helper3 = []
		u = 0 		# pointer for uk, increase by M in every loop
		while u < conv_size:
			helper3.append(helper2[u])
			u = u + M 
		helper1.append(helper3)
	yk_arrays.append(helper1)

##################
# plot yk[10][10]
# plt.stem(yk_arrays[10][10])
# plt.xlabel('samples')
# plt.ylabel('yk[10]')
# plt.show()


###########
# Step 2.2
###########

# I will need the Tq(i) values, so lets import
# the array from 1st part
Tg_array = np.load("Tg.npy")		# shape = (1179, 256)
#print(Tg_array[100])


# 1st Quantizer
# -------------

# a) Find minimum Tq(i)'s

# For each filter I need to find the minimum Tg(i)
# which will be used for the Bk calculation
# I will name the array which holds these values
# Tg_used and it's size is 32

indexes = np.arange(0, N // 2)

Tg_used = []
# print(Tg_array[1])

for k in range(0, M):
	fk = ((2*k - 1)*fs) / (4*M)
	fl = fk - fs/(4*M)
	fr = fk + fs/(4*M)
	valid_indexes = np.where(np.logical_and((fl <= fs*(indexes/N)), (fs*(indexes/N) <= fr)))
	valid_indexes = valid_indexes[0]
	# print(valid_indexes)
	minn = big_int
	for w in range(0, wind_num):
		helper1 = Tg_array[w]
		helper2 = helper1[valid_indexes]
		pos_min = np.min(helper2)
		if pos_min > 20 and pos_min < minn: minn = pos_min
	Tg_used.append(minn)

# Now, I can make the Bk's 
Bk = []

for k in range(0, M):
	helper = int(math.log2(R/Tg_used[k]) - 1)
	Bk.append(helper)

# print(Bk)

# Now, I am ready to make the adaptive quantizer
# I will make a mid-riser quantizer

#			  |-----------|
# y[n] -----> |	Mid Riser | -----> y_h[n] = Δ * ([x/Δ + 1/2])
#			  |	Quantizer |
#			  |-----------|

# For the quantizer I need the minimum and maximum values
# for each window of the music signal
mins = []
maxs = []
for k in range (0, M):
	minn = big_int
	maxx = 0
	for w in range(0, wind_num):
		pos_min = np.min(yk_arrays[k][w])
		pos_max = np.max(yk_arrays[k][w])
		if pos_min < minn: minn = pos_min
		if pos_max > maxx: maxx = pos_max
	mins.append(minn)
	maxs.append(maxx)

y_h = np.zeros([M, wind_num, 18])	# shape = (32, 1179, 18)


for k in range(0, M):
	tg = Tg_used[k]
	bk = Bk[k]
	rk = pow(2, bk)
	minn = mins[k]
	maxx = maxs[k]
	D = (maxx - minn) / rk
	minn = min(abs(minn), maxx)
	for w in range(0, wind_num):
		helper1 = yk_arrays[k][w]
		helper2 = [h/D + 1/2 for h in helper1]
		helper3 = np.where(helper2 >= np.round(helper2), np.round(helper2), np.round(helper2) - 1) 
		y_h[k][w] = [D * h for h in helper3]


###########
# Step 2.3
###########

# Make wk[n]
# ----------
wk = np.zeros([M, wind_num, conv_size])		# shape = (32, 1179, 575)

for k in range(0, M):
	for w in range(0, wind_num):
		for i in range(0, 18):
			wk[k][w][M*i] = y_h[k][w][i]



bfsum_arrays = []		# shape = (32, 1179, 638), 638 = (575 + 64 - 1), bfsum ---> before sum

for k in range (0, M):
	helper1 = gk_arrays[k]
	helper2  = []
	for w in range(0, wind_num):
		helper2.append(np.convolve(wk[k][w], helper1))
	bfsum_arrays.append(helper2)

# I want analysis frames of 512 size 
# As a result, I must add the remaining samples
# in each frame (638 - 512) to the next frame 

bfol = []	# shape = (1179, 638), 638 = (575 + 64 - 1), bfol ---> before overlap
bfol = bfsum_arrays[0]

for k in range (1, M):
	for w in range(0, wind_num):
		bfol[w] = bfol[w] + bfsum_arrays[k][w]



# Make of s_h[n]
# --------------

s_h = np.zeros([wind_num, N])	# shape = (1179, 512)

overlapping_samples = []		# it has the samples that will be overlapped from a frame 
								# to the next one 
								# size = 638 - 512
								# I initilize it with the last frame's samples as they will 
								# be overlapped to the first

for i in range (N, conv_size2):
	overlapping_samples.append(bfol[wind_num-1][i])


for w in range(0, wind_num):
	helper = bfol[w][0:N]
	s_h[w] = helper
	for i in range (0, conv_size2 - N):
		s_h[w][i] = s_h[w][i] + overlapping_samples[i]
		overlapping_samples[i] = bfol[w][N+i]

s_hr = []
for w in range (0, wind_num):
	for i in range (0, N):
		s_hr.append(s_h[w][i])


sf.write('tone_sequence_adaptive.wav', s_hr, fs)


# Uniform 8bit quantizier
# ------------------

# Bk_un = []
# for k in range (0, M):
# 	Bk_un.append(8)

bk = 8
D = 1 / pow(2,7)
y_h_un = np.zeros([M, wind_num, 18])	# shape = (32, 1179, 18)
for k in range(0, M):
	for w in range(0, wind_num):
		helper1 = yk_arrays[k][w]
		helper2 = [h/D + 1/2 for h in helper1]
		helper3 = np.where(helper2 >= np.round(helper2), np.round(helper2), np.round(helper2) - 1) 
		y_h_un[k][w] = [D * h for h in helper3] 


wk_un = np.zeros([M, wind_num, conv_size])		# shape = (32, 1179, 575)

for k in range(0, M):
	for w in range(0, wind_num):
		for i in range(0, 18):
			wk_un[k][w][M*i] = y_h_un[k][w][i]



bfsum_arrays_un = []		# shape = (32, 1179, 638), 638 = (575 + 64 - 1), bfsum ---> before sum

for k in range (0, M):
	helper1 = gk_arrays[k]
	helper2  = []
	for w in range(0, wind_num):
		helper2.append(np.convolve(wk_un[k][w], helper1))
	bfsum_arrays_un.append(helper2)
# print(np.shape(bfsum_arrays))

# I want analysis frames of 512 size 
# As a result, I must add the remaining samples
# in each frame (638 - 512) to the next frame 



#################################################################################
bfol_un = []	# shape = (1179, 638), 638 = (575 + 64 - 1), bfol ---> before overlap
bfol_un = bfsum_arrays_un[0]

for k in range (1, M):
	for w in range(0, wind_num):
		bfol_un[w] = bfol_un[w] + bfsum_arrays_un[k][w]



# Make of s_h[n]
# --------------

s_h_un = np.zeros([wind_num, N])	# shape = (1179, 512)

overlapping_samples_un = []		# it has the samples that will be overlapped from a frame 
								# to the next one 
								# size = 638 - 512
								# I initilize it with the last frame's samples as they will 
								# be overlapped to the first

for i in range (N, conv_size2):
	overlapping_samples_un.append(bfol_un[wind_num-1][i])


for w in range(0, wind_num):
	helper = bfol_un[w][0:N]
	s_h_un[w] = helper
	for i in range (0, conv_size2 - N):
		s_h_un[w][i] = s_h_un[w][i] + overlapping_samples_un[i]
		overlapping_samples_un[i] = bfol_un[w][N+i]

s_hr_un = []
for w in range (0, wind_num):
	for i in range (0, N):
		s_hr_un.append(s_h_un[w][i])

# plt.plot(s_hr)
# plt.show()[


# plt.plot(b, Tg_array[100])
# plt.show()

sf.write('tone_sequence_non_adaptive.wav', s_hr_un, fs)

# plt.plot(x, color  = 'blue')
# plt.plot(s_hr, color = 'green')
# plt.show()


# Level of Compression
# --------------------
Bk_old = bits_per_sample * old_size
Bk_new_adaptive = 0
for k in range(0, M):
	b = Bk[k]
	Bk_new_adaptive = Bk_new_adaptive + b*wind_num*18
	Bk_new_adaptive = Bk_new_adaptive + 32

level_of_compression_adaptive = 1 - Bk_new_adaptive/Bk_old
# print(level_of_compression_adaptive)

Bk_new_8bit = 0
for k in range(0, M):
	Bk_new_8bit = Bk_new_8bit + 8*wind_num*18

Bk_new_8bit = Bk_new_8bit + 32
level_of_compression_8bit = 1 - Bk_new_8bit/Bk_old
# print(level_of_compression_8bit)


# Squared Error
# -------------
delay = 63
E_8bit = []
for i in range (delay, old_size):
	E_8bit.append(pow((x[i-delay] - s_hr_un[i]), 2))
E_8bit = np.array(E_8bit)
Mean_E_8bit = np.sum(E_8bit) / (old_size - delay)
# print(Mean_E_8bit) 

E_ad = []
for i in range (delay, old_size):
	E_ad.append(pow((x[i-delay] - s_hr[i]), 2))
E_ad = np.array(E_ad)
Mean_E_ad = np.sum(E_ad) / (old_size - delay)
# print(Mean_E_ad)	

# plt.plot(E_ad[N:2*N], color = 'red')
# plt.plot(E_8bit[N:2*N], color = 'black')
# plt.xlabel('samples')
# plt.ylabel('Squared Errors')
# plt.show()