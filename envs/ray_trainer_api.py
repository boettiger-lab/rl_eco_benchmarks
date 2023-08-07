import torch

# from ray.tune import register_env
from ray import tune
from gymnasium.envs.registration import register

from ray.rllib.algorithms.a2c import A2CConfig
from ray.rllib.algorithms.a3c import A3CConfig
from ray.rllib.algorithms.maml import MAMLConfig
from ray.rllib.algorithms.apex_dqn.apex_dqn import ApexDQNConfig
from ray.rllib.algorithms.dqn.dqn import DQNConfig
from ray.rllib.algorithms.ddpg.ddpg import DDPGConfig
from ray.rllib.algorithms.td3 import TD3Config
from ray.rllib.algorithms.ars import ARSConfig
from ray.rllib.algorithms.appo import APPOConfig
from ray.rllib.algorithms.ddppo import DDPPOConfig
from ray.rllib.algorithms.ppo import PPOConfig

from ray.rllib.agents.ppo import PPOTrainer

from base_env import eco_env, ray_eco_env
from env_factories import env_factory, ray_env_factory

class ray_trainer:
	""" an RL agent training on one of ray's algorithms. """

	def __init__(
		self, 
		algo_name, 
		config, 
		env_model_name,
		n_act,
	):
		#
		# env
		tune.register_env(
			env_model_name, 
			lambda env_config: ray_env_factory(env_config=env_config)
		)
		print("registered with Ray tune!")
		# register_env(env_name, env_class)
		#
		# algo
		self.algo_name = algo_name
		self.algo_config = self._make_config()
		#
		# boiler plate algo settings
		# self.config.training(vf_clip_param = 50.0)
		self.algo_config.disable_env_checking = True # otherwise it complains about the env
		self.algo_config.num_envs_per_worker=30
		self.algo_config = self.algo_config.resources(num_gpus=torch.cuda.device_count())
		self.algo_config.framework_str="torch"
		self.algo_config.create_env_on_local_worker = True
		# 
		# config.env
		self.algo_config.env=env_model_name
		self.algo_config.env_config = config
		#
		# agent
		self.agent = self.algo_config.build()

	def _make_config(self):
		config_dict = {
			'a2c': A2CConfig,
			'a3c': A3CConfig,
			'appo': APPOConfig,
			'ddppo': DDPPOConfig,
			'ppo': PPOConfig,
			'maml': MAMLConfig,
			'apex': ApexDQNConfig,
			'dqn': DQNConfig,
			'ddpg': DDPGConfig,
			'td3': TD3Config,
			'ars': ARSConfig,
		}
		return config_dict[self.algo_name]()

	def train(
		self, 
		path_to_checkpoint="cache", 
		verbose = True
	):
		for i in range(iterations):
			if verbose:
				print(f"iteration nr. {i}", end="\r")
			self.agent.train()
		checkpoint = self.agent.save(os.path.join(path_to_checkpoint, f"PPO{iterations}_checkpoint"))
		return agent

