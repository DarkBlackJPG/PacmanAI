
from gym.envs.registration import register

from PacmanGym import PacmanGym

environments = [['PacmanGym', 'v0']]

for environment in environments:
    register(
        id='{}-{}'.format(environment[0], environment[1]),
        entry_point='PacmanGymWrapper:{}'.format(environment[0]),
        nondeterministic=True
    )