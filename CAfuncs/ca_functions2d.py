from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def plot2d(ca, timestep=None, title=''):
    cmap = plt.get_cmap('Greys')
    plt.title(title)
    if timestep is not None:
        data = ca[timestep]
    else:
        data = ca[-1]
    plt.imshow(data, interpolation='none', cmap=cmap)
    plt.show()

def plot2d_slice(ca, slice=None, title=''):
    cmap = plt.get_cmap('Greys')
    plt.title(title)
    if slice is not None:
        data = ca[:, slice]
    else:
        data = ca[:, len(ca[0])//2]
    plt.imshow(data, interpolation='none', cmap=cmap)
    plt.show()

def plot2d_spacetime(ca, alpha=None, title=''):
    fig = plt.figure(figsize=(10, 7))
    plt.title(title)
    ax = fig.gca(projection='3d')
    ca = ca[::-1]
    xs = np.arange(ca.shape[2])[None, None, :]
    ys = np.arange(ca.shape[1])[None, :, None]
    zs = np.arange(ca.shape[0])[:, None, None]
    xs, ys, zs = np.broadcast_arrays(xs, ys, zs)
    masked_data = np.ma.masked_where(ca == 0, ca)
    ax.scatter(xs.ravel(),
               ys.ravel(),
               zs.ravel(),
               c=masked_data, cmap='cool', marker='s', depthshade=False, alpha=alpha, edgecolors='#0F0F0F')
    plt.show()

from matplotlib.colors import ListedColormap, LinearSegmentedColormap
def plot2d_animate(ca, title='', image_name = '', begin_save = 0, end_save = 200):

    cmp = plt.get_cmap('Greys')
    fig = plt.figure()
    plt.title(title)
    plt.axis('off')
    im = plt.imshow(ca[0], animated=True, cmap=cmp)
    i = {'index': 0}
    def updatefig(*args):

        i['index'] += 1
        if i['index'] > end_save:
            plt.close(fig)
        if i['index'] == len(ca):
            i['index'] = 0
        im.set_array(ca[i['index']])
        if (i['index']+1 >= begin_save and i['index']+1 <= end_save):
            plt.savefig('data/' + image_name + str(i['index']+1)+".png", bbox_inches = 'tight', transparent = 'True', pad_inches = 0)
        return im,
    ani = animation.FuncAnimation(fig, updatefig, interval=1, blit=True)
    #fig.savefig()
    #ani.save('animationframe.png')

    fig.canvas.manager.window.showMinimized()
    # mng = plt.get_current_fig_manager()
    # mng.frame.Minimize(True)
    plt.show()

def init_simple2d(rows, cols, val=1, dtype=np.int):
    """
    Returns a matrix initialized with zeroes, with its center value set to the specified value, or 1 by default.
    :param rows: the number of rows in the matrix
    :param cols: the number of columns in the matrix
    :param val: the value to be used in the center of the matrix (1, by default)
    :param dtype: the data type
    :return: a tensor with shape (1, rows, cols), with the center value initialized to the specified value, or 1 by default
    """
    x = np.zeros((rows, cols), dtype=dtype)
    x[x.shape[0]//2][x.shape[1]//2] = val
    return np.array([x])

# Randy implemented
def init_random2d_anyK(rows, cols, num_states, dtype=np.int):
    """
    Returns a randomly initialized matrix with values consisting of numbers in {0, k-1}
    """
    if np.issubdtype(dtype, np.integer):
        rand_nums = np.random.randint(2, size=(rows, cols), dtype=dtype)
        rand_nums[rand_nums== 1] = num_states-1
    return np.array([rand_nums])


def evolve2dMoore(cellular_automaton, survive_arr, born_arr, num_states, timesteps, apply_rule, r=1, neighbourhood='Moore'):
    # """
    #
    # :param cellular_automaton:
    # :param timesteps: the number of time steps in this evolution; note that this value refers to the total number of
    #                   time steps in this cellular automaton evolution, which includes the initial condition
    # :param apply_rule: a function representing the rule to be applied to each cell during the evolution; this function
    #                    will be given three arguments, in the following order: the neighbourhood, which is a numpy
    #                    2D array of dimensions 2r+1 x 2r+1, representing the neighbourhood of the cell (if the
    #                    'von Neumann' neighbourhood is specified, the array will be a masked array); the cell identity,
    #                    which is a tuple representing the row and column indices of the cell in the cellular automaton
    #                    matrix, as (row, col); the time step, which is a scalar representing the time step in the
    #                    evolution
    # :param r: the neighbourhood radius; the neighbourhood dimensions will be 2r+1 x 2r+1
    # :param neighbourhood: the neighbourhood type; valid values are 'Moore' or 'von Neumann'
    # :return:
    # """
    _, rows, cols = cellular_automaton.shape
    array = np.zeros((timesteps, rows, cols), dtype=cellular_automaton.dtype)
    array[0] = cellular_automaton

    def get_neighbourhood(cell_layer, row, col):
        row_indices = range(row - r, row + r + 1)
        row_indices = [i - cell_layer.shape[0] if i > (cell_layer.shape[0] - 1) else i for i in row_indices]
        col_indices = range(col - r, col + r + 1)
        col_indices = [i - cell_layer.shape[1] if i > (cell_layer.shape[1] - 1) else i for i in col_indices]
        n = cell_layer[np.ix_(row_indices, col_indices)]
        if neighbourhood == 'Moore':
            return n
        # elif neighbourhood == 'von Neumann':
        #     return np.ma.masked_array(n, von_neumann_mask)
        else:
            raise Exception("unknown neighbourhood type: %s" % neighbourhood)

    # This is the bottle neck. O(N^3). Try to parallelize in the future.
    for t in range(1, timesteps):
        print("generation " + str(t), flush=True)
        cell_layer = array[t - 1] # Use the CA matrix from the previous time step to perform calculation
        for row, cell_row in enumerate(cell_layer):
            for col, cell in enumerate(cell_row):
                n = get_neighbourhood(cell_layer, row, col)
                array[t][row][col] = apply_rule(n, survive_arr, born_arr, num_states)
    return array

def random_2d_rule(neighbourhood, survive_arr, born_arr, num_states): # c is the cell position. t is the timestep
    center_cell = neighbourhood[1][1]
    #make_live_cells_1 =np.minimum(neighbourhood, 1) This was the bug. need to treat transition cells as dead!
    max_state = num_states - 1
    make_live_cells_1 = (neighbourhood == max_state).astype(int)
    #total = np.sum(neighbourhood) #this was also a bug
    total = np.sum(make_live_cells_1)
#http://psoup.math.wisc.edu/mcell/rullex_gene.html#Brian%27s%20Brain
    if center_cell == max_state: # live. Could be multiple live states.
        for num_neighbors in survive_arr: # Brian's brain doesn't have a surviving arr
            if total - 1 == num_neighbors:
                return center_cell  # Any live cell with two or three live neighbours lives on to the next generation.
        return center_cell - 1 # Either decremented living state or, if it survived, same state
    elif center_cell != 0 and center_cell !=max_state: #transition state. it cannot immediately become alive again
        return center_cell - 1
    else:
        for num_neighbors in born_arr:
            if total == num_neighbors:
                return  max_state  # Any live cell with two or three live neighbours lives on to the next generation.
        return 0
