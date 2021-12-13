"""
@author Xichen Liu

Class that stores the positions inside of the maze
"""

import sys


class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        # the total cost is initialized to the maximum value
        self.cost = sys.maxsize

    """
    Show the info of a position
    
    :return the string that contains the x, y, and z
    """
    def show_content(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"
