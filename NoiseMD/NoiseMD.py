import numpy as np
import scipy.stats 
import matplotlib.pyplot as plt


class NoiseMD:
    def __init__(self):
        self.positions = np.zeros(10)
        self.velocities = []
        self.energy = []
        self.strides = []
        self.methods = []

    def create_initial_positions(self, nx, ny, a=2**(2/3)):
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
        self.initial_positions = np.copy(self.positions)

    def potential(self):
        self.potent = 0
        self.forces = np.zeros(self.positions.shape)
        for i in range(1, self.natoms) :
            for j in range(i) :
                r2 = (self.positions[i,0] - self.positions[j,0])**2+(self.positions[i,1] - self.positions[j,1])**2
                r6 = r2*r2*r2
                r12 = r6*r6
                self.potent += 4*((1/r12)-(1/r6))

                self.forces[i,:] += 4*(self.positions[i,:] - self.positions[j,:])*((12/(r12*r2))-(6/(r2*r6)))
                self.forces[j,:] += -4*(self.positions[i,:] - self.positions[j,:])*((12/(r12*r2))-(6/(r2*r6)))
        return self.potent

    def set_params( self, tstep, temp, friction, nc_const, delx, dely ) : 
        self.tstep = tstep
        self.temp = temp
        self.friction = friction
        self.nc_const = nc_const
        self.delx = delx
        self.dely = dely

    def attach_method( self, stride, method ) :
        self.strides.append(stride)
        self.methods.append(method)

    def set_initial_velocities( self, temp ) : 
        # code for setting initial velocities
        self.velocities = np.zeros( self.positions.shape )
        for i in self.moving_atoms:
            self.velocities[i,0] = np.sqrt(temp)*np.random.normal()
            self.velocities[i,1] = np.sqrt(temp)*np.random.normal()
        for i in self.force_atoms:
            self.velocities[i,0] = 0
            self.velocities[i,1] = 0


    def set_moving_atoms( self, statlist ) :
        self.moving_atoms = []
        self.thermo_atoms = []
        self.force_atoms = []
        for i in range(len(statlist)) : 
            if statlist[i]>=0 : self.moving_atoms.append(int(i)) 
            if statlist[i]==0 : self.thermo_atoms.append(int(i))
            if statlist[i]>0 : self.force_atoms.append(int(i))

    def Kinet(self) :
        v2 = np.square(self.velocities)
        total_vel = np.sum(v2)
        return 0.5*total_vel

    def runMD(self, nsteps):
        self.therm = 0        
        if self.friction>0 :
            therm1 = np.exp(-self.tstep*self.friction) # change here
            therm2 = np.sqrt((self.temp*(1-np.exp(-2*self.tstep*self.friction)))) # change here
        for i in self.force_atoms:
            self.positions[i][0] += self.delx
            self.positions[i][1] += self.dely
        self.potential()
        for step in range(nsteps) :
            if self.friction>0 : 
                # Do thermostat step 
                
                self.therm = self.therm + self.Kinet()
                for j in self.thermo_atoms : 
                    self.velocities[j,0] = self.velocities[j,0]*therm1 + therm2*np.random.normal()
                    self.velocities[j,1] = self.velocities[j,1]*therm1 + therm2*np.random.normal()
                self.therm = self.therm - self.Kinet()

            # Update velocity by a half time step
            for j in self.moving_atoms :
                self.velocities[j,0] = self.velocities[j,0] + 0.5*self.forces[j,0]*self.tstep
                self.velocities[j,1] = self.velocities[j,1] + 0.5*self.forces[j,1]*self.tstep
                # Update position by a full time step
                self.positions[j,0]  = self.positions[j,0] + self.velocities[j,0]*self.tstep
                self.positions[j,1]  = self.positions[j,1] + self.velocities[j,1]*self.tstep
            # Calculate the new energy and forces
            self.potential()
            
            # Add your non conservative force
            for j in self.force_atoms : 
                self.forces[j][0] = self.forces[j][0] - self.nc_const*(self.positions[j][1]-self.initial_positions[j][1])
                self.forces[j][1] = self.forces[j][1] + self.nc_const*(self.positions[j][0]-self.initial_positions[j][0])

            # Update velocity by a half time step
            for j in self.moving_atoms :
                self.velocities[j,0] = self.velocities[j,0] + 0.5*self.forces[j,0]*self.tstep
                self.velocities[j,1] = self.velocities[j,1] + 0.5*self.forces[j,1]*self.tstep


            if self.friction>0 : 
                # Do thermostat step
                self.therm = self.therm + self.Kinet()
                for j in self.thermo_atoms : 
                    self.velocities[j,0] = self.velocities[j,0]*therm1 +therm2*np.random.normal()
                    self.velocities[j,1] = self.velocities[j,1]*therm1 +therm2*np.random.normal()
                self.therm = self.therm - self.Kinet()            
            
            
            for i in range(len(self.methods)) :
                if step%self.strides[i]==0 : self.methods[i](self)
                


    def get_positions(self):
        return self.positions

