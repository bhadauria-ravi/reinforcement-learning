import numpy as np
from timeit import default_timer as timer


class EpsilonGreedy(object):
    def __init__(self, epsilon, testbed, alpha=0.001, seed=1993):
        self.epsilon = epsilon
        self.testbed = testbed
        self.alpha = alpha
        self.seed = seed
        self.expected_rewards = np.zeros_like(self.testbed.mu, dtype=np.float32)
        self.rng = np.random.default_rng(self.seed)

    def _explore_or_exploit(self):
        if self.rng.random() > self.epsilon:
            return np.argmax(self.expected_rewards)
        else:
            return self.rng.integers(self.testbed.n)

    def _update_action_value_expectation(self, i):
        old_expected_reward = self.expected_rewards[i]
        reward = self.testbed.get_dist(i)
        self.expected_rewards[i] = old_expected_reward + self.alpha * (
            reward - old_expected_reward
        )
        return reward

    def run(self, steps, echo_every=100):
        rewards = np.zeros(steps, dtype=np.float32)
        start = timer()
        for s in range(steps):
            action_arg = self._explore_or_exploit()
            rewards[s] = self._update_action_value_expectation(action_arg)
            if ((s + 1) % echo_every) == 0:
                print(f"Finished step: {s+1}, elapsed time: {timer()-start}")
        return rewards

    def __str__(self) -> str:
        return (
            f"Epsilon: {self.epsilon}\n"
            f"Relaxation: {self.alpha}\n"
            f"Random Seed: {self.seed}\n"
            f"TestBed: {self.testbed.__str__()}\n"
        )
