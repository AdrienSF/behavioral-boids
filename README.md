## ?? branch
In the boids algorithm, each boid's velocity is a function of their current velocity, the mean velocity of the boids around it, and the mean position of the boids around it. The boids algorithm uses a specific function to produce flocking behaviour, but what if each boid starts with a random function? In this branch, each boid copies this function from the boids around it, adding it to it's own. What will happen...?

I'm sticking with linear functions for now:

velocity = A*self.velocity + B*flock.velocity + C*flock.relative_position

new_func = old_func + weight * flock_func
