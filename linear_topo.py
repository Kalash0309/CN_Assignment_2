
from mininet.topo import Topo

class MyTopo( Topo ):
    #"Custom topology example."

    def build( self ):
        #"Create custom topo."

        # Add hosts 
        hostA = self.addHost( "h1" )
        hostB = self.addHost( "h2" )

        # Add switch
        switchR1 = self.addSwitch( "s1" )

        # Add links
        self.addLink( hostA, switchR1, bw = 1000, delay = 1, loss=5 )
        self.addLink( hostB, switchR1, bw = 1000, delay = 1, loss=5  )


topos = { 'mytopo': ( lambda: MyTopo() ) }
