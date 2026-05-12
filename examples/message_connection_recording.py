#%%
# ---------------------------------------------------------------------
# ./examples/message_connection_recording.py
#
# Demonstrates Basilisk message connection and state recording:
# subscribeTo() for module-to-module message passing, recorder()
# for data logging, and NumPy array access via .times().
# Corresponds to Section 4.4 of the paper.
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

# Instantiate two modules
module_a = cModuleTemplate.cModuleTemplate()
module_a.ModelTag = "module_a"

module_b = cModuleTemplate.cModuleTemplate()
module_b.ModelTag = "module_b"

sim_obj.AddModelToTask("dynamicsTask", module_a, 20)
sim_obj.AddModelToTask("dynamicsTask", module_b, 10)

# Connect module_b input to module_a output via subscribeTo()
module_b.dataInMsg.subscribeTo(module_a.dataOutMsg)

# Attach a recorder to module_a output — record every update
msg_log = module_a.dataOutMsg.recorder()
sim_obj.AddModelToTask("dynamicsTask", msg_log)

# Attach a sparse recorder to module_b output — record at specified interval
msg_log_sparse = module_b.dataOutMsg.recorder(macros.sec2nano(20.))
sim_obj.AddModelToTask("dynamicsTask", msg_log_sparse)

sim_obj.InitializeSimulation()
sim_obj.ConfigureStopTime(macros.sec2nano(100.))
sim_obj.ExecuteSimulation()

# Access logged data as NumPy arrays
time_data        = msg_log.times() * macros.NANO2SEC
time_data_sparse = msg_log_sparse.times() * macros.NANO2SEC

print(f'Number of recorded samples (every update):       {len(time_data)}')
print(f'Number of recorded samples (sparse, 20s period): {len(time_data_sparse)}')
print(f'\nRecorded time steps (every update, s):  {time_data}')
print(f'Recorded time steps (sparse, s):        {time_data_sparse}')