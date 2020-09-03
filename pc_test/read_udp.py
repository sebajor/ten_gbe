import struct
import numpy as np
import matplotlib.pyplot as plt

f = file('udp_data3','r')

data = np.zeros([1024, 1024])
for i in range(1024):
    try:
        raw_data = f.read(1024*8)
        dat= struct.unpack('>1024Q', raw_data)
        data[i,:] = dat
    except:
        print('issue at i=%i' %i)
        break

data = data.flatten()
plt.figure()
plt.title('10Gbeth data')
plt.ylabel('read values')
plt.grid()
plt.plot(data-data[0])


plt.figure()
plt.title('Difference 10Gbeth')
plt.grid()
plt.plot(np.diff(data))

est = np.sum(np.diff(data))-len(data)
print("Estimated dropped samples %i" %est)

plt.show()


