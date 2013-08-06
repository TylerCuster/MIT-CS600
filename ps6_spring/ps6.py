# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab
import numpy

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        assert width > 0, height > 0
        self.width = width
        self.height = height
        self.cleanDict = {}
        for x in range(width+1):
            for y in range(height+1):
                self.cleanDict[(x,y)] = False
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        pos_round = (math.floor(pos.x), math.floor(pos.y))
        self.cleanDict[pos_round] = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.cleanDict[m,n]
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        count = 0
        for keys in self.cleanDict.keys():
            if self.cleanDict[keys] == True:
                count += 1
        return count

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x_rand = random.random()*self.width
        y_rand = random.random()*self.height
        return Position(x_rand, y_rand)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (pos.x,pos.y) in self.cleanDict.keys()

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = self.room.getRandomPosition()
        self.direction = random.random()*360
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotPosition(self.position.getNewPosition(self.direction, self.speed))
        self.room.cleanTileAtPosition(self.position)

# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        try_position = self.position.getNewPosition(self.direction, self.speed)
        if try_position.x < 0:
            self.direction = random.random()*360
        elif try_position.x > self.room.width:
            self.direction = random.random()*360
        elif try_position.y < 0:
            self.direction = random.random()*360
        elif try_position.y > self.room.height:
            self.direction = random.random()*360
        else:
            self.position = try_position
            self.room.cleanTileAtPosition(self.position)
            return self.position
        self.updatePositionAndClean()

# === Problem 3

def runSimulation(NUM_ROBOTS, speed, width, height, MIN_COVERAGE, NUM_TRIALS,
                  ROBOT_TYPE):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    countDict = {}
    squareCount = math.floor(width*height*MIN_COVERAGE)
    for t in range(NUM_TRIALS):
##        anim = ps6_visualize.RobotVisualization(NUM_ROBOTS, width, height)
        room = RectangularRoom(width, height)
        robotDict = {}
        for i in range(NUM_ROBOTS):
            robotDict[i] = ROBOT_TYPE(room, speed)
        robotList = []
        for key in robotDict.keys():
            robotList.append(robotDict[key])
        steps = 0
        L = True
        while L == True:
            for key in robotDict.keys():
                robotDict[key].updatePositionAndClean()
##                anim.update(room, robotList)
            steps += 1
            if room.getNumCleanedTiles() >= squareCount:
                countDict[t] = steps
                L = False
##        anim.done()
    meanSum = 0
    count = 0
    for keys in countDict.keys():
        meanSum = meanSum + countDict[keys]
        count += 1
    return meanSum/count
            
# Dict for recording number of steps for each trial
# Square count: figure out number of squares required for MIN_COVERAGE of room
# For each trial:
#   Initialize room
#   Initialize robots
#   Make robots begin moving around room by calling function
#   Check at each new step to see if square count is reached
#       access room.cleanDict to count keys that are True
#       If reached, record number of steps in Dict
#           end loop, onto next trial
#       If not reached, call move 1-step around room function
# Return mean of number of steps in Dict

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    robot_list = [1,2,3,4,5,6,7,8,9,10]
    sim_list = []
    for i in robot_list:
        sim_list.append(runSimulation(i, 1.0, 20, 20, 0.80, 10, StandardRobot))
    print "sim list", sim_list
    pylab.title("Dependence of cleaning time on number of robots")
    pylab.xlabel("Number of Robots")
    pylab.ylabel("Mean of cleaning time under 10 trials")
    pylab.plot(robot_list, sim_list)
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    sim_list = []
    sim_list.append(runSimulation(2, 1.0, 20, 20, 0.80, 10, StandardRobot))
    sim_list.append(runSimulation(2, 1.0, 25, 16, 0.80, 10, StandardRobot))
    sim_list.append(runSimulation(2, 1.0, 40, 10, 0.80, 10, StandardRobot))
    sim_list.append(runSimulation(2, 1.0, 50, 8, 0.80, 10, StandardRobot))
    sim_list.append(runSimulation(2, 1.0, 80, 5, 0.80, 10, StandardRobot))
    sim_list.append(runSimulation(2, 1.0, 100, 4, 0.80, 10, StandardRobot))
##    area_list = [20x20, 25x16, 40x10, 50x8, 80x5, 100x4]
    area_list = [1,2,3,4,5,6]
    pylab.plot(area_list, sim_list)
    pylab.title("Dependence of cleaning time on room shape")
    pylab.xlabel("Width x Height")
    pylab.ylabel("Mean of cleaning time under 10 trials")
    pylab.show()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        try_position = self.position.getNewPosition(self.direction, self.speed)
        self.direction = random.random()*360
        if try_position.x < 0:
            pass
        elif try_position.x > self.room.width:
            pass
        elif try_position.y < 0:
            pass
        elif try_position.y > self.room.height:
            pass
        else:
            self.position = try_position
            self.room.cleanTileAtPosition(self.position)
            return self.position
        self.updatePositionAndClean()

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    N = 10
    ind = numpy.arange(N)
    width = 0.35
    S_means = []
    for i in range(1,N+1):
        S_means.append(runSimulation(i, 1.0, 20, 20, 0.80, 1, StandardRobot))
    print S_means
    R_means = []
    for i in range(1,N+1):
        R_means.append(runSimulation(i, 1.0, 20, 20, 0.80, 1, RandomWalkRobot))
    print R_means
    pylab.subplot(111)
    rects1 = pylab.bar(ind+width, R_means, width, color='r')
    rects2 = pylab.bar(ind+width, S_means, width, color='y')
    pylab.xlabel("Number of Robots")
    pylab.ylabel("Mean of 10 trials")
    pylab.xticks(ind+width, ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"))
    pylab.legend( (rects1[0], rects2[0]), ("RandomWalkRobot", "StandardRobot") )
    pylab.show()
