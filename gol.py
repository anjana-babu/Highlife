import sys
import random
class bcolors:
    """ bcolors: Facilitates printing colors on terminals with support for
    escape sequences. It was borrowed from the following stackoverflow answer:
    <http://stackoverflow.com/a/287944>
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def get_term_size():
    """ get_term_size: Returns a tuple of the host's terminal width and size
    (in that order).  This code should be platform independent and was borrowed
    from the following stackoverflow answer:
    <http://stackoverflow.com/a/566752>
    """
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])

def clear_terminal():
    """ clear_terminal: Clears the terminal's window.
    """
    import sys
    sys.stdout.write( chr(27) + "[2J" )

def main():
    # Define grid
    (width, height) = get_term_size()
    grid = [(width-5)*[0] for i in range(height-5)]


    # Draw initial grid
    update_screen(grid)

    # Read initial config
    read_initial_conf(grid)

    # Step through grid
    prompt = ('ITER %d: Type anything to continue, the number of steps to ' + 
              'perform (or quit to exit): ')
    iter_step = 1
    update_screen(grid)
    while True:
        # Wait for user
        play = raw_input('%s' % (prompt % iter_step))
        if play == 'quit':
            break
        try:
            batch_steps = int(play)
        except:
            batch_steps = 1
            pass
        for i in range(batch_steps):
            # Define auxiliary grid matrix
            new_grid = [len(grid[0])*[0] for i in range(len(grid))]
            # Update grid
            next_step(grid, new_grid)
            grid, new_grid = new_grid, grid
            # Print updated grid
            update_screen(grid)
        iter_step += batch_steps


def update_screen(grid):
    """ update_screen: Takes the grid and updates the terminal to display it.
    (Making this function more efficient and informative is a to-do)
    """
    clear_terminal()
    print bcolors.RED + ' '*( len(grid[0])/2 - 5) + ' GAME OF LIFE (HIGHLIFE)' + bcolors.ENDC
    print bcolors.YELLOW + '-'*( len(grid[0]) + 5) + bcolors.ENDC
    print
    for i, line in enumerate(grid):
        print bcolors.BLUE + '%3d ' % i + bcolors.ENDC,
        for element in line:
            if element:
                sys.stdout.write(bcolors.GREEN + 'x' + bcolors.ENDC)
            else:
                sys.stdout.write(' ')
        print
    print bcolors.YELLOW + '-' * ( len(grid[0]) + 5 ) + bcolors.ENDC

def read_initial_conf(grid):
    row = len(grid) 
    col = len(grid[0])

    if row * col > 10:
        total_init_items = random.randint(10, row * col)
    else:
        total_init_items = random.randint(0, row * col)

    for loop in range(total_init_items):
        coord = [0, 0]
        coord[0] = random.randint(0, col-1)
        coord[1] = random.randint(0, row-1)
        
        # Update grid (it actually toggles the grid position provided)
        grid [coord[1]][coord[0]] = (grid[coord[1]][coord[0]] + 1) % 2
        update_screen(grid) 

def next_step(grid, new_grid):
    """ next_step: Computes the grid's next step and stores it in the list
    new_grid. The latter needing to have been previously defined.
    B3S23
    B36S23 Highlife
    """
    # For each column in grid...
    for x in range(0, len(grid[0])):
        # Iterate through each line in grid
        for y in range(0, len(grid)):
            # Count live cells around (x, y)
            live_neighbors = healthy_neighbors(x, y, grid)
            # Apply Game of Life's rules B3S23
            if grid[y][x]:
                if live_neighbors < 2 or live_neighbors > 3: 
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = grid[y][x]
            else:
                #if live_neighbors == 3: # B3S23
                if live_neighbors == 3  or live_neighbors == 2: # B23S23
                    new_grid[y][x] = 1

def healthy_neighbors(x, y, grid):
    """ healthy_neighbors: Returns the number of live cells neighboring the 
    given coordinate. Given it treats the grid as a loop (making this
    optional is a to-do) it should be able to handle most dumb calls.
    """
    live_neighbors = 0
    for i in range(-1, 2):
        testx = (x+i) % len(grid[0])
        for j in range(-1, 2):
            testy = (y+j) % len(grid)
            if j == 0 and i == 0:
                continue
            if grid[testy][testx] == 1:
                live_neighbors += 1
    return live_neighbors

if __name__ == '__main__':
    main()

