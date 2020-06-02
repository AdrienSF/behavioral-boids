import pyglet
from boid import Boid

window = pyglet.window.Window()


# arrow_image = pyglet.image.load('arrow.png')
# create boids
boids = []
for i in range(50):
    boids.append(Boid())

# create points
batch = pyglet.graphics.Batch()
vertex_list = []
for point_boid in boids:
    vertex_list.append( batch.add(1, pyglet.gl.GL_POINTS, None,
                ('v2f', tuple(point_boid.position))
            ))

# print([ list(pyglet_obj.vertices) for pyglet_obj in vertex_list])

def move_boids(dt):
    for i in range(len(boids)):
        # use a 100 x smaller timestep to ensure colisions are handled properly. 
        # This shouldn't be computationally very difficult.. except it is!?
        # for t in range(100):
        boids[i].move(dt)
        boids[i].set_new_acceleration(boids)
        # set points to be at the same position as the boid objects
        vertex_list[i].vertices = list(boids[i].position)
    # print('moved all boids')




@window.event
def on_draw():
    window.clear()
    batch.draw()



pyglet.clock.schedule_interval(move_boids, 1/120.0)
pyglet.app.run()