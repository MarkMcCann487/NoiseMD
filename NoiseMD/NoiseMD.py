import numpy as np
import scipy.stats 


class NoiseMD:
    def __init__(self):
        self.positions = np.zeros(10)
        self.velocities = []
        self.energy = []
        self.attachments = []

    def create_initial_positions(self, nx, ny):
        """
        This function generates an initial 2D structure which has the atoms on a 2D FCC lattice

        Input arguments:
        nx = number of replicas of the unit cell in the x direction
        ny = number of replicas of the unit cell in the y direction
        """
        a = (2**(2/3))
        self.natoms = 2*nx*ny
        self.positions = np.zeros([self.natoms,2])

        k=0
        for ix in range(nx) :
            for iy in range(ny) :
                self.positions[k][0] = (0+ix)*a
                self.positions[k][1] = (0+iy)*a
                self.positions[k+1][0] = (0.5+ix)*a
                self.positions[k+1][1] = (0.5+iy)*a
                k+=2

    def potential(self):
        """
        Returns:
        ???
        """
        pass

    def set_params( self, tstep, temp, friction ) : 
        self.tstep = tstep
        self.temp = temp
        self.friction = friction

    def set_initial_velocities( self, temp ) : 
        # code for setting initial velocities
        self.velocities = np.zeros( self.positions.shape )

    def set_moving_atoms( self, statlist ) :
        self.moving_atoms = []
        self.themo_atoms = []
        self.force_atoms = []
        for i in range(len(statlist)) : 
            if statlist[i]>=0 : self.moving_atoms.append(i) 
            if statlist[i]==0 : self.thermo_atoms.append(i)
            if statlist[i]>0 : self.force_atoms.append(i)

    def runMD(self, nsteps):
        """ """
        for step in range(nsteps) :
            if friction>0 : 
                # Do thermostat step 
                for j in self.thermo_atoms : 

            # Update velocity by a half time step
            for j in self.moving_atoms :
                velocities[j,0] = velocities[j,0] + 0.5*forces[j,0]*tstep
                velocities[j,1] = velocities[j,1] + 0.5*forces[j,1]*tstep
                # Update position by a full time step
                positions[j,0]  = positions[j,0] + velocities[j,0]*tstep
                positions[j,1]  = positions[j,1] + velocities[j,1]*tstep
            # Calculate the new energy and forces
            pe, forces = potential (positions)

            # Add your non conservative force
            for j in self.force_atoms : 
                forces[j][0] += 
                forces[j][1] += 

            # Update velocity by a half time step
            for j in self.moving_atoms :
                velocities[j,0] = velocities[j,0] + 0.5*forces[j,0]*tstep
                velocities[j,1] = velocities[j,1] + 0.5*forces[j,1]*tstep

            if friction>0 : 
                # Do thermostat step
                for j in self.thermo_atoms : 

    def get_positions(self):
        return self.positions


