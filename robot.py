# -----------------------------------------------------------------------------
# Name:         robot
# Purpose:      class definitions for robots and underwater robots
#
# Author:       David Gudeman
# Date:         June 29, 2015
# -----------------------------------------------------------------------------

"""
Module to describe and control Robot and UnderwaterRobots objects in a maze.
"""
import tkinter


class Robot(object):

    """
    Represents a robot that can move in two dimensions

    Arguments:
    name (string): name of the robot
    color (string): color of the robot
    row (int, optional): start row, defaults to 0
    column (int, optional): start column, defaults to 0

    Attributes:
    name (string): name of the robot
    color (string): color of the robot
    row (int): robot's row
    column (int): robot's column
    battery (int): how many squares the robot can move without a recharge
    """

    # class variable used by the show method
    unit_size = 60

    # Class variable describing the maze
    # False represents an obstacle, True represents open space
    maze = [[True, True, False, True, True, True, False, True, True, True],
            [True, True, False, True, True, True, False, True, True, True],
            [True, False, True, True, True, True, False, True, True, True],
            [True, True, True, True, True, True, True, True, False, True],
            [True, True, True, True, True, True, True, True, False, True],
            [True, True, True, True, True, True, True, True, True, True],
            [True, False, False, False, False, True, True, True, True, True],
            [True, True, False, True, True, True, True, True, False, True],
            [True, False, True, True, True, True, True, True, False, True],
            [True, True, True, True, True, True, True, True, False, True]]

    # class variable describing the width and heighth of maze coordinates
    maze_size = len(maze)

    # class variable to represent a full battery
    # A robot with a fully charged battery can take up to 20 steps
    full = 20

    def __init__(self, name, color, row=0, column=0):
        self.name = name
        self.color = color
        self.row = row
        self.column = column
        self.recharge()

    def __str__(self):
        """
        string representation of the robot object

        returns: a string describing the robot name and color and activity
        """
        return self.name + ' is a ' + self.color + ' robot lost in the maze.'

    def __gt__(self, other):
        """
        rich comparator of the current battery values of two robots
        :param other (string): takes argument of the other robots identifier
        :returns (object): the robot with largest current battery value
        """
        result = (self.battery > other.battery)
        return result

    def recharge(self):
        """
        sets the robot.battery value to value of full class variable

        returns (object): the robot
        """
        self.battery = 20
        return self

    def one_step_forward(self):
        """
        evaluates the feasibility of taking a step into a larger row
        will not move robot if the robots battery 0
        will move only if the next coordinate is true, obstacles are false
        """
        next_row = self.row + 1 # anticipated row

        # check maze length to make sure does not go off the maze board
        # for some reason this throughs an error but behaves to specs in all
        # other aspects.

        if next_row >= 0 & next_row < Robot.maze_size:
            if Robot.maze[next_row][self.column]:   # test for availability
                if self.battery > 0:
                    self.row = next_row                 # if square = True move
                    self.battery -= 1
        return self

    def one_step_back(self):
        """"
        evaluates the feasibility of taking a step into a smaller row
        will not move robot if the robots battery 0
        will move only if the next coordinate is true, obstacles are false
        """
        next_row = self.row - 1                 # anticipated row
        if next_row >= 0 & next_row < Robot.maze_size: # edge test
            if Robot.maze[next_row][self.column]:   # test for obstacle
                if self.battery > 0:            # checks battery
                    self.row = next_row         # moves robot
                    self.battery -= 1           # reduces battery by 1
        return self


    def one_step_right(self):
        """
        evaluates the feasibility of taking a step into a larger column
        will not move robot if the robots battery 0
        will move only if the next coordinate is true, obstacles are false
        """
        next_column = self.column + 1            # anticipated column
        if next_column >= 0 & next_column < Robot.maze_size: # edge test
            if Robot.maze[self.row][next_column]:   # test for obstacle
                if self.battery > 0:             # checks the battery
                    self.column = next_column    # makes move
                    self.battery -= 1            # reduces battery by 1
        return self

    def one_step_left(self):
        """
        evaluates the feasibility of taking a step into a smaller column
        will not move robot if the robots battery 0
        will move only if the next coordinate is true, obstacles are false
        """
        next_column = self.column - 1           # anticipated column
        if next_column >= 0 & next_column < Robot.maze_size: # edge test
            if Robot.maze[self.row][next_column]:  # test for obstacle
                if self.battery > 0:            # checks battery
                    self.column = next_column   # moves robot
                    self.battery -= 1           # reduces battery by 1
        return self

    def forward(self, steps):
        """
        The argument supplies how many steps forward to take

        :param: steps(string): number of steps to take
        :return: the robot object
        """
        i = 1
        while i <= steps: # steps arg defines No. one_step forward fxn calls
            self.one_step_forward()
            i += 1        # increments index with each call

    def backward(self, steps):
        """
        The argument supplies how many steps backward to take

        :param: steps(string): number of steps to take
        :return: the robot object
        """
        i = 1
        while i <= steps: # step param defines No. one_step_backward fxn calls
            self.one_step_back()
            i += 1        # increment index with each call

    def right(self, steps):
        """
        The argument supplies how many steps right to take

        :param: steps(string): number of steps to take
        :return: the robot object
        """
        i = 1
        while i <= steps: # step param defines No. of one_step_right fxn calls
            self.one_step_right()
            i += 1        # increment index with each call

    def left(self, steps):
        """
        The argument supplies how many steps left to take

        :param: steps(string): number of steps to take
        :return: the robot object
        """
        i = 1
        while i <= steps: # step param defines No. of one_step_left fxn calls
            self.one_step_left()
            i += 1        # increment index with each call

    # the method below has been written for you
    # you can use it when testing your class
    def show(self):
        """
        Draw a graphical representation of the robot in the maze.

        The robot's position and color are shown.
        The color is assumed to be one of the colors recognized by tkinter
        (https://www.tcl.tk/man/tcl8.4/TkCmd/colors.htm)
        If the robot's battery is empty, the robot is shown in a
        horizontal position. Otherwise the robot is shown in an upright
        position.
        The obstacles in the maze are shown in red.

        Parameter: None
        Return: None
        """
        root = tkinter.Tk()
        root.title (self.name + ' in the Maze')
        canvas= tkinter.Canvas(root, background = 'light green',
                               width = self.unit_size * self.maze_size,
                               height = self.unit_size * self.maze_size)
        canvas.grid()

        # draw a representation of the robot in the maze
        if self.battery:
            upper_x = self.column * self.unit_size + self.unit_size / 4
            upper_y = self.row * self.unit_size
            lower_x = upper_x + self.unit_size / 2
            lower_y = upper_y + self.unit_size
            eye_x = lower_x - 3 * self.unit_size /  20
            eye_y = upper_y + self.unit_size / 10

        else: # the robot ran out of battery
            upper_x = self.column * self.unit_size
            upper_y = self.row * self.unit_size + self.unit_size / 2
            lower_x = upper_x + self.unit_size
            lower_y = upper_y + self.unit_size / 2
            eye_x = lower_x - 9 * self.unit_size / 10
            eye_y = lower_y -  3 * self.unit_size / 20

        rectangle = canvas.create_rectangle(upper_x,
                                            upper_y,
                                            lower_x,
                                            lower_y,
                                            fill = self.color)
        # draw the robot's eyes
        canvas.create_oval(upper_x + self.unit_size / 10,
                           upper_y + self.unit_size / 10,
                           upper_x + 3 * self.unit_size / 20,
                           upper_y + 3 * self.unit_size / 20,
                           fill = 'black')
        canvas.create_oval(eye_x,
                           eye_y,
                           eye_x + self.unit_size / 20,
                           eye_y + self.unit_size / 20,
                           fill = 'black')
        # draw the obstacles in the maze
        for row in range(self.maze_size):
            for col in range(self.maze_size):
                if not self.maze[row][col]:
                    canvas.create_rectangle(col * self.unit_size,
                                            row * self.unit_size,
                                            (col + 1) * self.unit_size,
                                            (row + 1) * self.unit_size,
                                            fill='red')
        for row in range(self.maze_size):
            canvas.create_line(0,
                               row * self.unit_size,
                               self.maze_size * self.unit_size,
                               row * self.unit_size)
        for col in range(self.maze_size):
            canvas.create_line(col * self.unit_size,
                               0,
                               col * self.unit_size,
                               self.maze_size * self.unit_size )
        root.mainloop()

class UnderwaterRobot(Robot):
    """
    Represents a robot that can move in two dimensions and
        dive underwater

    Arguments:
    name (string): name of the robot
    color (string): color of the robot
    depth (int, oprional): depth of start, defaults to 0
    row (int, optional): start row, defaults to 0
    column (int, optional): start column, defaults to 0

    Attributes:
    name (string): name of the robot
    color (string): color of the robot
    depth (int): represents the depth in squares of the robot
    row (int): robot's row
    column (int): robot's column
    battery (int): how many squares the robot can move without a recharge
    """
    def __init__(self, name, color, depth=0, column=0, row=0):
        self.depth = depth
        Robot.__init__(self, name, color, column, row)

    def __str__(self):
        """
        returns a string describing the robot

        :return (string): description includes: name, color, ability to dive
        """
        return self.name + ' is a ' + self.color + ' robot diving underwater.'

    def dive(self, squares):
        """
        moves the robot up and down in water column.
        :param squares (int): number of squares to move. positive numbers
             descend and negative numbers rise
        :return: robot object
        """
        self.depth = self.depth + squares




