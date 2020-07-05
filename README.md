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
 
## Installation
After cloning this repository, you will need to install the pyglet and numpy python libraries to run this code.
 
## Usage
Run the main.py python script to test out this project. Parameters and weights can be tweaked in the boid.py class file.
