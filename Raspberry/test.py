# simulate_policy.py
import numpy as np, matplotlib.pyplot as plt
from traffic_env import TrafficEnv
from problem_modulation import MAX_CARS

Q = np.load("data/models/qtable_latest.npy")
env = TrafficEnv()
state = env.reset()[:2]
hist, cum_reward = [], 0
STEPS = 200

for t in range(STEPS):
    n1, n2 = state
    action = int(np.argmax(Q[n1, n2, :]))
    next_state, reward = env.step(action)
    cum_reward += reward
    hist.append((t, n1, n2, action, reward))
    state = next_state[:2]

print("Cumulative reward:", cum_reward)

t, r1, r2 = zip(*[(h[0], h[1], h[2]) for h in hist])
plt.figure(figsize=(10,4))
plt.plot(t, r1, label="Road1 cars")
plt.plot(t, r2, label="Road2 cars")
plt.title("Greedy Policy Simulation (no Arduino)")
plt.xlabel("Step"); plt.ylabel("Cars"); plt.grid(True); plt.legend(); plt.show()