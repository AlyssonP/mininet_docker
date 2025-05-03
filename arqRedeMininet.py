#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.link import Intf
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class NetworkTopo(Topo):
    "A LinuxRouter connecting three IP subnets"
    
    def build(self, **_opts):
        defaultIP = "172.18.0.10/16"  # IP address for r1-eth1
        r1 = self.addNode("r1", cls=LinuxRouter, ip=defaultIP)
        s1, s2 = [self.addSwitch(s) for s in ("s1", "s2")]
        
        self.addLink(s1, r1, intfName2="r1-eth1", params2={"ip": defaultIP})
        self.addLink(s2, r1, intfName2="r1-eth2", params2={"ip": "172.19.0.10/16"})

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)

    brteste01 = "br-8f91297f76b9"  # Substitua pelo ID real
    brteste02 = "br-b9b84ce45687"  # Substitua pelo ID real

    s1 = net.getNodeByName("s1")
    s2 = net.getNodeByName("s2")

    info(f"Conectando {brteste01} ao s1\n")
    _intf1 = Intf(brteste01, node=s1)

    info(f"Conectando {brteste02} ao s2\n")
    _intf2 = Intf(brteste02, node=s2)
    
    net.start()
        
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r1' ].cmd( 'route' ) )

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    run()