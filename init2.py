import corr, time, numpy, struct, sys,socket
import matplotlib.pyplot as plt

dest_ip  =10*(2**24) + 30 #10.0.0.30
fabric_port=60000         
source_ip=10*(2**24) + 20 #10.0.0.20
mac_base=(2<<40) + (2<<32)
ip_prefix='10. 0. 0.'     #Used for the purposes of printing output.

pkt_period = 100#100  #in FPGA clocks (200MHz) la cague
payload_len = 50#50   #in 64bit words


#pkt_period = 120
#payload_len = 50
#Esto equivale a 3.3Gbbps


tx_core_name = 'gbe0'
rx_core_name = 'gbe1'
fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof='gbe_tut1_2020_May_03_1543.bof.gz'
fpga.upload_program_bof(bof, 3000)
time.sleep(1)



fpga.tap_start('rx_tap',rx_core_name,mac_base+dest_ip,dest_ip,fabric_port)

fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)

fpga.write_int('packet_period',pkt_period)
fpga.write_int('packet_payload_len',payload_len)

fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',fabric_port)


fpga.write_int('gbe_rst',1)
fpga.write_int('gbe_rst',0)
fpga.write_int('cnt_rst',1)
fpga.write_int('cnt_rst',0)


fpga.write_int('packet_enable',1)
time.sleep(2)


rx_data = struct.unpack('>1024Q',fpga.read('rx_data',1024*8))
tx_data = struct.unpack('>1024Q',fpga.read('tx_data',1024*8))

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


ax1.plot(tx_data)
ax1.set_title('tx_data')
ax1.grid()
ax2.plot(rx_data)
ax2.set_title('rx_data')
ax2.grid()
plt.show()





data_rate = 1.*payload_len/pkt_period*100
tge_rate = data_rate/(8./10*156.25)


print("10gb rate: %.4f" %(tge_rate*10))


#test lost packages

n_iter = 1000

f = open('lost_pack', 'w')
f.close()

f = file('lost_pack', 'a')

for i in range(n_iter):
    fpga.write_int('cnt_rst',1)
    fpga.write_int('cnt_rst',0)
    rx_data = struct.unpack('>Q',fpga.read('rx_data',8))
    tx_data = struct.unpack('>Q',fpga.read('tx_data',8))
    offset = rx_data[0]-tx_data[0]
    print(offset)
    f.write(str(offset)+'\n')
    time.sleep(1)
f.close()


















