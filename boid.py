import numpy as np

# idea: imitate relative position and velocity:


class Boid():
    def __init__(self):
        self.view_range = 100
        self.collision_range = 20
        self.wall_collision_range = self.collision_range
        self.speed_cap = 100
        # set random velocity
        self.velocity = np.array([np.random.uniform(-100, 100), np.random.uniform(-100, 100)])
        # and position
        self.position = np.array([np.random.uniform(0, 640 - self.wall_collision_range), np.random.uniform(0, 480 - self.wall_collision_range)])
        # and acceleration
        self.acceleration = np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])

        self.match_position_factor = 1/40
        self.match_velocity_factor = 1/100
        self.collision_factor = 4
        self.wall_collision_boost = 10


    def move(self, dt):
        self.position = np.array(self.position) + np.array(self.velocity) * dt
        unit_velocity = np.array(self.velocity) / np.linalg.norm(self.velocity)
        self.velocity = np.array(self.velocity) + np.array([ self.acceleration[0] * unit_velocity[0], self.acceleration[1] * unit_velocity[1] ]) * dt


    def getRotation(self):
        unit_velocity = np.array(self.velocity) / np.linalg.norm(self.velocity)
        angle = np.arccos(unit_velocity[0]) * np.sign(unit_velocity[1])
        # convert from radians to negative degrees (this is what pyglet uses, I don't make the rules)
        to_return = -1 * angle * (180/np.pi)
        return to_return

    def set_new_velocity(self, flock: list):
        # get all other boids within view range
        in_view = [ boid for boid in flock if np.linalg.norm(np.array(boid.position) - np.array(self.position)) < self.view_range and boid != self ]
        
        new_velocity = np.array(self.velocity) + self.avoid_collision(in_view)
        if in_view:
            new_velocity = new_velocity + self.match_position(in_view) + self.match_velocity(in_view)

        self.velocity = new_velocity
        # make sure boid is within speed limit:
        if np.linalg.norm(self.velocity) > self.speed_cap:
            self.velocity = self.speed_cap * self.velocity / np.linalg.norm(self.velocity)
            self.acceleration = np.array([0, 0])

    def avoid_collision(self, flock: list):
        # make 100% sure nothing goes off screen
        boost = 1
        if self.position[0] < 0:
            # self.velocity[0] = -1*self.velocity[0]
            self.position[0] = 1
            boost = self.wall_collision_boost

        if self.position[1] < 0:
            # self.velocity[1] = -1*self.velocity[1]
            self.position[1] = 1
            boost = self.wall_collision_boost

        if self.position[0] > 640:
            # self.velocity[0] = -1*self.velocity[0]
            self.position[0] = 640 - 1
            boost = self.wall_collision_boost

        if self.position[1] > 480:
            # self.velocity[1] = -1*self.velocity[1]
            self.position[1] = 480 - 1
            boost = self.wall_collision_boost

        # if should_return:
            # return np.array([0, 0])


        # avoid other boids
        other_boids = [ np.array(other.position) - np.array(self.position) for other in flock if np.linalg.norm(np.array(self.position) - np.array(other.position)) < self.collision_range]
        if other_boids:
            avoid_obs = -1 * np.mean(other_boids, axis=0)
        else:
            avoid_obs = np.array([0.0, 0.0])
        # avoid edges of screen
        if self.position[0] < 0 + self.wall_collision_range:
            avoid_obs -= np.array([-1*self.position[0], 0])

        if self.position[1] < 0 + self.wall_collision_range:
            avoid_obs -= np.array([0, -1*self.position[1]])

        if self.position[0] > 640 - self.wall_collision_range:
            avoid_obs -= np.array([640 - self.position[0], 0])

        if self.position[1] > 480 - self.wall_collision_range:
            avoid_obs -= np.array([0, 480 - self.position[1]])
        
        # normalize avoidance vector, otherwise there's less "avoidance" the closer boids are to colliding 
        if np.linalg.norm(avoid_obs) != 0:
            avoid_obs = avoid_obs / np.linalg.norm(avoid_obs)
        return self.collision_factor * avoid_obs * boost

    def match_position(self, flock: list):
        towards_center = np.mean([ boid.position for boid in flock ],  axis=0) - np.array(self.position)
        return self.match_position_factor * towards_center

    def match_velocity(self, flock: list):
        towards_direction = np.mean([ boid.velocity for boid in flock ], axis=0) - np.array(self.velocity)
        return self.match_velocity_factor * towards_direction