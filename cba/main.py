from dialogue_manager import DialogueManager
from environment import CustomEnv
from stable_baselines3 import PPO

def main():

    N_AGENT_ACTIONS = 10
    SIMULATED_USER_ACTIONS = 8
    # since we are not using images, the observation space is 1D
    model = PPO.load("../ppo_custom_env_backup")
    env = CustomEnv(N_AGENT_ACTIONS, SIMULATED_USER_ACTIONS)
    # model = PPO("MultiInputPolicy", env, verbose=1, n_epochs=100)
    # model.learn(total_timesteps=25000)
    dialogue_manager = DialogueManager(model, env)
    dialogue_manager.run()

if __name__ == "__main__":
    main()