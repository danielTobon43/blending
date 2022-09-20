#!/usr/bin/env python3.7
import numpy as np

## NOTE:
## YOU NEED TO MAKE SURE BOTH IMAGES HAVE SAME SIZE (HEIGHT*WIDTH)

# ----------------------------------------------------- System
# check if platform is windows or linux:
# import sys
# from sys import platform
# if platform == "linux" or platform == "linux2":
# 	sys.path.append("/opt/opencv-4.1.2/build/lib/python3")
# elif platform == "win32":
#     print("")
#     sys.path.append("C:/Users/xxx/Desktop/opencv/opencv-4.1.2/build/lib/python3")
# else:
# 	print("only for linux or windows")
# 	sys.exit(-1)

# ----------------------------------------------------- Opencv
import cv2


if __name__ == "__main__":

    print("")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("***   MAIN PROGRAM        ***")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    img1 = cv2.imread("images/apple.jpg")
    img2 = cv2.imread("images/orange.jpg")

    # generate Gaussian pyramid for A
    G = img1.copy()
    gpA = [G]
    for i in range(6):
        G = cv2.pyrDown(G)
        gpA.append(G)

    # generate Gaussian pyramid for B
    G = img2.copy()
    gpB = [G]
    for i in range(6):
        #     yeah = cv2.pyrDown(ff_)
        G = cv2.pyrDown(G)
        gpB.append(G)

    # We generate a Gaussian pyramid for the image with the orange.
    # generate Laplacian Pyramid for A
    lpA = [gpA[5]]
    for i in range(5, 0, -1):
        #     GE = cv2.pyrUp(gpA[i])
        GE = cv2.pyrUp(gpA[i])
        L = cv2.subtract(gpA[i - 1], GE)
        lpA.append(L)

    # generate Laplacian Pyramid for B
    lpB = [gpB[5]]
    for i in range(5, 0, -1):
        GE = cv2.pyrUp(gpB[i])
        L = cv2.subtract(gpB[i - 1], GE)
        lpB.append(L)

    # We generate a Laplacian pyramid for both of the images.
    # Now add left and right halves of images in each level
    LS = []
    for la, lb in zip(lpA, lpB):
        rows, cols, dpt = la.shape
        ls = np.hstack((la[:, 0 : int(cols / 2)], lb[:, int(cols / 2) :]))
        LS.append(ls)

    # We add the halves of the images.
    # now reconstruct
    ls_ = LS[0]
    for i in range(1, 6):
        ls_ = cv2.pyrUp(ls_)
        ls_ = cv2.add(ls_, LS[i])
    cv2.imshow("RESULT", ls_)
    cv2.waitKey(0)
