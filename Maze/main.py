import matplotlib.pyplot as plt

image = []
helper_matrix = []
black = [0,0,0]
white = [255,255,255]
starting_point = [1,1]
red_dot = [47,1]

def initialise_array(img):
    for i in range(0,51):
        img.append([])
        for j in range(0,51):
            img[i].append(0)
    return img

def create_maze(file, row = 0, col = 0):
    img = initialise_array(image)
    with open(file, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip("\n")
        if line == "True":
            img[row][col] = black
        else:
            img[row][col] = white
        row += 1
        if row % 51 == 0:
            row = 0
            col += 1

    img[starting_point[0]][starting_point[1]] = [0, 255, 0]
    img[red_dot[0]][red_dot[1]] = [255, 0, 0]

    return img

def make_step(image, k):
    for i in range(len(helper_matrix)):
        for j in range(len(helper_matrix[i])):
            if helper_matrix[i][j] == k:
                if i>0 and helper_matrix[i-1][j] == 0 and image[i-1][j] != black:
                  helper_matrix[i-1][j] = k + 1
                if j>0 and helper_matrix[i][j-1] == 0 and image[i][j-1] != black:
                  helper_matrix[i][j-1] = k + 1
                if i<len(helper_matrix)-1 and helper_matrix[i+1][j] == 0 and image[i+1][j] != black:
                  helper_matrix[i+1][j] = k + 1
                if j<len(helper_matrix[i])-1 and helper_matrix[i][j+1] == 0 and image[i][j+1] != black:
                   helper_matrix[i][j+1] = k + 1

def find_all_paths(k = 0):
    while helper_matrix[red_dot[0]][red_dot[1]] == 0:
        k += 1
        make_step(image, k)

def find_shortest_path():
    find_all_paths()
    i, j = red_dot
    k = helper_matrix[i][j]
    the_path = [(i, j)]
    while k > 1:
        if i > 0 and helper_matrix[i - 1][j] == k - 1:
            i, j = i - 1, j
            the_path.append((i, j))
            k -= 1
        elif j > 0 and helper_matrix[i][j - 1] == k - 1:
            i, j = i, j - 1
            the_path.append((i, j))
            k -= 1
        elif i < len(helper_matrix) - 1 and helper_matrix[i + 1][j] == k - 1:
            i, j = i + 1, j
            the_path.append((i, j))
            k -= 1
        elif j < len(helper_matrix[i]) - 1 and helper_matrix[i][j + 1] == k - 1:
            i, j = i, j + 1
            the_path.append((i, j))
            k -= 1
    return the_path

def color_path_to_red_dot(path, color):
    for cord in path[1:len(path)-1]:
        image[cord[0]][cord[1]] = color

helper_matrix = initialise_array(helper_matrix)
helper_matrix[starting_point[0]][starting_point[1]] = 1

image = create_maze("design.txt")
shortest_path = find_shortest_path()
color_path_to_red_dot(shortest_path, [0,0,255])

plt.imshow(image)
plt.show()