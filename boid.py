import numpy as np

# idea: imitate relative position and velocity:


class Boid():
    def __init__(self):
        self.view_range = 100
        self.colision_range = 20
        self.wall_colision_range = 40
        # set random velocity
        self.velocity = np.array([np.random.uniform(-100, 100), np.random.uniform(-100, 100)])
        # and position
        self.position = np.array([np.random.uniform(0, 640 - self.wall_colision_range), np.random.uniform(0, 480 - self.wall_colision_range)])

        self.match_position_factor = 1
        self.match_velocity_factor = 1/10
        self.colision_factor = 10
        # self.speed = 10


    def move(self, dt):
        self.position = np.array(self.position) + np.array(self.velocity) * dt
        # print(str(self.velocity) + " |   | " + str(self.getRotation()))


    def getRotation(self):
        unit_velocity = np.array(self.velocity) / np.linalg.norm(self.velocity)
        angle = np.arccos(unit_velocity[0]) * np.sign(unit_velocity[1])
        # convert from radians to negative degrees (this is what pyglet uses, I don't make the rules)
        to_return = -1 * angle * (180/np.pi)
        return to_return

    def set_new_velocity(self, flock: list):
        # get all other boids within view range
        in_view = [ boid for boid in flock if np.linalg.norm(np.array(boid.position) - np.array(self.position)) < self.view_range and boid != self ]
        if in_view:
            new_velocity = np.array(self.velocity) + self.match_position(in_view) + self.avoid_colision(in_view) + self.match_velocity(in_view)
        else:
            new_velocity = np.array(self.velocity) + self.avoid_colision(in_view)

        # self.velocity = self.speed * new_velocity / np.linalg.norm(new_velocity)
        self.velocity = new_velocity

    def avoid_colision(self, flock: list):
        # make 100% sure nothing goes off screen
        if self.position[0] < 0:
            self.velocity[0] = 0
            self.position[0] = 1

        if self.position[1] < 0:
            self.velocity[1] = 0
            self.position[1] = 1

        if self.position[0] > 640:
            self.velocity[0] = 0
            self.position[0] = 640 - 1

        if self.position[1] > 480:
            self.velocity[1] = 0
            self.position[1] = 480 - 1

        # avoid other boids
        other_boids = [ np.array(other.position) - np.array(self.position) for other in flock if np.linalg.norm(np.array(self.position) - np.array(other.position)) < self.colision_range]
        if other_boids:
            avoid_obs = -1 * np.mean(other_boids, axis=0)
        else:
            avoid_obs = np.array([0.0, 0.0])
        # avoid edges of screen
        if self.position[0] < 0 + self.wall_colision_range:
            avoid_obs -= np.array([-1*self.position[0], 0])

        if self.position[1] < 0 + self.wall_colision_range:
            avoid_obs -= np.array([0, -1*self.position[1]])

        if self.position[0] > 640 - self.wall_colision_range:
            avoid_obs -= np.array([640 - self.position[0], 0])

        if self.position[1] > 480 - self.wall_colision_range:
            avoid_obs -= np.array([0, 480 - self.position[1]])

        # print(avoid_obs)
        return self.colision_factor * avoid_obs# - np.array([self.colision_range, self.colision_range]))

    def match_position(self, flock: list):
        towards_center = np.mean([ boid.position for boid in flock ],  axis=0) - np.array(self.position)
        return self.match_position_factor * towards_center

    def match_velocity(self, flock: list):
        towards_direction = np.mean([ boid.velocity for boid in flock ], axis=0) - np.array(self.velocity)
        return self.match_velocity_factor * towards_direction