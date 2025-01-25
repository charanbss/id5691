import numpy as np
from PWLPlan import Node


def create_location_regions(locations_list, half_length=0.5):
    """
    Convert list of location points into square regions
    """
    A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    regions = []

    for loc in locations_list:
        # Convert point to square region like in doorpuzzle-1
        region = np.array([
            -(loc[0] - half_length),
            (loc[0] + half_length),
            -(loc[1] - half_length),
            (loc[1] + half_length)
        ])
        regions.append((A, region))

    return regions


def create_sequential_visit_spec(regions, obstacles, tw, tmax):
    """
    Create STL specification for visiting regions in sequence while avoiding obstacles

    Parameters:
    regions: List of (A,b) tuples defining regions to visit
    obstacles: List of (A,b) tuples defining obstacles to avoid
    tw: Time to stay at each location
    tmax: Maximum time to complete all visits
    """
    # Create obstacle avoidance specification
    avoid_obs = Node('and', deps=[
        Node('negmu', info={'A': A, 'b': b})
        for A, b in obstacles
    ])
    # Always avoid obstacles throughout the entire time
    always_avoid = Node('A', deps=[avoid_obs], info={'int': [0, tmax]})

    # Create basic predicate nodes for being in each region
    stay_nodes = [
        Node('mu', info={'A': region[0], 'b': region[1]})
        for region in regions
    ]

    # Create "stay for tw" nodes
    stay_for_tw = [
        Node('A', deps=[stay_node], info={'int': [0, tw]})
        for stay_node in stay_nodes
    ]

    # Create eventually nodes for sequential visiting
    visit_nodes = []
    curr_time = 0
    for stay in stay_for_tw:
        visit = Node('F', deps=[stay], info={'int': [curr_time, tmax]})
        visit_nodes.append(visit)
        curr_time += tw

    # Combine visit requirements AND obstacle avoidance
    spec = Node('and', deps=visit_nodes + [always_avoid])

    return spec


def create_multi_robot_specs(all_robot_locations, obstacles, tw, tmax):
    """
    Create STL specifications for multiple robots
    Each robot has its own sequence of locations to visit
    """
    specs = []

    # Create spec for each robot
    for robot_locations in all_robot_locations:
        # Convert locations to regions
        regions = create_location_regions(robot_locations)

        # Create sequential visit spec for this robot
        robot_spec = create_sequential_visit_spec(regions, obstacles, tw, tmax)
        specs.append(robot_spec)

    print(len(specs))

    return specs
