import random

import pygame
import matplotlib.pyplot as plt
import PacmanGymWrapper.PacmanGameGym as PacmanGameGym
import gym
from gym import spaces
import numpy as np
from stable_baselines3 import A2C
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import VecFrameStack, VecNormalize
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import DQN
class PacmanGym(gym.Env):
    metadata = {"render_modes": [PacmanGameGym.PacmanGame.RenderType.HUMAN, PacmanGameGym.PacmanGame.RenderType.RGB_ARRAY]}

    def __init__(self, render_mode=None, render_fps=9999):
        self.core_game = PacmanGameGym.PacmanGameGym(fps=0, render_type=render_mode, external_inputs=True)
        self.i = 0
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.core_game.HEIGHT, self.core_game.WIDTH, 3), dtype=np.uint8)
        self._action_to_direction = {
            0: None,
            1: PacmanGameGym.PacmanGameGym.directions_API[0],
            2: PacmanGameGym.PacmanGameGym.directions_API[1],
            3: PacmanGameGym.PacmanGameGym.directions_API[2],
            4: PacmanGameGym.PacmanGameGym.directions_API[3],
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.observation = None
        self.reward = None
        self.done = None

    def reset(self, seed=None, options=None):
        self.i = 0
        self.core_game.full_reset()
        self.observation = self.core_game.get_board_rgb_array()
        return self.observation

    def step(self, action):
        # if action is None or action is np.NaN or not (0 <= action <= 4):
        #     raise ValueError(f'Available actions are from 0 to 4, requested action value {action}')
        self.i += 1
        print(action)
        direction = self._action_to_direction[action]
        self.core_game.external_input(direction)

        self.core_game.update()

        info = {
            "raw_score": self.core_game.score,
            "lives": self.core_game.pacman_lives,
            "number_of_pellets": self.core_game.number_of_small_pellets,
            "number_of_powerups": self.core_game.number_of_powerups
        }

        self.observation = self.core_game.get_board_rgb_array()

        self.reward = self.core_game.get_reward()
        self.core_game.reset_state()

        if self.reward > 100:
            self.reward = 200
        elif self.reward > 50:
            self.reward = 100

        self.done = self.core_game.done

        return self.observation, self.reward, self.done, info

    def close(self):
        self.core_game.run = False
        pygame.quit()
        pass

if __name__ == '__main__':
    env = gym.make("PacmanGym-v0", render_mode=PacmanGameGym.PacmanGame.RenderType.HUMAN)
    check_env(env, warn=True)
    env.reset()
    n_envs = 4
    vec_env = make_vec_env(lambda: env, n_envs=n_envs)
    vec_env = VecFrameStack(vec_env, n_stack=4)
    vec_env = VecNormalize(vec_env, norm_obs=True, norm_reward=True, clip_obs=10.0)

    model = DQN("CnnPolicy", vec_env, verbose=1)
    model.learn(total_timesteps=1000, log_interval=4)
    obs = env.reset()
    for _ in range(1000):
        action, _states = model.predict(obs)
        if type(action) == np.ndarray:
            obs, rewards, dones, info = env.step(action.item(0))
        else:
            obs, rewards, dones, info = env.step(action)

    env.close()
