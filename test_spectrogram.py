import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt

dir = 'wavfiles/'
filename = 'cat.wav'


sample_rate, data = wavfile.read(dir +  filename)
frequencies, times, spectrogram = signal.spectrogram(data, sample_rate)
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle(filename)
ax1.pcolormesh(times, frequencies, spectrogram, shading='auto')
ax1.set_ylabel('Frequency [Hz]')
ax1.set_xlabel('Time [sec]')
ax2.plot(np.linspace(0, times[-1], data.size), data)
print(times)
plt.show()

