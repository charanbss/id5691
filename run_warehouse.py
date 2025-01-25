import sys
import numpy as np

from PWLPlan import plan, Node
from vis import vis
from Create_MASTL_specs import create_multi_robot_specs
from task_locations import create_task_locations_list


def WareHouseStlPlanner():

    #Input task locations list from BHTA allocation
    task_locations_list = create_task_locations_list(25)


    x0s = []  # Initialize empty list for robot locations

    # First loop: Fill locations for robots 0-19 (pairs at y at 2 and 4)
    b = 0 
    b_dash = 0
    while b < 20 and b_dash <= 9:
        x0s.append([7 + 8*b_dash, 2])  # First robot in pair
        x0s.append([7 + 8*b_dash, 4])  # Second robot in pair
        b += 2
        b_dash += 1

    # Second loop: Fill locations for robots 20-24 (at y = 6)
    b_dash = 0
    while len(x0s) < 25 and b_dash <= 4:
        x0s.append([27 + 5*b_dash, 6])
        b_dash += 1

    x0s = x0s[:25]

    #Defining Warehouse Environment Parameters
    wall_half_width = 0.05
    A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    walls = []

    #Defining the boundaries of the warehouse
    walls.append(np.array([0, 0, 0, 80], dtype = np.float64))
    walls.append(np.array([100, 100, 0, 80], dtype = np.float64))
    walls.append(np.array([0, 100, 0, 0], dtype = np.float64))
    walls.append(np.array([0, 100, 80, 80], dtype = np.float64))    

    #Defining pod locations in the warehouse
    _pod_locs = []
    x_stacks = 16  # Number of stacks of pods in x direction 
    y_stacks = 4   # Number of stacks of pods in y direction

    for k in range(y_stacks):
        for i in range(x_stacks):
            for j in range(6):
                _pod_locs.append(np.array([1+10+5*i, 15 + 2*j + 13*k]))
                _pod_locs.append(np.array([1+10+5*i+2, 15 + 2*j + 13*k]))

    #Defining Pick Station Walls in the warehouse
    walls.append(np.array([5, 5, 74, 79], dtype = np.float64))
    walls.append(np.array([10, 10, 74, 79], dtype = np.float64))
    walls.append(np.array([20, 20, 74, 79], dtype = np.float64))
    walls.append(np.array([25, 25, 74, 79], dtype = np.float64))
    walls.append(np.array([35, 35, 74, 79], dtype = np.float64))
    walls.append(np.array([40, 40, 74, 79], dtype = np.float64))

    #Defining Replenishment Station Walls in the warehouse
    walls.append(np.array([1, 5, 5, 5], dtype = np.float64))
    walls.append(np.array([1, 5, 10, 10], dtype = np.float64))
    walls.append(np.array([1, 5, 20, 20], dtype = np.float64))
    walls.append(np.array([1, 5, 25, 25], dtype = np.float64))
    walls.append(np.array([1, 5, 35, 35], dtype = np.float64))
    walls.append(np.array([1, 5, 40, 40], dtype = np.float64))

    #Giving thickness to walls
    obs = []
    for wall in walls:
        if wall[0]==wall[1]:
            wall[0] -= wall_half_width
            wall[1] += wall_half_width
        elif wall[2]==wall[3]:
            wall[2] -= wall_half_width
            wall[3] += wall_half_width
        else:
            raise ValueError('wrong shape for axis-aligned wall')
        wall *= np.array([-1,1,-1,1])
        obs.append((A, wall))

    #Making Pod locations as static square obstacles
    pod_half_width = 0.50
    for pod_loc in _pod_locs:
        pod_loc = np.array([-(pod_loc[0] - pod_half_width), (pod_loc[0] + pod_half_width), -(pod_loc[1] - pod_half_width), (pod_loc[1] + pod_half_width)])
        obs.append((A,pod_loc))

    vmax = 1.30 #Max speed of an Amazon Kiva Robot (m/s)
    tmax = 10000 #Total time in which a batch of tasks should be completed (seconds)
    tw = 2 #Waiting time at pod location/pick station/charge station (seconds)

    #Creating STL specifications for each robot
    specs = create_multi_robot_specs(task_locations_list, obs, tw, tmax)

    # Calculate required number of segments, initial assumption of 3 per location
    max_locations = max(len(locs) for locs in task_locations_list)
    num_segs = max_locations * 3

    # Plan paths
    PWL = plan(x0s, specs, bloat=0.2, MIPGap=0.85, num_segs=num_segs, tmax=tmax, vmax=vmax)

    plots = [[obs, 'k']]
    return x0s, plots, PWL

if __name__ == '__main__':
    try:
        print("Starting warehouse simulation...")
        results = vis(WareHouseStlPlanner)
        print("Simulation completed successfully")
    except Exception as e:
        print(f"An error occurred during simulation: {str(e)}")

    

    


