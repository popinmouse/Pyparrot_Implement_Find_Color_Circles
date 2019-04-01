
import cv2

cv2.namedWindow( "The window", cv2.WINDOW_AUTOSIZE )

orig = cv2.imread("test_5.jpg")
cv2.imshow("The window", orig)
#cv2.waitKey(5000)
#orig = cv2.imwrite("test.jpg",orig)

hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
cv2.imshow("The window", hsv)
#cv2.waitKey(5000)

thresh = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))
cv2.imshow("The window", thresh)
#cv2.waitKey(5000)

_, outlines, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

print("Num contours = ", len(outlines))

cv2.drawContours(orig, outlines, -1, (0,255,0), 3)
cv2.imshow("The window", orig)
#cv2.waitKey(5000)

for line in outlines :
    if len(line) >= 5 :
        ellipse = cv2.fitEllipse(line)
        print("length = ", len(line), "Params = ", ellipse)
        cv2.ellipse(orig,ellipse,(255,0,0),2)
    else :
        print("length = ", len(line))

if orig is not None:
    if orig is not False:
        cv2.imshow("The window", orig)
        cv2.waitKey(10000)
    else :
        print("is false")
else :
    print("is none")


