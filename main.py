import pyglet
from boid import Boid

window = pyglet.window.Window()

# create boids
boids = []
for i in range(30):
    boids.append(Boid())

# create points
batch = pyglet.graphics.Batch()
vertex_list = []
for point_boid in boids:
    vertex_list.append( batch.add(1, pyglet.gl.GL_POINTS, None,
                ('v2f', tuple(point_boid.position))
            ))


def move_boids(dt):
    for i in range(len(boids)):
        boids[i].move(dt)
        boids[i].set_new_velocity(boids)
        # set points to be at the same position as the boid objects
        vertex_list[i].vertices = list(boids[i].position)


@window.event
def on_draw():
    window.clear()
    batch.draw()


# call move_boids 120 a second
pyglet.clock.schedule_interval(move_boids, 1/120.0)
pyglet.app.run()