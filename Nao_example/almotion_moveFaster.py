#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Walk - Small example to make Nao walk"""

import qi
import argparse
import sys
import time


def main(session):
    """
    Walk: Small example to make Nao walk Faster (Step of 6cm).
    This example is only compatible with NAO.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    # Initialize the walk process.
    # Check the robot pose and take a right posture.
    # This is blocking called.
    motion_service.moveInit()

    # TARGET VELOCITY
    X         = 1.0
    Y         = 0.0
    Theta     = 0.0
    Frequency = 1.0

    # Default walk (MaxStepX = 0.04 m)
    try:
        motion_service.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()

    time.sleep(3.0)
    print "walk Speed X :",motion_service.getRobotVelocity()[0]," m/s"

    # Speed walk  (MaxStepX = 0.06 m)
    # Could be faster: see walk documentation
    try:
        motion_service.moveToward(X, Y, Theta, [["Frequency", Frequency],
                                             ["MaxStepX", 0.06]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()

    time.sleep(4.0)
    print "walk Speed X :",motion_service.getRobotVelocity()[0]," m/s"

    # stop walk on the next double support
    motion_service.stopMove()

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
