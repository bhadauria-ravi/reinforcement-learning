from cgi import test
import numpy as np
from testbed import TestBed
from experiment import BanditExperiment
from joblib import Parallel, delayed


def do_single_run(num_bandits, steps, epsilon, alpha, seed1, seed2):
    testbed = TestBed(num_bandits, seed1)
    epg = BanditExperiment(epsilon, testbed, alpha, seed2)
    return epg.run(steps), np.max(testbed.mu)


def avg_runs(num_bandits, num_runs, steps, epsilon, alpha, seed, workers=1):
    rng = np.random.default_rng(seed)
    rewards, max_expected_reward = zip(*Parallel(n_jobs=workers)(
        delayed(do_single_run)(
            num_bandits, steps, epsilon, alpha, rng.integers(10000), rng.integers(10000)
        )
        for _ in range(num_runs)
    ))
    return np.mean(np.array(rewards), axis=0), np.mean(np.array(max_expected_reward), axis=0)


def main():
    rewards, _ = avg_runs(
        num_bandits=10,
        num_runs=2000,
        steps=1000,
        epsilon=0.1,
        alpha=None,
        seed=1993,
        workers=5,
    )
    print(rewards)


if __name__ == "__main__":
    main()
