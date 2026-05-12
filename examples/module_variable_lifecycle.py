#%%
# ./examples/module_variable_lifecycle.py
#
# Demonstrates Basilisk module execution lifecycle: variable state
# before initialization, after InitializeSimulation(), and after
# SingleStepProcesses(). Corresponds to Section 4.3 of the paper.
#
# Author:       Anubhav Gupta
# Affiliation:  University of Colorado Boulder
#               In Orbit Aerospace Inc.
# Organization: Infinite Labs
# License:      MIT
# ---------------------------------------------------------------------

from Basilisk.moduleTemplates import cModuleTemplate
from Basilisk.utilities import SimulationBaseClass, macros

sim_obj = SimulationBaseClass.SimBaseClass()
dyn_process = sim_obj.CreateNewProcess("dynamicsProcess")
dyn_task = sim_obj.CreateNewTask("dynamicsTask", macros.sec2nano(5.))
dyn_process.addTask(dyn_task)

module_obj = cModuleTemplate.cModuleTemplate()
sim_obj.AddModelToTask("dynamicsTask", module_obj, 10)

module_obj.dummy = -10
print(f'Before initialization: {module_obj.dummy}')  # -10.0

sim_obj.InitializeSimulation()
print(f'After initialization: {module_obj.dummy}')   # 0.0

sim_obj.TotalSim.SingleStepProcesses()
print(f'After execution: {module_obj.dummy}')        # 1.0