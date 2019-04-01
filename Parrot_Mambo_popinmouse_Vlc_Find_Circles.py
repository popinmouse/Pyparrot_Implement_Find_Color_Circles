"""
Applying the demomMamboVisionGUI to design a program to allow the drone find and go through the color rings.

Author: CHT
"""
from pyparrot.Minidrone import Mambo
from pyparrot.DroneVisionGUI import DroneVisionGUI
import cv2
import time

low_red  = (156, 128, 128)
high_red = (180, 255, 255)

low_yellow = (21, 128, 30)
high_yellow = (34, 200, 200)

low_blue = (100, 128, 128)
high_blue = (124, 255, 255)

# set this to true if you want to fly for the demo
testFlying = True

class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        # print("in save pictures on image %d " % self.index)

        img = self.vision.get_latest_valid_picture()

        if (img is not None):
            filename = "test_image_%06d.png" % self.index
            # uncomment this if you want to write out images every time you get a new one
            cv2.imwrite(filename, img)
            self.index += 1
            print(self.index)
            #if self.index == 200:
            #   self.index = 0
            #   print("renew_picture")

    def auto_filter(self, line=0, ellip_1=(0.0, 0.0), ellip_2=(0.0, 0.0), ellip_list=None):
        filter_ellip_list = []
        for i in range(len(ellip_list)):
            if ellip_list[i][0] > line:
                if ellip_list[i][1][0][0] < ellip_1[0]:
                    if ellip_list[i][1][0][1] < ellip_1[1]:
                        if ellip_list[i][1][1][0] < ellip_2[0]:
                            if ellip_list[i][1][1][1] < ellip_2[1]:
                                filter_ellip_list.append(ellip_list[i])
        return filter_ellip_list

    def detect_function(self, color="red"):
        if color is "red":
            low_color_set = low_red
            high_color_set = high_red
        elif color is "yellow":
            low_color_set = low_yellow
            high_color_set = high_red
        elif color is "blue":
            low_color_set = low_blue
            high_color_set = high_blue
        print("detect_{}_start".format(color))
        detect = False
        count = 0
        while detect is False:
            count += 1
            orig = self.vision.get_latest_valid_picture()
            cv2.imshow("The window", orig)
            hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
            cv2.imshow("The window", hsv)
            thresh = cv2.inRange(hsv, low_color_set, high_color_set)
            cv2.imshow("The window", thresh)
            _, outlines, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            print("Num contours = ", len(outlines))
            cv2.drawContours(orig, outlines, -1, (0, 255, 0), 3)
            cv2.imshow("The window", orig)

            ellipse_list = []
            for line in outlines:
                if len(line) >= 5:
                    ellipse = cv2.fitEllipse(line)
                    print("length = ", len(line), "Params = ", ellipse)
                    cv2.ellipse(orig, ellipse, (255, 0, 0), 2)
                    line_list = [len(line), ellipse]
                    ellipse_list.append(line_list)
                else:
                    pass
            if orig is not None:
                if orig is not False:
                    cv2.imshow("The window", orig)
                    cv2.waitKey(100)
                else:
                    pass
            else:
                pass

            ellipse_list.sort()
            print(ellipse_list[-1])
            if len(ellipse_list) == 0:
                print("turning degree of 90")
                mambo.turn_degrees(90)
            else:
                detect = True
                print("detected_{}".format(color))
        return detect

    def target_function(self, color="red"):
        if color is "red":
            low_color_set = low_red
            high_color_set = high_red
        elif color is "yellow":
            low_color_set = low_yellow
            high_color_set = high_red
        elif color is "blue":
            low_color_set = low_blue
            high_color_set = high_blue
        print("target_{}_start".format(color))
        target = False
        count = 0
        while target is False:
            count += 1
            # orig = cv2.imread("test_image_000000.png")
            orig = self.vision.get_latest_valid_picture()
            cv2.imshow("The window", orig)
            # cv2.waitKey(5000)
            # orig = cv2.imwrite("test.jpg",orig)
            hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
            cv2.imshow("The window", hsv)
            # cv2.waitKey(5000)
            thresh = cv2.inRange(hsv, low_color_set, high_color_set)
            cv2.imshow("The window", thresh)
            # cv2.waitKey(5000)
            _, outlines, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            print("Num contours = ", len(outlines))
            cv2.drawContours(orig, outlines, -1, (0, 255, 0), 3)
            cv2.imshow("The window", orig)
            #cv2.waitKey(5000)
            ellipse_list = []
            for line in outlines:
                if len(line) >= 5:
                    ellipse = cv2.fitEllipse(line)
                    print("length = ", len(line), "Params = ", ellipse)
                    cv2.ellipse(orig, ellipse, (255, 0, 0), 2)
                    line_list = [len(line), ellipse]
                    ellipse_list.append(line_list)
                else:
                    pass
            if orig is not None:
                if orig is not False:
                    cv2.imshow("The window", orig)
                    cv2.waitKey(100)
                else:
                    pass
            else:
                pass
            print("len of ellipse:", len(ellipse_list))
            ellipse_list.sort()
            print(ellipse_list[-1])
            max = int(-1)
            maxvalue = ellipse_list[-1][0]
            print("max len:", maxvalue, "ellipse:", ellipse_list[max])
            if maxvalue >= 20:
                x = 0.0
                y = 0.0
                x, y = ellipse_list[max][1][0]
                if x > 310.0 and x < 330.0 and y > 230.0 and y < 250.0:
                    # filter if the ellipse is right in the center
                    a = 0.0
                    b = 0.0
                    a, b = ellipse_list[max][1][1]
                    if a > 50.0 and b > 50.0 and abs(a-b) < 10.0:
                        print("targeted_{}".format(color))
                        print("target_{}_fly_close".format(color))
                        mambo.fly_direct(roll=0, pitch=5, yaw=0, vertical_movement=0, duration=1)
                        if abs(a - b) < 5.0:
                            print("target_{}_fly_through".format(color))
                            mambo.fly_direct(roll=0, pitch=40, yaw=0, vertical_movement=0, duration=4)
                            target = True
                    elif abs(a - b) > 10.0:
                        # y axis it too long . drone flies round along the ring with clockwise
                        print("y axis is too long")
                        mambo.fly_direct(roll=0, pitch=-5, yaw=0, vertical_movement=0, duration=1)
                if x > 330.0:  # target is too right
                    print("target is too right")
                    mambo.fly_direct(roll=5, pitch=0, yaw=0, vertical_movement=0, duration=1)
                    pass
                elif x < 310.0:  # target is too left
                    print("target is too left")
                    mambo.fly_direct(roll=-5, pitch=0, yaw=0, vertical_movement=0, duration=1)
                    pass
                if y > 250.0:  # target is too high
                    print("target is too high")
                    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-5, duration=1)
                    pass
                elif y < 230.0:  # target is too low
                    print("target is too low")
                    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=5, duration=1)
                    pass
                print("regular forward")
                mambo.fly_direct(roll=0, pitch=1, yaw=0, vertical_movement=0, duration=0.2)
            print("count:", count)
            if count > 1000:
                target = True
                print("mission_target_{}_count_out".format(color))
        return target

