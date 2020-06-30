import corr, time, struct
import numpy as np
import matplotlib.pyplot as plt


def read_brams(fpga):
        len_data = 8192*16
        par = struct.unpack('>8192I', fpga.read('ring_buffer_brams1_parity', 2**13*4,0))
        dat0 = struct.unpack('>16384Q',fpga.read('ring_buffer_brams1_dat0', len_data))
        dat1 = struct.unpack('>16384Q',fpga.read('ring_buffer_brams1_dat1', len_data))
        dat0 = np.array(dat0).reshape(8192,2)    
        dat1 = np.array(dat1).reshape(8192,2)
        vals = np.hstack([dat0[:,::-1], dat1[:,::-1]])
        vals = vals.flat
        return [par, vals]



pkt_period = 1030#1024#100  #in FPGA clocks (200MHz) la cague
payload_len = 1024#1000#50   #in 64bit words

gen_rate = 1.*payload_len/pkt_period*100
tge_rate = gen_rate/(8./10*156.25)*10
print('data rate: %.2f GSa/s' %(tge_rate))


dest_ip  =10*(2**24) + 30 #10.0.0.30
fabric_port=60000         
source_ip=10*(2**24) + 20 #10.0.0.20
mac_base=(2<<40) + (2<<32)
ip_prefix='10. 0. 0.'     #Used for the purposes of printing output.


tx_core_name = 'gbe0'
rx_core_name = 'gbe2'


fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof = 'gbe_dram.bof.gz'#'gbe_ex.bof.gz'
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

##set the dram 
fpga.write_int('ring_buffer_read',0)
fpga.write_int('ring_buffer_rst_brams1',1)
fpga.write_int('ring_buffer_rst_brams1',0)
fpga.write_int('ring_buffer_en_write',1)



fpga.write_int('cnt_rst',0)
fpga.write_int('packet_enable',1)
time.sleep(5)

print('read data')
fpga.write_int('ring_buffer_en_write',0)

total_addr = 2**24
len_bram = 8192
iterations = total_addr/len_bram
f = file('dram_data', 'a')
errors = 0

start = time.time()
fpga.write_int('ring_buffer_read',1)




[par, vals] = read_brams(fpga)

plt.plot(vals[4:8192])
plt.title('RX data')
plt.grid()
plt.show()

dif = np.diff(vals)
plt.plot(dif[8:])
plt.grid()
plt.title('Difference')
plt.show()



errors = []
for i in range(2**11):
    print('iter: %i' %i)
    counter = 0
    while(1):
        if(fpga.read_int('ring_buffer_bram_full1')):
            break
        elif(counter>4000):
            errors = errors+1
            print('Error')
            break
        counter = counter + 1
    [par, vals] = read_brams(fpga)
    fpga.write_int('ring_buffer_rst_brams1',1)
    fpga.write_int('ring_buffer_rst_brams1',0)
    dif = np.diff(vals)
    ind = np.where(dif!=1)
    errors.append(dif[ind[0]])
    
    

total = time.time()-start
print('total time: '+str(total))








        
        











