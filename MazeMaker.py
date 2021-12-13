"""
@author Xichen Liu

The algorithm that generate a 3D maze
"""
import numpy as np
import Positions


class ThreeDMaze:
    def __init__(self, size = 15):
        self.size = size  # size of maze (length of width, length, and depth)
        self.number_of_obstacles = size // 5  # number of obstacles in the maze
        self.obstacle_positions = []  # each element in the list is a obstacle which consist of couple positions
        self.generate_obstacle()

        # Demo
        self.demo_with555()
        self.demo_with666()

    """
    Two pre set maze to test whether the algorithm works
    """
    def demo_with555(self):
        self.obstacle_positions.append(Positions.Position())

    def demo_with666(self):
        self.obstacle_positions.append(Positions.Position())

    """
    Generate a square obstacle 
    
    
    :param the size of the obstacle
    :return a list of positions that compose the obstacle
    """
    def obstacle(self, x_size, y_size, z_size):
        temp = []
        x = np.random.randint(0, self.size - x_size)
        y = np.random.randint(0, self.size - y_size)
        z = np.random.randint(0, self.size - z_size)
        for i in range(x_size):
            for j in range(y_size):
                for k in range(z_size):
                    temp.append(Positions.Position(x + i, y + j, z + k))
        return temp

    """
    Generate all obstacles in the maze
    """
    def generate_obstacle(self):

        for i in range(self.number_of_obstacles):
            flag = np.random.randint(1, 3)

            if flag == 1:
                # generate obstacles on xy plane
                obstacle_size = np.random.randint(3, 5)
                # self.obstacle(obstacle_size, obstacle_size, 0)
                self.obstacle_positions.append(self.obstacle(obstacle_size, obstacle_size, 1))

            elif flag == 2:
                # generate obstacles on xz plane
                obstacle_size = np.random.randint(3, 5)
                # self.obstacle(obstacle_size, 0, obstacle_size)
                self.obstacle_positions.append(self.obstacle(obstacle_size, 1, obstacle_size))

            elif flag == 3:
                # generate obstacles on yz plane
                obstacle_size = np.random.randint(3, 5)
                # self.obstacle(0, obstacle_size, obstacle_size)
                self.obstacle_positions.append(self.obstacle(1, obstacle_size, obstacle_size))

    """
    Determine whether the given position is a obstacle
    
    :param x:   x position
    :param y:   y position
    :param z:   z position
    :return True or False
    """
    def is_obstacle(self, x, y, z):
        for i in self.obstacle_positions:
            for j in i:
                if x == j.x and y == j.y and z == j.z:
                    return True
        return False
