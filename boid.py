import numpy as np
from collections import deque 

# https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
# ---------------------------------------------------------------------------------------------------------------


class Boid():
    def __init__(self):
        self.view_range = 20
        self.field_of_view = np.pi
        self.collision_range = 10
        self.speed_cap = 10000
        self.expiration_age = 50
        self.past_saving_interval = 1

        # set random velocity
        self.velocity = np.array([np.random.uniform(-80, 80), np.random.uniform(-80, 80)])
        # set random position
        self.position = np.array([np.random.uniform(0, 640), np.random.uniform(0, 480)])
        # create dict of past positions and velocities
        self.past = deque([ {'age': 0, 'pos': self.position, 'vel': self.velocity} ])

        self.match_position_factor = 1/80
        self.match_velocity_factor = 1/20
        self.collision_factor = 4


    def move(self, dt):
        # velocity adds to position
        self.position = np.array(self.position) + np.array(self.velocity) * dt

        # remove expired past info.
        # oldest past info is furthest to the left, so we keep removing leftmost info until we reach non-expired items.
        # FIFO queues should be efficient with collections.deque
        while self.past[0]['age'] >= self.expiration_age:
            self.past.popleft()

        # if enough time has passed since the last past info has been saved, save present info
        if self.past[-1]['age'] >= self.past_saving_interval:
            current_info = {'age': 0, 'pos': self.position, 'vel': self.velocity}
            self.past.append(current_info)
            # print('past: ' + str(len(list(self.past))))

        # add to all items' age
        for i in range(len(self.past)):
            self.past[i]['age'] += dt



    def set_new_velocity(self, flock: list):
        in_view = [ boid for boid in flock if np.linalg.norm(np.array(boid.position) - np.array(self.position)) < self.view_range and boid != self ]
    
        past_in_view = []
        for boid in flock:
            # if boid != self:
            for past_info in boid.past:
                if (np.linalg.norm(past_info['pos'] - self.position) < self.view_range and 
                    abs(angle_between(self.velocity, past_info['pos'] - self.position)) < self.field_of_view/2): 
                    past_in_view.append(past_info)

        # calculat new velocity only if other boids/past boids are in view
        new_velocity = self.velocity
        if past_in_view:
            new_velocity += self.match_position(past_in_view) + self.match_velocity(past_in_view)        
            
        self.velocity = new_velocity + self.avoid_collision(in_view)

        # make sure boid is within speed limit, if exeeded, reset acceleration to random
        # if np.linalg.norm(self.velocity) > self.speed_cap:
            # self.velocity = self.speed_cap * self.velocity / np.linalg.norm(self.velocity)
            # self.acceleration = np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])


    def avoid_collision(self, flock: list):
        # make screen wrap around
        if self.position[0] < 0:
            self.position[0] = 640

        if self.position[1] < 0:
            self.position[1] = 480

        if self.position[0] > 640:
            self.position[0] = 0

        if self.position[1] > 480:
            self.position[1] = 0

        # avoid other boids
        other_boids = [ np.array(other.position) - np.array(self.position) for other in flock if np.linalg.norm(np.array(self.position) - np.array(other.position)) < self.collision_range]
        if other_boids:
            avoid_obs = -1 * np.mean(other_boids, axis=0)
        else:
            avoid_obs = np.array([0.0, 0.0])
        
        # normalize avoidance vector, otherwise there's less "avoidance" the closer boids are to colliding 
        if np.linalg.norm(avoid_obs) != 0:
            avoid_obs = avoid_obs / np.linalg.norm(avoid_obs)
        return self.collision_factor * avoid_obs

    def match_position(self, past_flock: list):
        towards_center = np.mean([ boid['pos'] for boid in past_flock ],  axis=0) - np.array(self.position)
        return self.match_position_factor * towards_center

    def match_velocity(self, past_flock: list):
        towards_direction = np.mean([ boid['vel'] for boid in past_flock ], axis=0) - np.array(self.velocity)
        return self.match_velocity_factor * towards_direction