def demo_mambo_user_vision_function(mamboVision, args):
    """
    Demo the user code to run with the run button for a mambo

    :param args:
    :return:
    """
    mambo = args[0]
    cv2.namedWindow("The window", cv2.WINDOW_AUTOSIZE)

    if (testFlying):
        print("taking off!")
        mambo.safe_takeoff(5)

        if (mambo.sensors.flying_state != "emergency"):
            print("flying state is %s" % mambo.sensors.flying_state)

            detect_color = False
            target_color = False
            while detect_color is False:
                detect_color = mamboVision.set_user_callback_function(userVision.detect_function(color='red'), user_callback_args=None)
                time.sleep(1)
            while target_color is False:
                target_color = mamboVision.set_user_callback_function(userVision.target_function(color='red'), user_callback_args=None)
                time.sleep(1)
                if target_color is True:
                    # done doing vision demo
                    print("Ending the sleep and vision")
                    mamboVision.close_video()
                    mambo.smart_sleep(5)
                    print("disconnecting")
                    mambo.disconnect()

        print("landing")
        print("flying state is %s" % mambo.sensors.flying_state)
        mambo.safe_land(5)
    else:
        print("Sleeping for 15 seconds - move the mambo around")
        mambo.smart_sleep(15)

if __name__ == "__main__":
    # you will need to change this to the address of YOUR mambo
    mamboAddr = "e0:14:d0:63:3d:d0"

    # make my mambo object
    # remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
    mambo = Mambo(mamboAddr, use_wifi=True)
    print("trying to connect to mambo now")
    success = mambo.connect(num_retries=3)
    print("connected: %s" % success)

    if (success):
        # get the state information
        print("sleeping")
        mambo.smart_sleep(1)
        mambo.ask_for_state_update()
        mambo.smart_sleep(1)

        print("Preparing to open vision")
        mamboVision = DroneVisionGUI(mambo, is_bebop=False, buffer_size=200, fps=1,
                                     user_code_to_run=demo_mambo_user_vision_function, user_args=(mambo, ))
        userVision = UserVision(mamboVision)
        #mamboVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
        mamboVision.open_video()