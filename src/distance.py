import numpy as np
######top and bottom are cordinates

## Transform x or y in pixel space to X or Y in scene space
def transform_coordinate(pixel_coordinates, l,L):
    scene_coordinates = (L*pixel_coordinates)/l ## Since L/l = Y/y => y*L/l=Y
    return scene_coordinates

def get_distance_given_length(top, bottom, origin=(0,0), L=165, f = 1):
    l = top[1]-bottom[1]
    centers = (top + bottom)/2
    centers_list = centers.tolist()
    centers_list.append(f)
    # print(centers_list)
    coordinates = np.array(centers_list)
    coordinates_scene = transform_coordinate(coordinates,l,L)
    # print(coordinates_scene)
    return coordinates_scene[2]


# Example call
# get_distance_given_length(np.array([3,165]),np.array([3,0]))