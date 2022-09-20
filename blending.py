#!/usr/bin/env python3.7
import numpy as np

## NOTE:
## YOU NEED TO MAKE SURE BOTH IMAGES HAVE SAME SIZE (HEIGHT*WIDTH)

# ----------------------------------------------------- System
# check if platform is windows or linux:
# import sys
# from sys import platform
# if platform == "linux" or platform == "linux2":
#     sys.path.append("/opt/opencv-4.1.2/build/lib/python3")
# elif platform == "win32":
#     print("")
#     sys.path.append("C:/Users/xxx/Desktop/opencv/opencv-4.1.2/build/lib/python3")
# else:
#     print("only for linux or windows")
#     sys.exit(-1)
import cv2


def pyramid_blend(A, B, m, num_levels):
    # 1. as in api55's answer, mask needs to be from 0 to 1, since you're multiplying a pixel value by it. Since mask
    # is binary, we only need to set all values which are 255 to 1
    m[m == 255] = 1

    GA = A.copy()
    GB = B.copy()
    GM = m.copy()

    gpA = [GA]
    gpB = [GB]
    gpM = [GM]

    for i in range(num_levels):
        GA = cv2.pyrDown(GA)
        GB = cv2.pyrDown(GB)
        GM = cv2.pyrDown(GM)

        gpA.append(np.float32(GA))
        gpB.append(np.float32(GB))
        gpM.append(np.float32(GM))

    lpA = [gpA[num_levels - 1]]
    lpB = [gpB[num_levels - 1]]
    gpMr = [gpM[num_levels - 1]]

    for i in range(num_levels - 1, 0, -1):
        size = (gpA[i - 1].shape[1], gpA[i - 1].shape[0])

        LA = np.subtract(gpA[i - 1], cv2.pyrUp(gpA[i], dstsize=size))
        LB = np.subtract(gpB[i - 1], cv2.pyrUp(gpB[i], dstsize=size))

        lpA.append(LA)
        lpB.append(LB)

        gpMr.append(gpM[i - 1])

    LS = []
    for la, lb, gm in zip(lpA, lpB, gpMr):
        ls = la * gm + lb * (1.0 - gm)
        LS.append(ls)

    ls_ = LS[0]
    for i in range(1, num_levels):
        size = (LS[i].shape[1], LS[i].shape[0])
        ls_ = cv2.add(cv2.pyrUp(ls_, dstsize=size), np.float32(LS[i]))
        # 2. because of floating point rounding error, some pixels in ls_ will be larger than 255, and some will be
        # lower than 0. When casting back to uint8, this causes pixels lower than 0 to get wrapped around to 255, so we
        # should threshold it before passing it back
        ls_[ls_ > 255] = 255
        ls_[ls_ < 0] = 0

    # 3. when passing back, before saving and displaying, need to cast back to a uint8 from float64
    return ls_.astype(np.uint8)


if __name__ == "__main__":

    A = cv2.imread("./images/black.jpg")
    B = cv2.imread("./images/white.jpg")
    m = cv2.imread("./images/mask.jpg")

    lpb = pyramid_blend(A, B, m, 6)

    cv2.imshow("foo", lpb)
    cv2.waitKey()
    cv2.destroyAllWindows()
