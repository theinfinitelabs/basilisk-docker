#%%
# ./examples/scenario_spacecraft.py
#
# Baseline spacecraft simulation without orbital dynamics.
# Demonstrates simulation container setup, process/task hierarchy,
# and Vizard visualization. Corresponds to Section 5.2 of the paper.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace Inc.
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

from Basilisk.simulation import spacecraft
from Basilisk.utilities import SimulationBaseClass, macros, vizSupport

def run(time_step, simulation_time):
    simulation_obj = SimulationBaseClass.SimBaseClass()
    dynamics_process = simulation_obj.CreateNewProcess("simulation_process")
    simulation_time_step = macros.sec2nano(time_step)
    dynamics_process.addTask(
        simulation_obj.CreateNewTask(
            "simulation_task", simulation_time_step))

    spacecraft_obj = spacecraft.Spacecraft()
    spacecraft_obj.ModelTag = "bsk_sat"
    simulation_obj.AddModelToTask("simulation_task", spacecraft_obj)

    vizSupport.enableUnityVisualization(
        simulation_obj, "simulation_task",
        spacecraft_obj, liveStream=False,
        saveFile=__file__)

    simulation_obj.InitializeSimulation()
    simulation_obj.ConfigureStopTime( macros.sec2nano(simulation_time) )
    simulation_obj.ExecuteSimulation()

if __name__ == "__main__":
    run(1.0, 1000.0)