
#########################################################
#                                                       #
#   Author:  Carlos Luna-Mota (carlos.luna@mmaca.cat)   #
#   Version: 2024-01-28                                 #
#   License: The Unlicense                              #
#                                                       #
#########################################################

from pyx  import *
from math import *

### AUXILIARY FUNCTIONS ########################################################

def logarithmic_spiral(factor_per_turn, turns, points_per_turn, rotation=0):

    # Sanity checks
    assert(factor_per_turn > 0)
    assert(turns           > 0)
    assert(points_per_turn > 0)

    # Derived constants
    N = int(turns*points_per_turn) + 1
    A = 2*pi/points_per_turn
    R = (1/factor_per_turn)**(1/points_per_turn)

    # Return points
    return tuple(((R**i)*sin(A*i - rotation),
                  (R**i)*cos(A*i - rotation)) for i in range(N))


def put_text(x, y, t, s=[]):
    return (path.path(path.moveto(x-0.01,y),
                      path.lineto(x+0.01,y)),[deco.curvedtext(t)]+s)


def drawing(filename, symbol, K, angle, radii=24,
            width=210, height=297, margin=15,
            points_per_turn=360, turns=10, min_radii=5):

    # Derived constants:
    K_per_turn = K**(360/angle)
    rotation   = atan((1/K_per_turn)**(3/4)) # for a better fit in a rectangle 
    rotation   = (2*pi/radii) * round(rotation/(2*pi/radii), 0) # axis-aligned

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Scale:
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P)
    scale = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10

    # Compute Center and Extremes
    X, Y = scale*(X_max+X_min)/2, scale*(Y_max+Y_min)/2
    W, H = (width-1)/20, (height-1)/20
    X_top, Y_top = scale*X_max - X, scale*Y_max - Y, 

    # Remove points that are too close to the center:
    last_P = max(i for i in range(len(P)) if scale*hypot(*P[i]) >= min_radii/10)
    last_P = (points_per_turn*2/radii) * round(last_P*radii/2/points_per_turn,0)
    P = tuple(p for p in P[:int(max(points_per_turn+1,last_P))])

    # Setup drawing:
    CANVAS = canvas.canvas()
    BASE   = [style.linecap.round, style.linejoin.round]
    THICK  = BASE + [style.linewidth.THick]
    DASHED = BASE + [style.linestyle.dashed]
    DOTTED = BASE + [style.linestyle.dotted]
    
    # Draw Logo:
    CANVAS.fill(path.rect(X_top-3.35,Y_top-0.95, 3.35,0.95))
    CANVAS.draw(*put_text(X_top-1.65,Y_top-0.75, r"{\huge \bfseries MMACA}",
                          [color.rgb.white]))

    # Draw Info:
    info = r"{} / ${:3d}".format(symbol, angle) + r"^{\circ}$"
    CANVAS.draw(*put_text(X_top-1.65,Y_top-1.65, r"{\Large "+info+"}"))
    
    # Draw Radii:
    if   radii   <  8: R_STYLE = [BASE] * (radii+1)
    elif radii%2 == 0: R_STYLE = [BASE, DASHED] * (radii+1)
    else:              R_STYLE = [BASE] * (radii+1)

    for i,r in enumerate(R):
        CANVAS.stroke(path.path(path.moveto(-X, -Y),
                                path.lineto(scale*r[0]-X, scale*r[1]-Y)),
                                R_STYLE[i])

    # Draw Spiral:
    PATH = path.path(path.moveto(scale*P[0][0]-X, scale*P[0][1]-Y))
    for p in P[1:]: PATH.append(path.lineto(scale*p[0]-X, scale*p[1]-Y))
    CANVAS.stroke(PATH, THICK)

    # Output SVG:
    CANVAS.writeSVGfile("./SVG/" + filename)

    # Draw Paper Border:
    CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                            path.lineto( W,  H), path.lineto( W, -H),
                            path.closepath()),
                            BASE + [color.rgb.white, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./PDF/" + filename)


### MAIN #######################################################################

if __name__ == "__main__":

    # Setup LaTeX font
    text.set(text.LatexEngine)
    text.preamble(r"\renewcommand{\familydefault}{\sfdefault}")

    # Select constants
    CONSTANTS = {"2"     : (r"$2$",          2,             [90,180,270,360]),
                 "3"     : (r"$3$",          3,             [90,180,270,360]),
                 "4"     : (r"$4$",          4,             [90,180,270,360]),
                 "5"     : (r"$5$",          5,             [90,180,270,360]),
                 "E"     : (r"$e$",          e,             [90,180,270,360]),
                 "Pi"    : (r"$\pi$",        pi,            [90,180,270,360]),
                 "Root2" : (r"$\sqrt{2}$",   sqrt(2),       [90,180,270,360]),
                 "Root3" : (r"$\sqrt{3}$",   sqrt(3),       [90,180,270,360]),
                 "Root5" : (r"$\sqrt{5}$",   sqrt(5),       [90,180,270,360]),
                 "Phi"   : (r"$\phi$",       (1+sqrt(5))/2, [90,180,270,360])}                 

    # Draw spirals
    for name in CONSTANTS:
        symbol, value, angles = CONSTANTS[name]
        for a in angles:
            drawing("Spiral_{}_{:03d}".format(name, a), symbol, value, a)
            
################################################################################
