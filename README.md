# behavioral boids
The boids algorithm manages to simulate flocking behavior by making each boid follow only a few simple rules:
- Match the position of other boids
- Match the velocity of other boids
- avoid colliding with other boids

Matching the position and velocity of other boids is in a sense imitating the behavior of boids around it. In this project I try to extend this concept of imitating behavior: what happens if boids try to match acceleration instead of velocity? what if boids imitate the reaction other boids have in relation to their surroundings? There are many properties of a boid that can be imitated.

The master branch consists of a basic implementation of the boids algorithm, and each branch involves the imitation of a different aspect of behavior.


# Master branch
This is a basic implementation of the boids algorithm. For most weights, the boids gradually find a stable position and eventually stop moving all together apart from minor perturbations, which is evidently not the type of flocking behavior this algorithm is intended to simulate. I have not found a weight configuration that results in the conventional boids algorithm flocking behavior. With the current weight configuration, the boids resemble a cloud of insects.

# Accelerate branch
In this branch, each boid imitates the acceleration vector of the boids around it, instead of the velocity vector. This implementation actually results in a flocking behavior more typical of the boids algorithm than the basic master branch implementation. In the current weight configuration, it is easy to observe sudden changes in direction and velocity that resemble flocking behavior of small and agile animals. If the match_acceleration weight is set to be negligibly small, the boids exhibit an "orbiting" behavior around the flock's center of mass. The moon orbiting the earth is constantly accelerating towards the earth, similarly the boids are continuously accelerating towards the center of mass of the flock. Furthermore, the boids try to avoid collision, which keeps them from all collapsing into a single point.

<!--
-noticed distinct fractale-like empty circles when frame by frame with 100 boids
 Installation
 Usage
Project status
 -->
