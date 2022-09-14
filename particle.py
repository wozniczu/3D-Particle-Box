import numpy as np
import mayavi.mlab as mlab

from traits.api import HasTraits, Range, Instance, \
        on_trait_change
from traitsui.api import View, Item, Group

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, \
                MlabSceneModel

h = 6,63*10**(-34)

def cube_faces(xmin, xmax, ymin, ymax, zmin, zmax):
    faces = []

    x,y = np.mgrid[xmin:xmax:3j,ymin:ymax:3j]
    z = np.ones(y.shape)*zmin
    faces.append((x,y,z))

    x,y = np.mgrid[xmin:xmax:3j,ymin:ymax:3j]
    z = np.ones(y.shape)*zmax
    faces.append((x,y,z))

    x,z = np.mgrid[xmin:xmax:3j,zmin:zmax:3j]
    y = np.ones(z.shape)*ymin
    faces.append((x,y,z))

    x,z = np.mgrid[xmin:xmax:3j,zmin:zmax:3j]
    y = np.ones(z.shape)*ymax
    faces.append((x,y,z))

    y,z = np.mgrid[ymin:ymax:3j,zmin:zmax:3j]
    x = np.ones(z.shape)*xmin
    faces.append((x,y,z))

    y,z = np.mgrid[ymin:ymax:3j,zmin:zmax:3j]
    x = np.ones(z.shape)*xmax
    faces.append((x,y,z))

    return faces

def Energy(nx, ny, nz):
    return (h^2/(8*m))*(nx^2/a^2+ny^2/b^2+nz^2/c^2)

def mlab_plt_cube(xmin,xmax,ymin,ymax,zmin,zmax):
    faces = cube_faces(xmin,xmax,ymin,ymax,zmin,zmax)
    for grid in faces:
        x,y,z = grid
        mlab.mesh(x,y,z,opacity=0.1)

class MyModel(HasTraits):

    nx = Range(1, 10, 1)
    ny = Range(1, 10, 1)
    nz = Range(1, 10, 1)
    a = 100
    b = 100
    c = 100

    scene = Instance(MlabSceneModel, ())
    plot = Instance(PipelineBase)
    plot2 = Instance(PipelineBase)

    @on_trait_change('nx,ny,nz,scene.activated')
    def update_plot(self):
        mlab.clf()
        p, q, r = (self.nx, self.ny, self.nz)
        a, b, c = (self.a, self.b, self.c)

        x = np.arange(a)
        y = np.arange(b)
        z = np.arange(c)

        xx, yy, zz = np.meshgrid(x, y, z)

        self.plot = mlab.contour3d(abs((np.sqrt(8/(a*b*c))*np.sin((p*np.pi*xx)/a))*(np.sin((q*np.pi*yy)/b))*(np.sin((r*np.pi*zz)/c)))**2, contours=6, transparent=True, name = 'Particle in 3D box')
        mlab.axes(x_axis_visibility=True, y_axis_visibility=True, z_axis_visibility=True)
        self.plot2 = mlab_plt_cube(0,a,0,b,0,c)

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=800, width=1000, show_label=False),
                Group(
                        'nx', 'ny','nz'
                     ),
                resizable=True,
                )

def main():
    my_model = MyModel()
    my_model.configure_traits()

if __name__ == "__main__":
    main()