from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel

if '__main__' == __name__:
	setLogLevel('info')
	net = Mininet(link=TCLink)
	value = 0
	
	#Add Host
	hA = net.addHost('hA')
	hB = net.addHost('hB')
	
	#Add Router
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')
	
	#Add Link
	#Tambahkan max_queue_size dan use_htb = True untuk CLO4 
	net.addLink(r1, hA, max_queue_size = 100, use_htb = True, intfName1 = 'r1-eth0', intfName2 = 'hA-eth0', cls=TCLink, bw=1)
	net.addLink(r1, r3, max_queue_size = 100, use_htb = True, intfName1 = 'r1-eth1', intfName2 = 'r3-eth0', cls=TCLink, bw=0.5)
	net.addLink(r3, hB, max_queue_size = 100, use_htb = True, intfName1 = 'r3-eth1', intfName2 = 'hB-eth0', cls=TCLink, bw=1)
	net.addLink(hB, r4, max_queue_size = 100, use_htb = True, intfName1 = 'hB-eth1', intfName2 = 'r4-eth0', cls=TCLink, bw=1)
	net.addLink(r4, r2, max_queue_size = 100, use_htb = True, intfName1 = 'r4-eth1', intfName2 = 'r2-eth0', cls=TCLink, bw=0.5)
	net.addLink(r2, hA, max_queue_size = 100, use_htb = True, intfName1 = 'r2-eth1', intfName2 = 'hA-eth1', cls=TCLink, bw=1)
	net.addLink(r1, r4, max_queue_size = 100, use_htb = True, intfName1 = 'r1-eth2', intfName2 = 'r4-eth2', cls=TCLink, bw=1)
	net.addLink(r2, r3, max_queue_size = 100, use_htb = True, intfName1 = 'r2-eth2', intfName2 = 'r3-eth2', cls=TCLink, bw=1)
	net.build()
	
	#Config Host
	hA.cmd("ifconfig hA-eth0 0")
	hA.cmd("ifconfig hA-eth1 0")
	hA.cmd("ifconfig hA-eth0 192.168.0.1 netmask 255.255.255.0")
	hA.cmd("ifconfig hA-eth1 192.168.7.2 netmask 255.255.255.0")
	hB.cmd("ifconfig hB-eth0 0")
	hB.cmd("ifconfig hB-eth1 0")
	hB.cmd("ifconfig hB-eth0 192.168.3.2 netmask 255.255.255.0")
	hB.cmd("ifconfig hB-eth1 192.168.5.1 netmask 255.255.255.0")
	
	#Config Router
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 2 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 3 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 4 > /proc/sys/net/ipv4/ip_forward")
	
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	r1.cmd("ifconfig r1-eth0 192.168.0.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.1.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.2.1 netmask 255.255.255.0")
	
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	r2.cmd("ifconfig r2-eth0 192.168.6.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.7.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.4.2 netmask 255.255.255.0")
	
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	r3.cmd("ifconfig r3-eth0 192.168.1.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.3.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.4.1 netmask 255.255.255.0")
	
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	r4.cmd("ifconfig r4-eth0 192.168.5.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.6.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.2.2 netmask 255.255.255.0")
	
	#Routing Host
	hA.cmd("ip rule add from 192.168.0.1 table 1")
	hA.cmd("ip rule add from 192.168.7.2 table 2")
	hA.cmd("ip route add 192.168.0.0/24 dev hA-eth0 scope link table 1")
	hA.cmd("ip route add default via 192.168.0.2 dev hA-eth0 table 1")
	hA.cmd("ip route add 192.168.7.0/24 dev hA-eth1 scope link table 2")
	hA.cmd("ip route add default via 192.168.7.1 dev hA-eth1 table 2")
	hA.cmd("ip route add default scope global nexthop via 192.168.0.2 dev hA-eth0")
	hA.cmd("ip route add default scope global nexthop via 192.168.7.1 dev hA-eth1")
	#Tambahan untuk clo4
	hA.cmd("route add default gw 192.168.0.2 dev hA-eth0")
	hA.cmd("route add default gw 192.168.7.1 dev hA-eth1")
	
	hB.cmd("ip rule add from 192.168.3.2 table 3")
	hB.cmd("ip rule add from 192.168.5.1 table 4")
	hB.cmd("ip route add 192.168.3.0/24 dev hB-eth0 scope link table 1")
	hB.cmd("ip route add default via 192.168.3.1 dev hB-eth0 table 1")
	hB.cmd("ip route add 192.168.5.0/24 dev hB-eth1 scope link table 2")
	hB.cmd("ip route add default via 192.168.5.2 dev hB-eth1 table 2")
	hB.cmd("ip route add default scope global nexthop via 192.168.3.1 dev hB-eth0")
	hB.cmd("ip route add default scope global nexthop via 192.168.5.2 dev hB-eth1")
	#Tambahan untuk clo4
	hB.cmd("route add default gw 192.168.3.1 dev hB-eth0")
	hB.cmd("route add default gw 192.168.5.2 dev hB-eth1")
	
	#Routing Router
	r1.cmd("route add -net 192.168.3.0/24 gw 192.168.1.2")
	r1.cmd("route add -net 192.168.5.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.6.0/24 gw 192.168.2.2")
	r1.cmd("route add -net 192.168.7.0/24 gw 192.168.1.2")
	r1.cmd("route add -net 192.168.4.0/24 gw 192.168.1.2")
	
	r2.cmd("route add -net 192.168.0.0/24 gw 192.168.4.1")
	r2.cmd("route add -net 192.168.1.0/24 gw 192.168.4.1")
	r2.cmd("route add -net 192.168.3.0/24 gw 192.168.4.1")
	r2.cmd("route add -net 192.168.5.0/24 gw 192.168.6.1")
	r2.cmd("route add -net 192.168.2.0/24 gw 192.168.6.1")
	
	r3.cmd("route add -net 192.168.5.0/24 gw 192.168.4.2")
	r3.cmd("route add -net 192.168.6.0/24 gw 192.168.4.2")
	r3.cmd("route add -net 192.168.7.0/24 gw 192.168.4.2")
	r3.cmd("route add -net 192.168.0.0/24 gw 192.168.1.1")
	r3.cmd("route add -net 192.168.2.0/24 gw 192.168.1.1")
	
	r4.cmd("route add -net 192.168.7.0/24 gw 192.168.6.2")
	r4.cmd("route add -net 192.168.0.0/24 gw 192.168.2.1")
	r4.cmd("route add -net 192.168.1.0/24 gw 192.168.2.1")
	r4.cmd("route add -net 192.168.3.0/24 gw 192.168.2.1")
	r4.cmd("route add -net 192.168.4.0/24 gw 192.168.6.2")
	
	#iPerf
	hB.cmd('iperf -s &')
	hA.cmd('iperf -t 10 -B 192.168.0.1 -c 192.168.3.2 &')
	hA.cmd('iperf -t 10 -B 192.168.7.2 -c 192.168.3.2 &')
	
	CLI(net)
	net.stop()
