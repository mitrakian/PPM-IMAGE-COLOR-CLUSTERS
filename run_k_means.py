#Mitra Kian
#Kian0016
#PROJECT 1 CSCI 1913
#run_k_means.py

from k_means import *
from image_utils import *

if __name__ == "__main__":
    """
    This "main" statement prompts users for the number of clusters they would like to create, the name of the file
     they'd life to convert, and the name of 
    """
    print("Welcome to the K-Means 'running' program!")
    k = int(input("Please enter the number (k) of clusters you would like to create: "))
    image_file = input("Please enter the name of the image file name you would like to load (please include'.ppm'): ")
    image_save = input("Please enter what you'd like to name the image file (please include '.ppm'): ")

    image = read_ppm(image_file)
    image = replace_image(image,k)
    save_ppm(image_save, image)

