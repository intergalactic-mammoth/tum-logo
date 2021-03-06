from phi.flow import *
import pylab
import time
import os

#TODO: Change this accordingly
scene = Scene.create('/home/intergalactic-mammoth/FILES/UNI/TUM/HiWi-Thurey/TUM_Logo/phiflow/scene')
savedir = 'imgs/scene_%d/'

num = 0

while True:    
    
    if not os.path.exists(savedir%(num)):
        os.mkdir(savedir%(num))
        break
    else:
        num = num + 1
        if not os.path.exists(savedir%(num)):
            os.mkdir(savedir%(num))
            break


res = 128
rt = 4      #inflow rate
bf = 0.05    #buoyancy factor
frames = 100
step_sz = 0.5
obs = 0
speed = 0.035

def T_inflow(time):

    val = 0.3*res+res*(time*speed)

    threshold = 0.6*res 

    if val < threshold:
        return Sphere([0.8*res, val], radius = 0.0125*res)
    else:
        return Sphere([0.8*res-0.02*res*(time*speed), threshold], radius = 0.0125*res)

def M_inflow(time):

    #movement of flow in X dir
    valX = 1.1*res-0.015*res*(time*speed*8)
    
    #movement of flow in Y dir
    valY = 0.2*res + res*(time*speed)

    threshold = 0.8*res 

    if valY < threshold:
        return Sphere([valY, 1.1*res], radius = 0.0125*res)
    else:
        return Sphere([threshold, valX], radius = 0.0125*res)

world = World()
fluid = world.add(Fluid(Domain([res, int(1.5*res)], boundaries=OPEN), velocity=3.0, buoyancy_factor=bf), physics=IncompressibleFlow())
world.add(Inflow(T_inflow(0), rate = rt), physics=GeometryMovement(T_inflow))
world.add(Inflow(M_inflow(0), rate = rt), physics=GeometryMovement(M_inflow))


if obs:
    world.add(Obstacle(Sphere(center=[0.7*res,0.5*res], radius=0.0625*res)))

for frame in range(frames):
    
    start = time.time()
    world.step(dt=step_sz)
    end = time.time()
    print('Step %d done, %.3f seconds elapsed' % (frame, end-start))

    pylab.imshow(np.concatenate(fluid.density.data[...,0], axis=1), origin='lower', cmap='magma')
    plt_name = 'frame%d_bf%d_rt%d_dt%d'
    save_name = savedir + plt_name + '.png'
    pylab.savefig(save_name % (num, frame, bf*10, rt*10, step_sz*100), bbox_inches='tight')
    pylab.show()


print('Exiting simulation...')
