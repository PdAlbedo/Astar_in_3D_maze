"""
Xichen Liu

Test the algorithm
"""
import Algorithm
import MazeMaker

if __name__ == '__main__':
    # Pre-set example
    # make a 6 * 6 * 6 maze
    maze = MazeMaker.ThreeDMaze(6)

    for a in maze.obstacle_positions:
        for b in a:
            print(b.show_content())

    print(len(maze.obstacle_positions))
    print(len(maze.obstacle_positions[0]))

    a_star = Algorithm.AStar(maze)
    path = a_star.run_algorithm()

    if len(path) != 0:
        re = "\n"
        for i in path:
            re += i.show_content()
            re += "\n"

        print(re)
    # ------------------------------------------------
