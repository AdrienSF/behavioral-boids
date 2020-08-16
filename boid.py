import numpy as np

class Boid():
    def __init__(self):
        self.view_range = 100
        # self.collision_range = 20
        self.speed_cap = 50

        # set random velocity
        self.velocity = np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])
        # set random position
        self.position = np.array([np.random.uniform(0, 640), np.random.uniform(0, 480)])

        self.immitation_factors = {'A': 1, 'B': 1, 'C': 1}
        # set random movement function
        A = np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
        B = np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
        C = np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
        self.movement_func_coefs = {'A': A, 'B': B, 'C': C}


    def move(self, dt):
        self.position = np.array(self.position) + np.array(self.velocity) * dt
        self.screenwrap()


    def set_new_velocity(self, flock: list, dt):
        flock_velocity = np.array([])
        flock_relative_pos = np.array([])
        in_view = [ boid for boid in flock if np.linalg.norm(np.array(boid.position) - np.array(self.position)) < self.view_range and boid != self ]

        if in_view:
            self.set_new_coefs(in_view, dt)
            #inefficiency here may be an issue:
            flock_velocity = np.mean([ boid.velocity for boid in in_view ], axis=0)
            flock_relative_pos = np.mean([ boid.position for boid in in_view ], axis=0) - self.position

        self.velocity = self.velocity + self.movement_func(flock_velocity, flock_relative_pos) * dt

        # speed cap
        if np.linalg.norm(self.velocity) > self.speed_cap:
            self.velocity = self.speed_cap * (self.velocity / np.linalg.norm(self.velocity))

    def movement_func(self, flock_velocity, flock_relative_pos):
        # if there are no boids in view, return only the constant part of the movement function
        if flock_relative_pos.size == 0 and flock_velocity.size == 0:
            return self.movement_func_coefs['C']
        else:
            return self.movement_func_coefs['A'] * flock_velocity + self.movement_func_coefs['B'] * flock_relative_pos + self.movement_func_coefs['C']

    def set_new_coefs(self, boids, dt): #inefficiency here may be an issue
        self.movement_func_coefs['A'] += self.immitation_factors['A'] * np.mean([ boid.movement_func_coefs['A'] for boid in boids ], axis=0) * dt
        self.movement_func_coefs['B'] += self.immitation_factors['B'] * np.mean([ boid.movement_func_coefs['B'] for boid in boids ], axis=0) * dt
        self.movement_func_coefs['C'] += self.immitation_factors['C'] * np.mean([ boid.movement_func_coefs['C'] for boid in boids ], axis=0) * dt

    def screenwrap(self):
        # make screen wrap around
        if self.position[0] < 0:
            self.position[0] = 640

        if self.position[1] < 0:
            self.position[1] = 480

        if self.position[0] > 640:
            self.position[0] = 0

        if self.position[1] > 480:
            self.position[1] = 0

    #     # avoid other boids
    #     other_boids = [ np.array(other.position) - np.array(self.position) for other in flock if np.linalg.norm(np.array(self.position) - np.array(other.position)) < self.collision_range]
    #     if other_boids:
    #         avoid_obs = -1 * np.mean(other_boids, axis=0)
    #     else:
    #         avoid_obs = np.array([0.0, 0.0])
        
    #     # normalize avoidance vector, otherwise there's less "avoidance" the closer boids are to colliding 
    #     if np.linalg.norm(avoid_obs) != 0:
    #         avoid_obs = avoid_obs / np.linalg.norm(avoid_obs)
    #     return self.collision_factor * avoid_obs

