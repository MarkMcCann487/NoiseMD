import numpy as np


class NoiseMD : 
    def __init__(self) :
        self.positions = np.zeros(10)
        self.velocities = []
        self.energy = [] 
        self.attachments = []

    def create_initial_positions( self, nx, ny ) :
        """ 
        This function generates an initial 2D structure which has the atoms on a 2D FCC lattice

        Input arguments: 
        nx = number of replicas of the unit cell in the x direction
        ny = number of replicas of the unit cell in the y direction
        """ 
        self.positions = []
        pass

    def potential( self ) :
        """
        Returns:
        ???
        """
        pass

    def runMD( self, nsteps, tstep, temp, friction ) :
        """ 
        """
        print("HELLO WORLD")

    def get_positions( self ) : 
        return self.positions 
 
