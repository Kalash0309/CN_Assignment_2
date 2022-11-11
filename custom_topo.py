
from mininet.topo import Topo

class MyTopo( Topo ):
    #"Custom topology example."

    def build( self ):
        #"Create custom topo."

        # Add hosts 
        hostA = self.addHost( "h1" )
        hostB = self.addHost( "h2" )
        hostC = self.addHost( "h3" )
        hostD = self.addHost( "h4" )
        # Add switches
        switchR1 = self.addSwitch( "s1" )
        switchR2 = self.addSwitch( "s2" )

        # Add links
        self.addLink( hostA, switchR1, bw = 1000, delay = 1 )
        self.addLink( hostD, switchR1, bw = 1000, delay = 1  )
        self.addLink( switchR1, switchR2, bw = 500, delay = 10  )
        self.addLink( hostB , switchR2, bw = 1000, delay = 1  )
        self.addLink( hostC, switchR2, bw = 1000, delay = 5  )
        #self.addLink( hostC, switchR2, bw = 1000, delay = 1  )


topos = { 'mytopo': ( lambda: MyTopo() ) }
