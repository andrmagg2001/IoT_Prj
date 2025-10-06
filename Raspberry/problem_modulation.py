MAX_CARS    = 10
THRESHOLD   = (3, 7)

def traffic_level(n: int, thresholds=THRESHOLD) -> str:
    """
    Classifies the traffic level on a single road as 'low', 'medium', or 'high'.
    - low    : n <= thresholds[0]
    - medium : thresholds[0] < n <= thresholds[1]
    - high   : n > thresholds[1]
    """
    lo, hi = thresholds
    if n <= lo:
        return "low"
    if n <= hi:
        return "medium"
    return "high"


def compute_reward(n1: int, n2: int, action: int, thresholds=THRESHOLD) -> int:
    """
    Computes the reward (+1, 0, -1) based on the traffic levels (low/medium/high).
    action: 0 -> give green light to TL1 (road 1), 1 -> give green light to TL2 (road 2).

    Rules:
      +1 : if you give green to the road with HIGHER traffic level (high > medium > low)
       0 : if both levels are EQUAL (e.g., medium vs medium) or both low
      -1 : if you give green to the road with LOWER traffic level
    """
    lvl1 = traffic_level(n1, thresholds)
    lvl2 = traffic_level(n2, thresholds)

    order = {"low": 0, "medium": 1, "high": 2}
    s1, s2 = order[lvl1], order[lvl2]

    if s1 == s2:
        return 0

    if action == 0 and s1 > s2:
        return +1
    if action == 1 and s2 > s1:
        return +1
    return -1



def clamp_cars(n: int, max_cars: int = MAX_CARS) -> int:
    """
    Limits the number of cars to the range [0, max_cars].
    """
    return max(0, min(n, max_cars))


def apply_step(n1: int, n2: int, action: int, max_cars: int = MAX_CARS) -> tuple[int, int]:
    """
    Updates (n1, n2) in a simple way:
      - The road with the green light lets 1 to 3 cars pass.
      - The other road receives 0 to 2 new cars.
    Always applies the limits [0, max_cars].
    """
    import random

    if action == 0:  
        n1 = clamp_cars(n1 - random.randint(1, 3), max_cars)
        n2 = clamp_cars(n2 + random.randint(0, 2), max_cars)
    else:
        n2 = clamp_cars(n2 - random.randint(1, 3), max_cars)
        n1 = clamp_cars(n1 + random.randint(0, 2), max_cars)

    return n1, n2


if __name__ == "__main__":
    n1, n2 = 4, 9      
    action = 0         
    r = compute_reward(n1, n2, action)   
    n1, n2 = apply_step(n1, n2, action)  
    print("reward:", r, "next:", (n1, n2))