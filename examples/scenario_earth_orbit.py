#%%
# ./examples/scenario_earth_orbit.py
#
# Spacecraft in Earth orbit with Keplerian initial conditions and
# optional J2 spherical harmonic perturbations via the GGM03S model.
# Corresponds to Section 5.3 of the paper.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace Inc.
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

import numpy as np

from Basilisk.simulation import spacecraft
from Basilisk.utilities import (SimulationBaseClass, macros, vizSupport,
                                simIncludeGravBody, orbitalMotion)
from Basilisk import __path__
bskPath = __path__[0]

def run(time_step, simulation_time, use_spherical_harmonics=True):
    simulation_obj = SimulationBaseClass.SimBaseClass()
    dynamics_process = simulation_obj.CreateNewProcess("simulation_process")
    simulation_time_step = macros.sec2nano(time_step)
    dynamics_process.addTask(
        simulation_obj.CreateNewTask(
            "simulation_task", simulation_time_step))

    spacecraft_obj = spacecraft.Spacecraft()
    spacecraft_obj.ModelTag = "bsk_sat"
    simulation_obj.AddModelToTask("simulation_task", spacecraft_obj)

    grav_factory = simIncludeGravBody.gravBodyFactory()
    planet = grav_factory.createEarth()
    planet.isCentralBody = True

    if use_spherical_harmonics:
        planet.useSphericalHarmonicsGravityModel(bskPath + '/supportData/LocalGravData/GGM03S-J2-only.txt', 2)

    mu = planet.mu
    spacecraft_obj.gravField.gravBodies = \
        spacecraft.GravBodyVector(
            list(grav_factory.gravBodies.values()))

    oe = orbitalMotion.ClassicElements()
    oe.a     = 7000. * 1000    # m
    oe.e     = 0.0001
    oe.i     = 33.3  * macros.D2R
    oe.Omega = 48.2  * macros.D2R
    oe.omega = 347.8 * macros.D2R
    oe.f     = 85.3  * macros.D2R

    r_N, v_N = orbitalMotion.elem2rv(mu, oe)
    spacecraft_obj.hub.r_CN_NInit = r_N
    spacecraft_obj.hub.v_CN_NInit = v_N

    n = np.sqrt(mu / oe.a**3)
    T = 2. * np.pi / n

    vizSupport.enableUnityVisualization(
        simulation_obj, "simulation_task",
        spacecraft_obj, liveStream=False,
        saveFile=__file__)

    simulation_obj.InitializeSimulation()
    simulation_obj.ConfigureStopTime( macros.sec2nano(simulation_time) )
    simulation_obj.ExecuteSimulation()

if __name__ == "__main__":
    run(1.0,        # Simulation time step in seconds
        1000.0,     # Total simulation time in seconds
        False       # Flag to use spherical harmonics
        )