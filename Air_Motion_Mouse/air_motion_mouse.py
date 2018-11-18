######################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.                     #
# SDK: https://developer.leapmotion.com/                                             #
# Creators: Eduard Lavrishchev, Tim Zhang, Jack Reeves, Aihui Yang                   #
# Libraries used: Leap (for Leap Motion), PyAutoGUI (for mouse and keyboard control) #
######################################################################################

import sys
import pyautogui
import Leap
from Leap import CircleGesture

# disabling unnessesary stuf
# f
pyautogui.FAILSAFE = False
Leap.image_processing_auto_flip = False
Leap.images_mode = 0
Leap.robust_mode_enabled = False
Leap.background_app_mode = 2
Leap.power_saving_adapter = False
Leap.power_saving_battery = False
Leap.low_resource_mode_enabled = False


class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        for hand in frame.hands:

            direction = hand.direction
            strength = hand.grab_strength

            if hand.is_left:
                if strength > 0.7:
                    pyautogui.click()
                    pyautogui.moveTo(1000, 35)
                    pyautogui.click()

                normal = hand.palm_normal

                if round(normal[0] * 90) in range(70, 90):
                    pyautogui.scroll(5)

                if -90 < round(normal[0] * 90) < -70:
                    pyautogui.scroll(-5)

                for gesture in frame.gestures():
                    if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                        circle = CircleGesture(gesture)

                        # Determine clock direction using the angle between the pointable and the circle normal
                        if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI / 2:
                            pyautogui.press('right')
                        else:
                            pyautogui.press('left'
                                            )

                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                        pyautogui.press('enter')
                if not (frame.hands.is_empty and frame.gestures().is_empty):
                    pass
            else:
                strength = hand.grab_strength
                if strength < 0.5:
                    pyautogui.moveTo(round(direction[0], 10) * 1400 + 720, 500 - round(direction[1] * 900, 10))
                else:
                    pass

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
