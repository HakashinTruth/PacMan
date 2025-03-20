class Interaction:
    def __init__(self, pacman, ghosts, keyboard, walls, squares, points):
        self.pacman = pacman
        self.ghosts = ghosts
        self.keyboard = keyboard
        self.walls = walls
        self.squares = squares  # Rename for clarity
        self.points = points
        self.last_collision = None
        self.lives = 1
        self.score = 0
        
        # Create a spatial lookup grid for faster collision detection
        self.wall_grid = {}
        self.setup_collision_grid()
    
    def setup_collision_grid(self):
        # Create a grid-based lookup for walls to speed up collision detection
        grid_size = 40  # Size of each grid cell
        
        # Populate grid with walls
        all_walls = self.walls + self.squares
        for wall in all_walls:
            # Get grid cells this wall might occupy
            min_x = int(min(wall.x1, wall.x2) / grid_size)
            max_x = int(max(wall.x1, wall.x2) / grid_size) + 1
            min_y = int(min(wall.y1, wall.y2) / grid_size)
            max_y = int(max(wall.y1, wall.y2) / grid_size) + 1
            
            # Add this wall to all relevant grid cells
            for x in range(min_x, max_x):
                for y in range(min_y, max_y):
                    key = (x, y)
                    if key not in self.wall_grid:
                        self.wall_grid[key] = []
                    self.wall_grid[key].append(wall)
    
    def get_nearby_walls(self, entity):
        # Get grid cell of entity
        grid_size = 40
        grid_x = int(entity.pos.x / grid_size)
        grid_y = int(entity.pos.y / grid_size)
        
        nearby_walls = []
        
        # Check surrounding grid cells
        for x in range(grid_x-1, grid_x+2):
            for y in range(grid_y-1, grid_y+2):
                key = (x, y)
                if key in self.wall_grid:
                    nearby_walls.extend(self.wall_grid[key])
        
        return nearby_walls
    
    def update(self):
        self.last_collision = None
        
        # Only check nearby walls for collision
        nearby_walls = self.get_nearby_walls(self.pacman)
        for wall in nearby_walls:
            if wall.hit(self.pacman):
                self.pacman.stop()
                self.last_collision = wall
                
                # Adjust position
                if wall.x1 == wall.x2:  # Vertical wall
                    if self.pacman.pos.x < wall.x1:
                        self.pacman.pos.x = wall.x1 - self.pacman.radius
                    else:
                        self.pacman.pos.x = wall.x1 + self.pacman.radius
                else:  # Horizontal wall
                    if self.pacman.pos.y < wall.y1:
                        self.pacman.pos.y = wall.y1 - self.pacman.radius
                    else:
                        self.pacman.pos.y = wall.y1 + self.pacman.radius
                
                break  # Stop checking after first collision
        
        # Ghost-wall collisions
        for ghost in self.ghosts:
            ghost_nearby_walls = self.get_nearby_walls(ghost)
            for wall in ghost_nearby_walls:
                if wall.hit(ghost):
                    ghost.stop()
                    
                    if hasattr(ghost, 'current_direction') and ghost.__class__.__name__ == 'OtherGhost':
                        import random
                        directions = ["left", "right", "up", "down"]
                        newDirection = ghost.current_direction
                        while newDirection == ghost.current_direction:
                            newDirection = directions[random.randint(0,3)]
                        ghost.current_direction = newDirection
                    
                    # Adjust position
                    if wall.x1 == wall.x2:  # Vertical wall
                        if ghost.pos.x < wall.x1:
                            ghost.pos.x = wall.x1 - ghost.radius
                        else:
                            ghost.pos.x = wall.x1 + ghost.radius
                    else:  # Horizontal wall
                        if ghost.pos.y < wall.y1:
                            ghost.pos.y = wall.y1 - ghost.radius
                        else:
                            ghost.pos.y = wall.y1 + ghost.radius
                    
                    break
        
        # Point collection and ghost collision
        for point in list(self.points):  # Use a copy to avoid modification during iteration
            if self.pacman.collidedWithPoint(point):
                self.points.remove(point)
                self.score += 10
        
        for ghost in self.ghosts:
            if self.pacman.collidedWithPoint(ghost):
                self.lives -= 1
                self.pacman.reset_position()

                      