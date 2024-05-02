from copy import copy
from gymnasium import spaces
import numpy as np
import gymnasium as gym

STATE = {
    "description_detail": 0,
    "interaction_pref": 0,
    "n_clarifications": 0,
    "documentation_detail": 0,
    "documentation_type": 0,
    "unit_tests": 0,
    "frameworks": 0,
    "file_structure": 0,
    "language": 0,
    "codebase": 0,
}


class SimulatedUser:
    def __init__(self):
        self.description_detail = 0
        self.language_proficiency = {
            'python': np.random.rand(),
            'javascript': np.random.rand(),
            'c++': np.random.rand(),
        }
        self.interaction_pref = 0.8
        self.documentation_detail_pref = np.random.rand()

    def get_description_detail(self, action):
        return 0.3 * np.random.rand() + 0.1

    def get_user_action(self, action):
        if action == 0:
            return self.get_description_detail(action)

class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"]}

    def __init__(self, n_agent_actions, n_simulated_user_actions):
        super().__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        
        self.action_space = spaces.Discrete(10)

        self.observation_space = spaces.Dict({
            "description_detail": spaces.Box(low=0, high=1.0, dtype=float),
            "interaction_pref": spaces.Box(low=0, high=1.0, dtype=float),
            "n_clarifications": spaces.Discrete(100),
            "documentation_detail": spaces.Discrete(3),
            "documentation_type": spaces.Discrete(2),
            "frameworks": spaces.Discrete(2),
            "file_structure": spaces.Discrete(2),
            "unit_tests": spaces.Discrete(2),
            "language": spaces.Discrete(2),
            "codebase": spaces.Discrete(2),
        })
        
        self.n_simulated_user_actions = n_simulated_user_actions
        self.n_agent_actions = n_agent_actions
        self.user = SimulatedUser()
        self.state = copy(STATE)
        self.iteration = 0

    def get_observation(self, action):
        state = copy(self.state)
        if state["description_detail"] == 0 and action != 0:
            # print(self.iteration, "no change", action)
            return state
        if action == 0: # ask for project description
            if state["description_detail"] == 0:
                state["description_detail"] = np.random.rand() * 0.5 + 0.1
        elif action == 1: # ask for interaction preference
            state["interaction_pref"] = self.user.interaction_pref
        elif action == 2: # ask for clarification
            state["description_detail"] += 0.15
            # print(self.iteration, "detail increased", state["description_detail"])
            state["n_clarifications"] += 1
        elif action == 3: # ask for documentation detail
            state["documentation_detail"] = 1
        elif action == 4: # ask for documentation type
            state["documentation_type"] = 1
        elif action == 5: # ask for unit tests
            if np.random.rand() > 0.25:
                state["unit_tests"] = 1
        elif action == 6: # ask for frameworks
            if state["language"] == 1:
                state["frameworks"] = 1
        elif action == 7: # ask for file structure
            if np.random.rand() > 0.25:
                state["file_structure"] = 1
        elif action == 8: # ask for language
            state["language"] = 1
        elif action == 9: # build codebase
            if (
                state["description_detail"] > 0.5 and
                state["unit_tests"] == 1 and
                state["frameworks"] == 1 and
                state["file_structure"] == 1 and
                state["language"] == 1 and
                state["documentation_detail"] > 0 and
                True
            ):
                if state["documentation_detail"] == 1:
                    if state["documentation_type"] > 0:
                        state["codebase"] = 1
                else:
                    state["codebase"] = 1
        s = "".join([k[:3] + str(v) + " " for k, v in state.items()])
        # print(self.iteration, action, s)
        return state
    
    def reward_function(self, action, observation):
        if action == 0:
            if observation["description_detail"] == 0:
                return 25
        if action == 2:
            if observation["description_detail"] > 0.75:
                return -5
        if observation["codebase"] == 1:
            return 100
        if action == 8:
            if observation["language"] != 1:
                return -10
        return -1
    
    def termination_function(self, observation):
        if observation["codebase"] == 1:
            print("done")
            return True
        return False
    
    def truncation_function(self, observation):
        """Truncate the episode if the agent has asked for too many clarifications"""
        if observation["n_clarifications"] > 5:
            # print("truncated")
            return True
        elif self.iteration > 50:
            # print("truncated")
            return True
        return False

    def step(self, action):
        self.iteration += 1
        observation = copy(self.get_observation(action))
        reward = self.reward_function(action, observation)
        terminated = self.termination_function(observation)
        truncated = False
        # if not terminated:
        #     truncated = self.truncation_function(observation)
            # reward = -1
        info = {}
        # print(action, observation, reward)
        self.state = observation
        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        self.iteration = 0
        self.state = copy(STATE)
        return self.state, {}
    
    def render(self):
        pass

    def close(self):
        print("closing")