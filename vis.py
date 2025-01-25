import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_polygon_from_constraints(ax, A, b, color):
    """Draw a polygon defined by Ax <= b using simple rectangles"""
    # Convert constraints to simpler bounds
    xmin = ymin = float('inf')
    xmax = ymax = float('-inf')
    
    # Extract bounds from constraints
    for i in range(len(b)):
        a = A[i]
        if abs(a[0]) > 1e-10:  # x constraint
            x = b[i] / a[0]
            if a[0] > 0:
                xmax = min(xmax if xmax != float('-inf') else x, x)
            else:
                xmin = max(xmin if xmin != float('inf') else x, -x)
        if abs(a[1]) > 1e-10:  # y constraint
            y = b[i] / a[1]
            if a[1] > 0:
                ymax = min(ymax if ymax != float('-inf') else y, y)
            else:
                ymin = max(ymin if ymin != float('inf') else y, -y)
    
    # Create rectangle patch
    width = xmax - xmin
    height = ymax - ymin
    rect = patches.Rectangle((xmin, ymin), width, height, 
                           facecolor=color, alpha=0.3, edgecolor=color)
    ax.add_patch(rect)
    
    return [xmin, xmax, ymin, ymax]

def vis(test, limits=None, equal_aspect=True):
    _, plots, PWLs = test()
    
    plt.rcParams["figure.figsize"] = [6.4, 6.4]
    plt.rcParams['axes.titlesize'] = 20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis('on')  # Changed to 'on' to better see the space
    
    # Track bounds for auto-scaling
    all_bounds = []
    
    # Draw all polygons
    for plot in plots:
        for A, b in plot[0]:
            bounds = draw_polygon_from_constraints(ax, A, b, plot[1])
            all_bounds.append(bounds)
    
    # Set limits
    if limits is not None:
        plt.xlim(limits[0])
        plt.ylim(limits[1])
    else:
        if all_bounds:
            xmin = min(bound[0] for bound in all_bounds)
            xmax = max(bound[1] for bound in all_bounds)
            ymin = min(bound[2] for bound in all_bounds)
            ymax = max(bound[3] for bound in all_bounds)
            margin = 0.1 * max(xmax - xmin, ymax - ymin)
            plt.xlim([xmin - margin, xmax + margin])
            plt.ylim([ymin - margin, ymax + margin])
        else:
            plt.xlim([-2, 13])
            plt.ylim([-2, 12])
    
    if equal_aspect:
        plt.gca().set_aspect('equal', adjustable='box')
    
    if PWLs is None or PWLs[0] is None:
        plt.show()
        return
    
    # Draw paths
    if len(PWLs) <= 4:
        colors = ['k', np.array([153,0,71])/255, np.array([6,0,153])/255, np.array([0, 150, 0])/255]
    else:
        cmap = plt.get_cmap('tab10')
        colors = [cmap(i) for i in np.linspace(0, 0.85, len(PWLs))]
    
    for i in range(len(PWLs)):
        PWL = PWLs[i]
        # Draw path
        ax.plot([P[0][0] for P in PWL], [P[0][1] for P in PWL], '-', 
                color=colors[i], linewidth=2, label=f'Robot {i+1}')
        # Draw start point
        ax.plot(PWL[0][0][0], PWL[0][0][1], 'o', color=colors[i], 
                markersize=8, label=f'Start {i+1}')
        # Draw end point
        ax.plot(PWL[-1][0][0], PWL[-1][0][1], '*', color=colors[i], 
                markersize=10, label=f'End {i+1}')
    
    ax.legend()
    ax.grid(True)
    plt.show()