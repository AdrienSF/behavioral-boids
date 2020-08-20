# behavioral boids
The boids algorithm manages to simulate flocking behavior by making each boid follow only a few simple rules:
- Match the position of other boids
- Match the velocity of other boids
- avoid colliding with other boids
 
Matching the position and velocity of other boids is in a sense imitating the behavior of boids around it. In this project I try to extend this concept of imitating behavior: what happens if boids try to match acceleration instead of velocity? what if boids imitate the reaction other boids have in relation to their surroundings? There are many properties of a boid that can be imitated.
 
The master branch consists of a basic implementation of the boids algorithm, and each branch involves the imitation of a different aspect of behavior.
 
 
## Master branch
I followed [this pseudocode](http://www.vergenet.net/~conrad/boids/pseudocode.html) to build a basic implementation of the boids algorithm. For most weights, the boids gradually find a stable position and eventually stop moving all together apart from minor perturbations, which is evidently not the type of flocking behavior this algorithm is intended to simulate. I have not found a weight configuration that results in the conventional boids algorithm flocking behavior. With the current weight configuration, the boids resemble a cloud of insects.
 
## Accelerate branch
In this branch, each boid imitates the acceleration vector of the boids around it, instead of the velocity vector. This implementation actually results in a flocking behavior more typical of the boids algorithm than the basic master branch implementation. In the current weight configuration, it is easy to observe sudden changes in direction and speed that resemble flocking behavior of small and agile animals. If the match_acceleration weight is set to be negligibly small, the boids exhibit an "orbiting" behavior around the flock's center of mass. The moon orbiting the earth is constantly accelerating towards the earth, similarly the boids are continuously accelerating towards the center of mass of the flock. Furthermore, the boids try to avoid collision, which keeps them from all collapsing into a single point.
<!--
-noticed distinct fractale-like empty circles when frame by frame with 100 boids
-->

## Past branch
The idea here is for each boid to imitate the past velocity and position of other boids. This implementation is inspired by the behavior of ants: each boid leaves a "chemical trail" that holds information on the position and velocity of the boid at any given time. When a boid sees part of a "chemical trail" it starts to copy the position and velocity information left behind by the boid making the trail. On this branch, boids have not only a limited view range, but also a limited field of view (boids only see things in front of them). As one might expect, this implementation results in ant-like behavior. The boids slowly converge onto distinct paths, and these paths evolve over time. Sometimes bends in the path shift, sometimes the path breaks (the "chemical trails" eventually expire), and in general the paths smooth themselves out over time.

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
 
## Installation
After cloning this repository, you will need to install the pyglet and numpy python libraries to run this code.
 
## Usage
Run the main.py python script to test out this project. Parameters and weights can be tweaked in the boid.py class file.
