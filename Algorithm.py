"""
@author Xichen Liu

Implementation of A*, the start point is (0, 0, 0), end point is (size - 1, size - 1, size - 1) by default
"""

import sys
import time
import numpy as np
import Positions


class AStar:
    def __init__(self, maze):
        self.maze = maze
        self.open_set = []
        self.close_set = []

    """
    Calculate the distance in three ways
    
    :param dis  the mode chose to use
    :param dx   the difference of x between current position and another position
    :param dy   the difference of y between current position and another position
    :param dz   the difference of z between current position and another position
    :return distance
    """
    @staticmethod
    def calculate_dis(dis, dx, dy, dz, cost):
        if dis == "Manhattan":
            return dx + dy + dz
        elif dis == "diagonal":
            return dx + dy + dz + (cost - 2) * min(dx, dy, dz)
        elif dis == "Euclidean":
            return np.sqrt(dx * dx + dy * dy + dz * dz)
        return 0

    """
    Calculate the distance between current position and start point
    
    :param dis      the mode chose to use
    :param position the current position, the start position is (0, 0, 0) by default
    :return distance
    """
    def base_cost(self, position, distance = "diagonal"):
        cost = np.sqrt(3)
        dx = position.x
        dy = position.y
        dz = position.z

        return (self.calculate_dis("diagonal", dx, dy, dz, cost) + self.calculate_dis("Euclidean", dx, dy, dz, cost) +
                self.calculate_dis("Manhattan", dx, dy, dz, cost)) / 3

    """
    Calculate the distance between current position and end point

    :param dis      the mode chose to use
    :param position the current position, the end position is most far away from the start point by default
    :return distance
    """
    def heuristic_cost(self, position, distance = "diagonal"):
        cost = np.sqrt(3)
        dx = self.maze.size - 1 - position.x
        dy = self.maze.size - 1 - position.y
        dz = self.maze.size - 1 - position.z

        return (self.calculate_dis("diagonal", dx, dy, dz, cost) + self.calculate_dis("Euclidean", dx, dy, dz, cost) +
                self.calculate_dis("Manhattan", dx, dy, dz, cost)) / 3

    """
    Calculate the total cost which is the sum of base cost and heuristic cost
    
    :param position current position
    :return total cost
    """
    def total_cost(self, position):
        return self.base_cost(position) + self.heuristic_cost(position)

    """
    Check whether the position entered is in the range and not a obstacle
    
    :param x, y, z  information of the point to be checked
    :return True or False
    """
    def is_valid_point(self, x, y, z):
        if x < 0 or y < 0 or z < 0:
            return False
        if x >= self.maze.size or y >= self.maze.size or z >= self.maze.size:
            return False
        return not self.maze.is_obstacle(x, y, z)

    """
    Determine whether the point is in the given set
    
    :param position the current position
    :param pos_set  the set given
    :return True or False
    """
    @staticmethod
    def is_in_set(position, pos_set):
        for pos in pos_set:
            if position.x == pos.x and position.y == pos.y and position.z == pos.z:
                return True
        return False

    """
    Determine whether the point is in the open set
    
    :param position the current position
    :return True or False
    """
    def is_in_open_set(self, position):
        return self.is_in_set(position, self.open_set)

    """
    Determine whether the point is in the closed set
    
    :param position the current position
    :return True or False
    """
    def is_in_close_set(self, position):
        return self.is_in_set(position, self.close_set)

    """
    Whether the given position is the start point
    
    :param position the current position
    :return True or False
    """
    @staticmethod
    def is_start_point(position):
        return position.x == 0 and position.y == 0 and position.z == 0

    """
    Whether the given position is the start point
    
    :param position the current position
    :return True or False
    """
    def is_dest_point(self, position):
        return position.x == self.maze.size - 1 and position.y == self.maze.size - 1 \
               and position.z == self.maze.size - 1

    """
    Pick the position with the lowest cost
    
    :return the selected position
    """
    def select_from_open_set(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for position in self.open_set:
            cost = self.total_cost(position)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index

    """
    Add neighbors to the open set and record the parent, which is used to build the path
    
    :param x, y, z  coordinates of the position
    :parent         the previous position
    """
    def process_point(self, x, y, z, parent):
        if not self.is_valid_point(x, y, z):
            # Do nothing for invalid point
            return
        pos = Positions.Position(x, y, z)
        if self.is_in_close_set(pos):
            # Do nothing for visited point
            return
        # print("Process Point [", pos.x, ", ", pos.y, ", ", pos.z, "]", ", cost: ", pos.cost)
        if not self.is_in_open_set(pos):
            pos.parent = parent
            pos.cost = self.total_cost(pos)
            self.open_set.append(pos)

    """
    Build the path and track the run time
    
    :param pos  should be the end point
    :start_time the start time the algorithm
    """
    def build_path(self, pos, start_time):
        path = []
        while True:
            path.insert(0, pos)
            if self.is_start_point(pos):
                break
            else:
                pos = pos.parent
        end_time = time.time()
        print('===== Algorithm finish in', int(end_time - start_time), ' seconds')
        return path

    """
    Actual run the algorithm
    
    :return the path from the start to the end if there exists a path; otherwise, return an empty list
    """
    def run_algorithm(self):
        start_time = time.time()

        start_point = Positions.Position(0, 0, 0)
        start_point.cost = 0
        self.open_set.append(start_point)

        while True:
            index = self.select_from_open_set()
            # if no more points in the open list, return nothing
            if index < 0:
                print('No path found, algorithm failed.')
                return []
            position = self.open_set[index]

            if self.is_dest_point(position):
                return self.build_path(position, start_time)

            del self.open_set[index]
            self.close_set.append(position)

            # Process all neighbors
            x = position.x
            y = position.y
            z = position.z
            # 28 directions
            self.process_point(x - 1, y + 1, z, position)
            self.process_point(x - 1, y, z, position)
            self.process_point(x - 1, y - 1, z, position)
            self.process_point(x, y + 1, z, position)
            self.process_point(x, y - 1, z, position)
            self.process_point(x + 1, y + 1, z, position)
            self.process_point(x + 1, y, z, position)
            self.process_point(x + 1, y - 1, z, position)

            self.process_point(x - 1, y + 1, z + 1, position)
            self.process_point(x - 1, y, z + 1, position)
            self.process_point(x - 1, y - 1, z + 1, position)
            self.process_point(x, y + 1, z + 1, position)
            self.process_point(x, y, z + 1, position)
            self.process_point(x, y - 1, z + 1, position)
            self.process_point(x + 1, y + 1, z + 1, position)
            self.process_point(x + 1, y, z + 1, position)
            self.process_point(x + 1, y - 1, z + 1, position)

            self.process_point(x - 1, y + 1, z - 1, position)
            self.process_point(x - 1, y, z - 1, position)
            self.process_point(x - 1, y - 1, z - 1, position)
            self.process_point(x, y + 1, z - 1, position)
            self.process_point(x, y, z - 1, position)
            self.process_point(x, y - 1, z - 1, position)
            self.process_point(x + 1, y + 1, z - 1, position)
            self.process_point(x + 1, y, z - 1, position)
            self.process_point(x + 1, y - 1, z - 1, position)
