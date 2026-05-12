#%%
# ./examples/scenario_sun_earth.py
#
# Sun-Earth two-body simulation using SPICE ephemerides (DE430).
# Demonstrates multi-body gravitational setup and EphemerisConverter
# integration. Corresponds to Section 5.4 of the paper.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace Inc.
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

import numpy as np

from Basilisk.simulation import spacecraft, ephemerisConverter
from Basilisk.utilities import (SimulationBaseClass, macros, vizSupport,
                                simIncludeGravBody, orbitalMotion)
from Basilisk.topLevelModules import pyswice
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
    grav_bodies = grav_factory.createBodies(['sun', 'earth'])
    grav_bodies['earth'].isCentralBody = True

    time_init = "2000 Jan 1 11:59:28.000 (UTC)"
    grav_factory.createSpiceInterface(
        bskPath + '/supportData/EphemerisData/',
        time_init, epochInMsg=True)
    epoch_msg = grav_factory.epochMsg

    earth_ephem = ephemerisConverter.EphemerisConverter()
    simulation_obj.AddModelToTask("simulation_task", earth_ephem)
    grav_factory.spiceObject.zeroBase = 'Earth'
    earth_ephem.addSpiceInputMsg(grav_factory.spiceObject.planetStateOutMsgs[1])

    pyswice.furnsh_c(grav_factory.spiceObject.SPICEDataPath + 'de430.bsp')  # solar system bodies
    pyswice.furnsh_c(grav_factory.spiceObject.SPICEDataPath + 'naif0012.tls')  # leap second file
    pyswice.furnsh_c(grav_factory.spiceObject.SPICEDataPath + 'de-403-masses.tpc')  # solar system masses
    pyswice.furnsh_c(grav_factory.spiceObject.SPICEDataPath + 'pck00010.tpc')  # generic Planetary Constants

    
    mu = grav_factory.gravBodies['earth'].mu
    
    oe = orbitalMotion.ClassicElements()
    rLEO = 7000. * 1000
    oe.a     = rLEO    # m
    oe.e     = 0.0001
    oe.i     = 33.3  * macros.D2R
    oe.Omega = 48.2  * macros.D2R
    oe.omega = 347.8 * macros.D2R
    oe.f     = 85.3  * macros.D2R
    position_inertial, velocity_inertial = orbitalMotion.elem2rv(mu, oe)
    
    spacecraft_obj.hub.r_CN_NInit = position_inertial       # m   - r_BN_N
    spacecraft_obj.hub.v_CN_NInit = velocity_inertial       # m/s - v_BN_N

    mean_motion = np.sqrt(mu / oe.a / oe.a / oe.a)
    orbital_period_seconds = 2. * np.pi / mean_motion

    if use_spherical_harmonics:
        simulation_time = macros.sec2nano(3. * orbital_period_seconds)
    else:
        simulation_time = macros.sec2nano(0.75 * orbital_period_seconds)
    
    viz = vizSupport.enableUnityVisualization(simulation_obj,
                                        "simulation_task",
                                        spacecraft_obj,
                                        liveStream=False,
                                        saveFile = __file__
                                        )
    viz.epochInMsg.subscribeTo(epoch_msg)

    simulation_obj.InitializeSimulation()
    simulation_obj.ConfigureStopTime(simulation_time)
    simulation_obj.ExecuteSimulation()

if __name__ == "__main__":
    run(1.0,        # Simulation time step in seconds
        1000.0,     # Total simulation time in seconds
        True       # Flag to use spherical harmonics
        )