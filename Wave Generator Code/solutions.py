import numpy as np 


def calculation(b,wavelength, A):
    theta = np.pi/4
    H = A*2
    waterdepth = 0.14 #h, d in paper
    if theta >= wavelength/(np.pi*H):
        print("Outside of parameters")
        exit() 
    if ((H*wavelength) / (2*np.pi*np.tan(theta))) >= (waterdepth**2 - b**2):
        print("Outside of parameteres 2")
        exit()
    if ((H*wavelength) / (2*np.pi*np.tan(theta))) >= b**2
        print("Outside of parameters 3")
        exit()
    
    



    




calculation(0.025, 0.04, 0.01)


    
