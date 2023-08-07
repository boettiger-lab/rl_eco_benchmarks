import numpy as np
from dynamical_system import base_params_obj
from base_env import eco_env, ray_eco_env
from util import dict_pretty_print

##############################################################
####################### Example 1 ############################
##############################################################
print("\n\n" + "env 1 test:" + "\n\n")

def _unparametrized_dyn(X: np.float32):
	return np.float32([X * (1 - X)])

def _penalty_fn(t: int):
	return -1 / (t+1)

_metadata = {
	#
	# which env class
	'n_sp':  1,
	'n_act': 1,
	'_harvested_sp': [0],
	#
	# about episodes
	'init_pop': np.float32([0.5]),
	'reset_sigma': 0.01,
	'tmax': 1000,
	'penalty_fn': _penalty_fn,
	'extinct_thresh': 0.05,
	#
	# about dynamics / control
	'var_bound': 2,
	'_costs': np.zeros(1, dtype=np.float32),
	'_prices': np.ones(1, dtype=np.float32),
}

env_1 = eco_env(
	metadata = _metadata,
	dyn_fn = _unparametrized_dyn, 
	dyn_params = {}, 
	non_stationary = False, 
	non_stationarities = {},
	)

env_1.reset()
for _ in range(10):
	obs, rew, term, _, info = env_1.step(action = [-0.9])
	dict_pretty_print({**info, 'state': obs})


##############################################################
####################### Example 2 ############################
##############################################################
print("\n\n" + "env 2 test:" + "\n\n")

_params = {'r': 2, 'K': 1}

def _parametrized_dyn(X: np.float32, params: dict):
	P = params
	return np.float32([P["r"] * X * (1 - X / P["K"])])

env_2 = eco_env(
	metadata = _metadata,
	dyn_fn = _parametrized_dyn, 
	dyn_params = _params, 
	non_stationary = False, 
	non_stationarities = {},
	)

env_2.reset()
for _ in range(10):
	obs, rew, term, _, info = env_2.step(action = [-0.9])
	dict_pretty_print({**info, 'state': obs})


##############################################################
####################### Example 3 ############################
##############################################################
print("\n\n" + "env 3 test:" + "\n\n")

def _r(t):
	return 1 + t/1000


env_3 = eco_env(
	metadata = _metadata,
	dyn_fn = _parametrized_dyn, 
	dyn_params = _params, 
	non_stationary = True, 
	non_stationarities = {"r": _r},
	)

env_3.reset()
for _ in range(10):
	obs, rew, term, _, info = env_3.step(action = [-0.9])
	dict_pretty_print({**info, 'state': obs})


##############################################################
####################### Example 4 ############################
##############################################################
print("\n\n" + "env 4 test:" + "\n\n")

def _dyn_4(X, Y, Z, params):
	P = params
	return np.float32([P['rx'] * X * (1 - X / (1 - Z)), P['ry'] *Y * (1 - Y / (1 - Z)), P['rz'] *(X + Y) * Z * (1 - Z)])

def _penalty_fn_4(t: int):
	return - 1000 / (t+1)

_metadata_4 = {
	#
	# which env class
	'n_sp':  3,
	'n_act': 2,
	'_harvested_sp': [0,1],
	#
	# about episodes
	'init_pop': np.float32([0.5, 0.5, 0.1]),
	'reset_sigma': 0.01,
	'tmax': 1000,
	'penalty_fn': _penalty_fn_4,
	'extinct_thresh': 0.05,
	#
	# about dynamics / control
	'var_bound': 2,
	'_costs': np.zeros(2, dtype=np.float32),
	'_prices': np.ones(2, dtype=np.float32),
}

def _rx(t):
	return 1 + t/1000

_params_4 = {'rx': 1, 'ry': 2, 'rz': 0.1}

_non_stationarities_4 = {'rx': _rx}

env_4 = eco_env(
	metadata = _metadata_4,
	dyn_fn = _dyn_4, 
	dyn_params = _params_4, 
	non_stationary = True, 
	non_stationarities = _non_stationarities_4,
	)

env_4.reset()
for _ in range(10):
	obs, rew, term, _, info = env_4.step(action = [-1])
	dict_pretty_print({**info, 'state': obs}, dict_name = "step info")


##############################################################
####################### Example 5 ############################
##############################################################

_config_5 = {
	'metadata': _metadata_4,
	'dyn_fn': _dyn_4,
	'dyn_params': _params_4,
	'non_stationary': True,
	'non_stationarities': _non_stationarities_4,
}

env_5 = ray_eco_env(config=_config_5)

env_5.reset()
for _ in range(10):
	obs, rew, term, _, info = env_5.step(action = [-1])
	dict_pretty_print({**info, 'state': obs}, dict_name = "step info")


#####################################################################
#################### RAY TRAINER EXAMPLE ############################
#####################################################################

from ray_trainer_api import ray_trainer

