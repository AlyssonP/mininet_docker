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
        r1 = self.addNode("r1", cls=LinuxRouter, ip=None)
        s1, s2 = [self.addSwitch(s) for s in ("s1", "s2")]
        
        self.addLink(s1, r1, intfName2="r1-eth1", params2={"ip": "172.18.0.10/16"})
        self.addLink(s2, r1, intfName2="r1-eth2", params2={"ip": "172.19.0.10/16"})

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    
    net.start()

    brteste01 = "br-7263015daf68"  # Substitua pelo ID real
    brteste02 = "br-4a0cefb67b4e"  # Substitua pelo ID real
    
    try:
        info(f"Conectando {brteste01} ao s1\n")
        s1 = net.get("s1")
        _intf1 = Intf(brteste01, node=s1)

        info(f"Conectando {brteste02} ao s2\n")
        s2 = net.get("s2")
        _intf2 = Intf(brteste02, node=s2)
    except Exception as e:
        info(f"Erro ao conectar bridges: {e}\n")
        
    # info( '*** Routing Table on Router:\n' )
    # info( net[ 'r1' ].cmd( 'route' ) )

    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    run()