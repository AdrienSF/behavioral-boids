## Movement-func branch
In the boids algorithm, each boid's velocity is a function of their current velocity, the mean velocity of the boids around it, and the mean position of the boids around it. The boids algorithm uses a specific function to produce flocking behaviour, but what if each boid starts with a random function? In this branch, each boid copies this function from the boids around it, adding it to its own.
 
Every boid starts with a random function of this form:<br>
new_velocity = self.velocity + A × flock.velocity + B × flock.relative_position + C
 
Where A, B and C are vector constants randomly generated on creation of each boid.
 
Each boid imitates the movement function of the boids around it in the following manner:<br>
new_func = old_func + weight × flock_func
 
This abstraction of the boids algorithm leads to interesting results: no matter what random functions the boids start with, they always seem to eventually display some form of organized behavior despite the fact that no such behavior has been explicitly coded. I've identified a few types of organized behavior that boids seem to tend towards:
 
- flocking: boids form groups that move together within view range of each other.
- mutual avoidance: each boid stays just out of view range of other boids, to maintain this all boids have almost identical mean velocities. (view low, A high)
- consistent flight paths: all boids repeatedly follow the same (or a few different) flight path(s). An example of this would be all boids moving along the same line continuously (possibly in opposite directions), or all boids consistently moving downwards.
 
Sometimes a combination of these behaviors is observed.
 
Remaining in close proximity of other boids is indirectly encouraged: boids that stay close together have more time to copy each other's movement function, starting a positive feedback loop. This can explain the flocking behavior. Boids with movement functions that happen to lead to flocking remain in close proximity. Consequently, any non-flocking boid that passes by will quickly copy flocking behavior whereas the flocking boids will not easily copy the non-flocking behavior. Indeed, boids copy the mean movement function of the boids around them, and one non-flocking boid flying through a flock will not affect this mean very much.<br>
Flocking behavior seems to occur more when the view range of each boid is high, and the velocity coefficient A is low.
 
Since each boid starts with a random movement function, when one boid sees another it starts moving in a random direction. Of course, there are more such random directions that lead away from the boid than close to it. Since the movement functions are uniformly distributed, boids will avoid each other in most cases. However, once the boid is out of view, the first boid will resume its original behavior, leading the second boid right back into its field of view. The process thus repeats indefinitely, explaining the mutual avoidance behavior.
 
Regarding the observed behavior of consistent flight paths, I have no compelling hypothesis or comprehensive explanation. I am similarly perplexed regarding another observation: in all instances of this program I have seen, the boids match each other's mean velocity. I've not explicitly coded such behavior, yet the boids always somehow "learn" to match each other's velocity despite starting with random movement functions. By commenting out calls to set_new_coefs() it is easy to see that organized behavior does not arise without the "imitation" property of the boids. I find it remarkable that in this case, order arises from chaos simply due to the property of imitation, without the presence of something orderly to imitate initially.