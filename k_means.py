from image_utils import *
from math import *


def initial_means_list(k):
    """
    creates a list of initial random colors which will act as the initial means list
    """
    initial_means_list = [0 for i in range(k)]
    for i in range(k):
        initial_means_list[i] = random_color()
    return initial_means_list

def distance(color,means_list):
    """
    The function will take the color tuple parameter and compare it each color in the means list, then the function will
    compute each distance, store it in a list, and return the list of distances
    """
    red, green, blue = color
    list=[0 for i in range(len(means_list))]
    for i in range(len(means_list)):
        r2, g2, b2 = means_list[i]
        dist = sqrt((red - r2) ** 2 + (green - g2) ** 2 + (blue - b2) ** 2)
        list[i]=dist
    return list

def least_distance(color,means_list):
    """
    The function calls the 'distance' function which returns a list of distances from the color to each element in the means list.
    Then, the function compares all the computed distances, and returns the index in the list which corresponds to the smallest distance.
    The index returned will correspond to the color in the means list which the tested color is closest to.
    """
    distance_list = distance(color,means_list)
    least = distance_list[0]
    index=0
    for i in range(len(means_list)):
        if least > distance_list[i]:
            least=distance_list[i]
            index = i
    return index

def create_asi_list(image, k,means_list,width,height):
    """
    This function creates an assignment list of lists, calls the least distance function to find the index of the means
    list value 'closest' to the value, then inputs the index into the assignment list, and returns the assignment list
    """
    assignment = [[0 for j in range(height)] for i in range(width)]
    for i in range(width):
        for j in range(height):
            assignment[i][j]=least_distance(image[i][j], means_list)
    return assignment

def k_assignments(assignment,k,width,height):
    """
    This function goes through the assignments list and finds the (x,y) or '(i,j)' coordinates of every pixel in the
    assignment list assigned to a specific color. Then the function creates a list of all the coordinates
    """
    list=[]
    for i in range(width):
        for j in range(height):
            if assignment[i][j] == k:
                list.append((i, j))
    return list

def avg_of_means(assign_to_k,image):
    """
    The function takes the all of the coordinates of pixels assigned to a specific cluster color, then it uses those
    coordinates to find the average color coordinates for all elements in the cluster.
    """
    new_mean_color = average(assign_to_k,image)

    return new_mean_color


def average(assign_to_k, image):
    """
    Goes through the assign_to_k list of coordinates to access the pixels in the image, the sums all the red, green, and blue
    coordinates of the colors and averages them to find the 'average' color.
    """
    red_sum = 0
    blue_sum = 0
    green_sum = 0
    length = len(assign_to_k)
    if length == 0:
        return (0,0,0)
    for i in range(length):
        x, y = assign_to_k[i]
        red, green, blue = image[x][y]
        red_sum += red
        green_sum += green
        blue_sum += blue
    return (red_sum // length, green_sum // length, blue_sum // length)


def redo_means(image, means_list,assignment,width,height):
    """
    This function will generate a new means list based on the averages colors assigned to each cluser.
    """

    list=[0 for i in range(len(means_list))]

    for i in range(len(means_list)):
        assign_to_k = k_assignments(assignment,i,width,height)
        to_i = avg_of_means(assign_to_k,image)

        list[i]=to_i



    return list

def k_means(image, k):
    """
    This is the k means algorithm to create the clusters of the most common colors in the image (ie the means listO and
    the pixels associated with each color (ie the asscoiations list). The algorithm stops when the associations list
    stops changing.
    """
    assignment = []
    assignment_copy = 0
    means_list = initial_means_list(k)
    width, height = get_width_height(image)
    assignment = create_asi_list(image, k, means_list, width, height)

    while assignment != assignment_copy:

        assignment_copy = assignment
        means_list = redo_means(image, means_list, assignment, width, height)
        assignment = create_asi_list(image, k, means_list, width, height)

    return means_list, assignment


def replace_image(image,k):
    """
    This function runs the k_means algorithm and takes the produced associations list and means list to produce the image
    as a list of lists of tuples.
    """
    means,assignments = k_means(image,k)
    width,height=get_width_height(image)
    for i in range(width):
        for j in range(height):
            m_l_index=assignments[i][j]
            color=means[m_l_index]
            image[i][j]=color
    return image
