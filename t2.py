import numpy
import scipy
import scipy.special
import scipy.ndimage

from clean import *
from synthesis import *
from simulate import *

from matplotlib import pylab
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D

def aaf_ns(a, m, c):
    """

    """
    r=numpy.hypot(*ucs(a))
    return scipy.special.pro_ang1(m,m,c,r)



if 1:
    vlas=numpy.genfromtxt("/home/vlad/software/SKA/crocodile/test/VLA_A_hor_xyz_5ants.txt", delimiter=",")
    pyplot.scatter(vlas[:,0], vlas[:,1])
    pyplot.title('Antenna positions on the (X,Y) plane')
    pyplot.xlabel('X, meters')
    pyplot.ylabel('Y, meters')
    pyplot.show()
#    raw_input("press enter")

    uvstep = 0.1
    wl = 5.0
    vobs=genuv(vlas, numpy.arange(0,numpy.pi,uvstep) ,  numpy.pi/2.0)
    pyplot.cla()
    pyplot.scatter(vobs[:,0]/wl, vobs[:,1]/wl)
    pyplot.title('UV plane coverage for 12h observation, wavelength = 5m')
    pyplot.xlabel('U, number of wavelengths')
    pyplot.ylabel('V, number of wavelengths')
    pyplot.show()
#    raw_input("press enter")

    yy=genvis(vobs/wl, 0.01, 0.01)
    yy=yy + genvis(vobs/wl, -0.01, -0.01)

# Fill the conjugated part V(-u,-v) = V*(u,v)
    vobs_tmp = numpy.copy(vobs)
    vobs_tmp[:,0] *= -1.0
    vobs_tmp[:,1] *= -1.0
    vobs_new = numpy.concatenate((vobs, vobs_tmp))
    pyplot.cla()
    pyplot.scatter(vobs_new[:,0]/wl, vobs_new[:,1]/wl)
    pyplot.title('UV plane coverage for 12h observation with Hermitian part')
    pyplot.xlabel('U, number of wavelengths')
    pyplot.ylabel('V, number of wavelengths')
    pyplot.show()
#    raw_input("press enter")

    yy_tmp = numpy.conjugate(yy)
    yy_new = numpy.concatenate((yy, yy_tmp))

    nmat = 512
    mat_a = numpy.zeros((nmat,nmat),'D')
    maxvobs = max(vobs_new[:,0:1])[0] + 1
    mat_a = grid1(mat_a,(vobs_new/maxvobs),yy_new)
    pyplot.cla()
    pyplot.contour(numpy.abs(mat_a))
    pyplot.title('Module of visibility V(u,v) resampled to the matrix')
    pyplot.xlabel('U, number of pixel')
    pyplot.ylabel('V, number of pixel')
    pyplot.colorbar(label='abs(V(u,v)')
    pyplot.show()
#    raw_input("press enter")


#    pyplot.cla()
#    pyplot.imshow(numpy.abs(mat_a))
#    pyplot.show()
#    raw_input("press enter")

    mat_b = numpy.fft.ifftshift(mat_a)
    pyplot.cla()
    pyplot.contour(numpy.abs(mat_b))
    pyplot.title('Module of V(u,v) resampled to the matrix after FFTSHIFT')
    pyplot.xlabel('U, number of pixel')
    pyplot.ylabel('V, number of pixel')
    pyplot.colorbar(label='abs(V(u,v)')
    pyplot.show()
#    raw_input("press enter")

    c = numpy.fft.ifft2(mat_b)
    c1 = numpy.fft.fftshift(c)
    pyplot.cla()
    pyplot.contour(numpy.abs(c1))
    pyplot.title('Dirty image of the two point sources recovered')
    pyplot.xlabel('l, number of pixel')
    pyplot.ylabel('m, number of pixel')
    pyplot.show()
#    raw_input("press enter")
    


    ncomp = 4
    c2 = scipy.ndimage.gaussian_filter(abs(c1), ncomp)
    c3 = c2[::ncomp,::ncomp]
    X = numpy.arange(1, nmat/ncomp)
    Y = numpy.arange(1, nmat/ncomp)
    X, Y = numpy.meshgrid(X, Y)
    Z = c3[X,Y]
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot', linewidth=0, antialiased=False)
#    ax.set_zlim(-1.01, 1.01)

    fig.colorbar(surf, shrink=0.5, aspect=5, label='I(l,m), amplitude')
    pyplot.title('3D surface of the dirty image recovered (smoothed)')
    pyplot.xlabel('l, number of pixel')
    pyplot.ylabel('m, number of pixel')
   # pyplot.zlabel('I(l,m), amplitude')
 
    pyplot.show()

if 0:
    majorcycle(0.025, 15000, vobs/5 , yy, 0.1, 5, 100, 250000)
    

if 0: # some other testing code bits
    mg=exmid(numpy.fft.fftshift(numpy.fft.fft2(aaf(a, 0, 3))),5)
    ws=numpy.arange( p[:,2].min(), p[:,2].max(), wstep)
    wr=zip(ws[:-1], ws[1:]) + [ (ws[-1], p[:,2].max() ) ]
    yy=genvis(vobs/5, 0.001, 0.001)
    d,p=doimg(0.025, 15000, vobs/5, yy, lambda *x: wslicimg(*x, wstep=250))
    pylab.matshow(p[740:850,740:850]); pylab.colorbar(); pylab.show()
    x=numpy.zeros_like(d)
    x[1050,1050]=1
    xuv=numpy.fft.fftshift(numpy.fft.fft2(numpy.fft.ifftshift(x)))
