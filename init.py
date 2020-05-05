import time, corr


fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof = 'gbe_tut1_2020_May_03_1543.bof.gz'
fpga.upload_program_bof(bof, 3000)
time.sleep(1)

#packet options
pkt_period = 100 #16384 #measured in fpga cycles # vi que la cague, el contador tiene 8bits no mas....
payload_len = 128  #in 64bits words



dest_ip  =192*(2^24) + 168*(2^16) + 5*(2^8) + 16*(2^0)

 #10*(2**24) + 30 #10.0.0.30                          
fabric_port=10000 
source_ip=192*(2^24) + 168*(2^16) + 5*(2^8) + 20*(2^0)#10*(2**24) + 20 #10.0.0.20
mac_base=(2<<40) + (2<<32)
ip_prefix='10. 0. 0.'     #Used for the purposes of printing output.
rx_name = 'gbe1'
tx_name = 'gbe0'

#hex2dec('123456780000') esto es lo que sale en el bloque....

tx_link = bool(fpga.read_int('gbe_linkup'))

if not tx_link:
    print('There is no cable connected to port0')

rx_link = bool(fpga.read_int('gbe1_linkup'))

if not rx_link:
    print('There is no cable connected to port1')


print('Configuring the rx core')
fpga.tap_start('tap_rx', rx_name, mac_base+dest_ip,dest_ip,fabric_port)
print('done')

print('Configuring the tx core')
fpga.tap_start('tap_tx',tx_name,mac_base+source_ip,source_ip,fabric_port)
print('done')

print('Setting up packet source')
fpga.write_int('packet_period', pkt_period)
fpga.write_int('packet_payload_len', payload_len)
print('done')


print('Setting up dest addr')
fpga.write_int('dest_ip', dest_ip)
fpga.write_int('dest_port', fabric_port)
print('done')

print('reseting everything')
fpga.write_int('cnt_rst',1)
fpga.write_int('gbe_rst',0)
fpga.write_int('gbe_rst',1)
fpga.write_int('cnt_rst',0)

print('done')
time.sleep(2)



"""we dont use arp tables
print '10GbE Transmitter core details:'
        print '==============================='
        print "Note that for some IP address values, only the lower 8 bits are valid!"
        fpga.print_10gbe_core_details(tx_core_name,arp=True)
        print '\n\n============================'
        print '10GbE Receiver core details:'
        print '============================'
        print "Note that for some IP address values, only the lower 8 bits are valid!"
        fpga.print_10gbe_core_details(rx_core_name,arp=True)

"""

"""
print 'Sent %i packets already.'%fpga.read_int('gbe0_tx_cnt')
print 'Received %i packets already.'%fpga.read_int('gbe1_frame_out')

"""

print('enabling packets flow')
fpga.write_int('packet_enable',1)
print('done')




















