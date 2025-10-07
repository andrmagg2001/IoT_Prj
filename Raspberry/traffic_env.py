import random
import numpy as np
from problem_modulation import apply_step, compute_reward, MAX_CARS


class TrafficEnv:
    """
    Environment class for the Smart Traffic Light simulation.
    Manages the state (n1, n2, phase), applies actions, and computes rewards.
    """

    def __init__(self, n1 : int, n2 : int, phase : str) -> None:
        """
        Initialize environment with random starting values.

        Args:
            n1 (Optional[int]): Initial number of cars on road 1.
                                If None, a random value in [0, MAX_CARS] is used.
            n2 (Optional[int]): Initial number of cars on road 2.
                                If None, a random value in [0, MAX_CARS] is used.
            phase (Optional[str]): Initial phase identifier among {"S1","S2","S3","S4","S5"}.
                                   If None or invalid, "S1" is used.

        Notes:
            - Values for n1 and n2 are clamped to [0, MAX_CARS].
            - State is a tuple: (n1, n2, phase).
        """
        self.max_cars   = MAX_CARS
        self.state      = (random.randint(0, self.max_cars), random.randint(0, self.max_cars))
        self.state      = 0



    def reset(self) -> tuple[int, int, str]:
        """
        Reset the environment to an initial random state.

        Returns:
        tuple[int, int, str]: The new environment state represented as (n1, n2, phase).

        Notes:
            - Randomly assigns new values for the number of cars on both roads.
            - Resets the simulation step counter to zero.
            - Can be used at the start of each training episode in reinforcement learning.
        """
        self.state  = (random.randint(0, self.max_cars), random.randint(0, self.max_cars))
        self.steps  = 0
        return self.state



    def step(self, action: int) -> tuple[tuple[int, int, str], float]:
        """
        Execute one environment update step given an action.

        Args:
            action (int): The action chosen by the agent.
                        - 0 → Give green to TL1 (road 1).
                        - 1 → Give green to TL2 (road 2).

        Returns:
            tuple[tuple[int, int, str], float]: A tuple containing:
                - next_state (tuple[int, int, str]): The new state after applying the action.
                - reward (float): The reward obtained from the action.

        Notes:
            - Updates the environment by simulating traffic flow according to the action.
            - The reward is computed based on traffic reduction or balance.
            - The step counter is incremented at each call.
        """
        n1, n2  = self.state
        reward  = compute_reward(n1, n2, action)
        n1, n2  = apply_step(n1, n2, action)
        self.state = (n1, n2)
        self.steps += 1
        return self.state, reward  



    def render(self):
        """Print the current traffic situation."""
        n1, n2 = self.state
        print(f"Step {self.steps:02d} | Road1: {n1} cars | Road2: {n2} cars")



if __name__ == "__main__":
    env = TrafficEnv()
    state = env.reset()
    for _ in range(5):
        action = random.randint(0, 1)
        next_state, reward = env.step(action)
        print(f"Action: {action} -> Reward: {reward} | Next state: {next_state}")
        env.render()