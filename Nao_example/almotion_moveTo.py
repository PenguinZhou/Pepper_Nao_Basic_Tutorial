#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Move To - Small example to make Nao Move To an Objective"""

import qi
import argparse
import sys
import math
import almath


def main(session):
    """
    Move To: Small example to make Nao Move To an Objective.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    #####################
    ## Enable arms control by move algorithm
    #####################
    motion_service.setMoveArmsEnabled(True, True)
    #~ motion_service.setMoveArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
    motion_service.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    #####################
    ## get robot position before move
    #####################
    initRobotPosition = almath.Pose2D(motion_service.getRobotPosition(False))

    X = 0.3
    Y = 0.1
    Theta = math.pi/2.0
    motion_service.moveTo(X, Y, Theta, _async=True)
    # wait is useful because with _async moveTo is not blocking function
    motion_service.waitUntilMoveIsFinished()

    #####################
    ## get robot position after move
    #####################
    endRobotPosition = almath.Pose2D(motion_service.getRobotPosition(False))

    #####################
    ## compute and print the robot motion
    #####################
    robotMove = almath.pose2DInverse(initRobotPosition)*endRobotPosition
    # return an angle between ]-PI, PI]
    robotMove.theta = almath.modulo2PI(robotMove.theta)
    print "Robot Move:", robotMove

    # Go to rest position
    motion_service.rest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
