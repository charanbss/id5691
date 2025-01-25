def create_task_locations_list(n):
    """
    Create list of safe task locations for n robots
    Using only corridor spaces between pods
    
    Parameters:
    n : int
        Number of robot task lists to return (max 25, default 25)
    """
    # Safe x coordinates (in corridors between pod columns)
    safe_x = [
        8,      # First corridor
        13,     # Between pods 1-2  
        18,     # Between pods 2-3
        23,     # Between pods 3-4
        28,     # Between pods 4-5
        33,     # Between pods 5-6
        38,     # Between pods 6-7
        43,     # Between pods 7-8
        48,     # Between pods 8-9
        53,     # Between pods 9-10
        58,     # Between pods 10-11
        63,     # Between pods 11-12
        68,     # Between pods 12-13
        73,     # Between pods 13-14
        78,     # Between pods 14-15
        83      # Between pods 15-16
    ]

    # Safe y coordinates (in corridors between pod rows)
    safe_y = [
        8,      # Below pods
        12,     # First corridor
        26,     # Second corridor
        41,     # Third corridor
        56,     # Fourth corridor
        68      # Above pods
    ]

    # Create task list for each robot with safe corridor locations
    task_locations_list = [
        # Robots 1-5 (working in first section)
        [[safe_x[0], safe_y[0]], [safe_x[1], safe_y[1]], [safe_x[2], safe_y[1]], [safe_x[0], safe_y[2]]],
        [[safe_x[1], safe_y[0]], [safe_x[2], safe_y[1]], [safe_x[3], safe_y[1]], [safe_x[1], safe_y[2]]],
        [[safe_x[2], safe_y[0]], [safe_x[3], safe_y[1]], [safe_x[4], safe_y[1]], [safe_x[2], safe_y[2]]],
        [[safe_x[3], safe_y[0]], [safe_x[4], safe_y[1]], [safe_x[5], safe_y[1]], [safe_x[3], safe_y[2]]],
        [[safe_x[4], safe_y[0]], [safe_x[5], safe_y[1]], [safe_x[6], safe_y[1]], [safe_x[4], safe_y[2]]],
        
        # Robots 6-10 (working in second section)
        [[safe_x[5], safe_y[1]], [safe_x[6], safe_y[2]], [safe_x[7], safe_y[2]], [safe_x[5], safe_y[3]]],
        [[safe_x[6], safe_y[1]], [safe_x[7], safe_y[2]], [safe_x[8], safe_y[2]], [safe_x[6], safe_y[3]]],
        [[safe_x[7], safe_y[1]], [safe_x[8], safe_y[2]], [safe_x[9], safe_y[2]], [safe_x[7], safe_y[3]]],
        [[safe_x[8], safe_y[1]], [safe_x[9], safe_y[2]], [safe_x[10], safe_y[2]], [safe_x[8], safe_y[3]]],
        [[safe_x[9], safe_y[1]], [safe_x[10], safe_y[2]], [safe_x[11], safe_y[2]], [safe_x[9], safe_y[3]]],
        
        # Robots 11-15 (working in third section)
        [[safe_x[10], safe_y[2]], [safe_x[11], safe_y[3]], [safe_x[12], safe_y[3]], [safe_x[10], safe_y[4]]],
        [[safe_x[11], safe_y[2]], [safe_x[12], safe_y[3]], [safe_x[13], safe_y[3]], [safe_x[11], safe_y[4]]],
        [[safe_x[12], safe_y[2]], [safe_x[13], safe_y[3]], [safe_x[14], safe_y[3]], [safe_x[12], safe_y[4]]],
        [[safe_x[13], safe_y[2]], [safe_x[14], safe_y[3]], [safe_x[15], safe_y[3]], [safe_x[13], safe_y[4]]],
        [[safe_x[14], safe_y[2]], [safe_x[15], safe_y[3]], [safe_x[0], safe_y[3]], [safe_x[14], safe_y[4]]],
        
        # Robots 16-20 (working in fourth section)
        [[safe_x[0], safe_y[3]], [safe_x[1], safe_y[4]], [safe_x[2], safe_y[4]], [safe_x[0], safe_y[5]]],
        [[safe_x[1], safe_y[3]], [safe_x[2], safe_y[4]], [safe_x[3], safe_y[4]], [safe_x[1], safe_y[5]]],
        [[safe_x[2], safe_y[3]], [safe_x[3], safe_y[4]], [safe_x[4], safe_y[4]], [safe_x[2], safe_y[5]]],
        [[safe_x[3], safe_y[3]], [safe_x[4], safe_y[4]], [safe_x[5], safe_y[4]], [safe_x[3], safe_y[5]]],
        [[safe_x[4], safe_y[3]], [safe_x[5], safe_y[4]], [safe_x[6], safe_y[4]], [safe_x[4], safe_y[5]]],
        
        # Robots 21-25 (working in outer corridors)
        [[safe_x[5], safe_y[4]], [safe_x[6], safe_y[5]], [safe_x[7], safe_y[5]], [safe_x[5], safe_y[0]]],
        [[safe_x[6], safe_y[4]], [safe_x[7], safe_y[5]], [safe_x[8], safe_y[5]], [safe_x[6], safe_y[0]]],
        [[safe_x[7], safe_y[4]], [safe_x[8], safe_y[5]], [safe_x[9], safe_y[5]], [safe_x[7], safe_y[0]]],
        [[safe_x[8], safe_y[4]], [safe_x[9], safe_y[5]], [safe_x[10], safe_y[5]], [safe_x[8], safe_y[0]]],
        [[safe_x[9], safe_y[4]], [safe_x[10], safe_y[5]], [safe_x[11], safe_y[5]], [safe_x[9], safe_y[0]]]
    ]
    
    # Return only the first n lists
    return task_locations_list[:n]

def verify_location_safety(task_locations_list):
    """
    Verify that no location coincides with pod locations
    """
    def is_pod_location(x, y):
        # Check against exact pod locations
        x_pods = set()
        for i in range(16):
            x_pods.add(10 + 5*i)  # First pod in pair
            x_pods.add(12 + 5*i)  # Second pod in pair
            
        y_pods = set()
        for k in range(4):
            for j in range(6):
                y_pods.add(15 + 2*j + 13*k)
                
        return (x in x_pods) and (y in y_pods)
    
    has_collision = False
    for i, robot_tasks in enumerate(task_locations_list):
        for j, (x, y) in enumerate(robot_tasks):
            if is_pod_location(x, y):
                print(f"Warning: Robot {i+1}, Location {j+1}: ({x},{y}) coincides with a pod location")
                has_collision = True
    
    if not has_collision:
        print("All locations verified safe - no collisions with pods")
            
# Create and verify the task locations
task_locations_list = create_task_locations_list(25)
verify_location_safety(task_locations_list)