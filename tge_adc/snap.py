import numpy as np
import matplotlib.pyplot as plt
import struct
import matplotlib.animation as animation
import ipdb
from scipy.fftpack import fft 


def plot_snap(_fpga):
    global fpga, data
    fpga = _fpga; 
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax1.set_ylim(0, 16)
    ax2.set_ylim(0, 16)
    ax1.set_xlim(0,1024)
    ax2.set_xlim(0,1024)
    ax1.set_title('tx')
    ax2.set_title('rx')
    line1, = ax1.plot([],[])
    line2, = ax2.plot([],[])
    data = [line1, line2]
    ani = animation.FuncAnimation(fig, animate,init_func=init, interval=50, blit=True)
    plt.show()



def init():
    data[0].set_data([],[])
    data[1].set_data([],[])
    #ipdb.set_trace()
    return data

def animate(i):
    #ipdb.set_trace()
    snap1 = struct.unpack('>16384B',fpga.snapshot_get('tx_snap', man_trig=True, man_valid=True)['data'])
    snap2 = struct.unpack('>16384B',fpga.snapshot_get('rx_snap', man_trig=True, man_valid=True)['data'])
    data[0].set_data(np.arange(1024), snap1[0:1024])
    data[1].set_data(np.arange(1024), snap2[0:1024])
    return data






def plot_spectrums(fpga):
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.set_title('tx data')
    ax2.set_title('rx data')
    ax1.grid()
    ax2.grid()
    adc_data = struct.unpack('>16384B',fpga.snapshot_get('tx_snap', man_trig=True, man_valid=True)['data'])
    adc_spect = fft(adc_data)
    red_data = struct.unpack('>16384B',fpga.snapshot_get('rx_snap', man_trig=True, man_valid=True)['data'])
    red_spect = fft(red_data)

    freq = np.linspace(0, 1080,8192, endpoint=False)
    ax1.plot(freq, 20*np.log10(np.abs(np.array(adc_spect[0:8192]))+1))
    ax2.plot(freq, 20*np.log10(np.abs(np.array(red_spect[0:8192]))+1))
    plt.show()

