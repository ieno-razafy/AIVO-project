import cv2
import numpy
import matplotlib.pyplot as plt


def rgb_to_gray(image):
    """ Convert colored image to gray level """

    blue, green, red = cv2.split(image)
    gray_image = 0.299 * red + 0.587 * green + 0.144 * red
    gray_image = gray_image.astype(numpy.uint8)

    return gray_image


def rotate(image, angle):
    """ Rotate an image with an angle """

    image_height, image_width = image.shape[:2]
    matrix_of_image_pixels = cv2.getRotationMatrix2D((image_width / 2, image_height / 2), angle, 1)

    return cv2.warpAffine(image, matrix_of_image_pixels, (image_width, image_height))


def compute_histogram(image):
    """ Compute the histogram of an image """

    gray_image = rgb_to_gray(image)
    image_height, image_width = image.shape[:2]

    image_histogram = numpy.zeros(256, int)

    for i in range(0, image_height):
        for j in range(0, image_width):
            image_histogram[gray_image[i][j]] = image_histogram[gray_image[i][j]] + 1

    return image_histogram


def binarize(image, thresh):
    """ Binarize an image """

    gray_image = rgb_to_gray(image)
    image_height, image_width = image.shape[:2]

    binary_image = gray_image

    for i in range(0, image_width):
        for j in range(0, image_height):
            if gray_image[i][j] < thresh:
                binary_image[i][j] = 0
            else:
                binary_image[i][j] = 255

    return binary_image


def inverse(image):
    """ Inverse an image """

    gray_image = rgb_to_gray(image)
    image_height, image_width = image.shape[:2]
    I_MAX = image.max()

    inversed_image = gray_image

    for i in range(0, image_width):
        for j in range(0, image_height):
            # image[i][j] = 255 - image[i][j]
            inversed_image[i][j] = I_MAX - gray_image[i][j]

    return inversed_image


def equalize_histogram(image):
    """ Equalize the histogram of an image """

    gray_image = rgb_to_gray(image)
    image_height, image_width = image.shape[:2]
    histogram = numpy.zeros(256, int)

    for i in range(0, image_width):
        for j in range(0, image_height):
            histogram[gray_image[i][j]] = histogram[gray_image[i][j]] + 1

    histogram_cumulated = numpy.zeros(256, int)
    histogram_cumulated[0] = histogram[0]
    for i in range(1, 256):
        histogram_cumulated[i] = histogram[i] + histogram_cumulated[i - 1]

    number_of_pixels = gray_image.size
    hist0c = histogram_cumulated / number_of_pixels * 255

    for i in range(0, gray_image.shape[0]):
        for j in range(0, gray_image.shape[1]):
            gray_image[i][j] = hist0c[gray_image[i][j]]

    return cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)


def stretch_histogram(image, min, max):
    """ Stretch the histogram of an image """

    gray_image = rgb_to_gray(image)
    image_height, image_width = image.shape[:2]

    for i in range(0, image_width):
        for j in range(0, image_height):
            gray_image[i][j] = (255 * (gray_image[i][j] - min)) / (max - min)

    return cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)


def blur(image):
    """ Blur an image """

    gray_image = rgb_to_gray(image)
    filter_size = 7
    filter = (1 / (filter_size * filter_size)) * numpy.ones((filter_size, filter_size), dtype=numpy.uint8)

    new_image = numpy.zeros(image.shape, dtype=numpy.uint8)

    for x in range(0, gray_image.shape[0]):
        for y in range(0, gray_image.shape[1]):
            filter_half_width = filter.shape[0] // 2
            filter_half_height = filter.shape[1] // 2
            pixel_value = 0

            for i in range(0, filter.shape[0]):
                for j in range(0, filter.shape[1]):
                    x_image = x + i - filter_half_width
                    y_image = y + j - filter_half_height
                    if (x_image >= 0) and (x_image < gray_image.shape[0]) and (y_image >= 0) and (y_image < gray_image.shape[1]):
                        pixel_value += filter[i, j] * image[x_image, y_image]

            new_image[x, y] = pixel_value

    return new_image


def dilatation(binary_image):
    """ Dilate a binary image """

    filter = numpy.ones((3, 3), dtype=numpy.uint8)
8
    dilated_image = numpy.zeros(binary_image.shape, dtype=numpy.uint8)

    for x in range(0, binary_image.shape[0]):
        for y in range(0, binary_image.shape[1]):
            filter_half_width = filter.shape[0] // 2
            filter_half_height = filter.shape[1] // 2
            pixel_value = 0

            for i in range(0, filter.shape[0]):
                for j in range(0, filter.shape[1]):
                    x_image = x + i - filter_half_width
                    y_image = y + j - filter_half_height
                    if (x_image >= 0) and (x_image < binary_image.shape[0]) and (y_image >= 0) and (y_image < binary_image.shape[1]):
                        if binary_image[x_image, y_image] and filter[i, j]:
                            pixel_value = 255

            dilated_image[x, y] = pixel_value

    return dilated_image


def erosion(binary_image):
    """ Erode a binary image """

    filter = numpy.ones((3, 3), dtype=numpy.uint8)

    eroded_image = numpy.zeros(binary_image.shape, dtype=numpy.uint8)

    
    for x in range(0, binary_image.shape[0]): 
        for y in range(0, binary_image.shape[1]):
            filter_half_width = filter.shape[0] // 2
            filter_half_height = filter.shape[1] // 2
            pixel_value = 255

            for i in range(0, filter.shape[0]):
                for j in range(0, filter.shape[1]):
                    x_image = x + i - filter_half_width
                    y_image = y + j - filter_half_height
                    if (x_image >= 0) and (x_image < binary_image.shape[0]) and (y_image >= 0) and (y_image < binary_image.shape[1]):
                        if filter[i, j] and not (binary_image[x_image, y_image]):
                            pixel_value = 0

            eroded_image[x, y] = pixel_value

    return eroded_image


def opening(image):
    """ Apply dilatation just after erosion operation
    to an image which need to be binarizing first """

    binarized_image = binarize(image, 128)

    return dilatation(erosion(binarized_image))


def closing(image):
    """ Apply erosion just after dilatation operation
    to an image which need to be binarizing first """

    binarized_image = binarize(image, 128)

    return erosion(dilatation(binarized_image))


def opening_top_hat(image):
    binary_image = binarize(image, 128)

    return binary_image - opening(image)


def closing_top_hat(image):
    binary_image = binarize(image, 128)

    return closing(image) - binary_image


def detect_edge(image):
    """ Detect edge on an image """

    binary_image = binarize(image, 128)

    image_after_dilatation = dilatation(binary_image)
    image_after_dilatation = binary_image - image_after_dilatation

    image_after_erosion = erosion(binary_image)
    image_after_erosion = binary_image - image_after_erosion

    return image_after_dilatation + image_after_erosion
