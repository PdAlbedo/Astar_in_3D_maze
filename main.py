"""
Xichen Liu

Test the algorithm
"""

import numpy as np
import Algorithm
import MazeMaker


if __name__ == '__main__':
    # Demo
    # Pre-set example
    # make a 4 * 4 * 4 maze
    # maze = MazeMaker.ThreeDMaze()

    # A*
    val = input("Enter the size of maze you want to make: ")
    maze = MazeMaker.ThreeDMaze(int(val))

    print("Number of obstacles: " + str(len(maze.obstacle_positions)))
    for a in maze.obstacle_positions:
        print("\nSize of obstacle " + str(maze.obstacle_positions.index(a) + 1) + ": " + str(int(np.sqrt(len(a)))) +
              " * " + str(int(np.sqrt(len(a)))))
        print("Points in the obstacle: ")
        for b in a:
            print(b.show_content())

    a_star = Algorithm.AStar(maze)
    path = a_star.run_algorithm()

    if len(path) != 0:
        re = "\n"
        for i in path:
            re += i.show_content()
            re += "\n"

        print(re)
