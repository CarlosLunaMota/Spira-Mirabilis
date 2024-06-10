
#########################################################
#                                                       #
#   Author:  Carlos Luna-Mota (carlos.luna@mmaca.cat)   #
#   Version: 2024-06-10                                 #
#   License: The Unlicense                              #
#                                                       #
#########################################################

from pyx  import *
from math import *

### AUXILIARY FUNCTIONS ########################################################

def get_rectangle(A,B, ratio):
    v = (B[1]-A[1],A[0]-B[0])
    k = ratio #/ hypot(*v)
    C = (B[0] + k*v[0], B[1] + k*v[1])
    D = (A[0] + k*v[0], A[1] + k*v[1])
    return (A,B,C,D)
    
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

def template(filename, symbol, K, angle, radii=24,
            width=210, height=297, margin=15,
            points_per_turn=360, turns=10, min_radii=5):

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.white, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_00(rectangle_style, input_style, output_style):
    """
    Frontpage Logo
    """

    filename        = "Example_00"
    symbol          = r"$\phi$"
    K               = (1+sqrt(5))/2
    angle           = 90

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.white, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_00b(rectangle_style, input_style, output_style):
    """
    Frontpage Logo
    """

    filename        = "Example_00b"
    symbol          = r"$\phi$"
    K               = (1+sqrt(5))/2
    angle           = 90

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    #if margin:
    #    CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
    #                            path.lineto( W,  H), path.lineto( W, -H),
    #                            path.closepath()),
    #                            BASE + [color.rgb.white, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_01(rectangle_style, input_style, output_style):
    """
    Un full de paper de mida A7 encaixa a l'espiral √2/270°.
    Quines són les proporcions d'aquest full?
    """

    filename        = "Example_01"
    symbol          = r"$\sqrt{2}$"
    K               = sqrt(2)
    angle           = 270

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((scale*RR[5][0]-X,scale*RR[5][1]-Y),
                            (              -X,              -Y),
                            1/sqrt(2))

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    CANVAS.stroke(path.circle(C[0], C[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), output_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_02(rectangle_style, input_style, output_style):
    """
    Un full de paper de mida A7 encaixa a l'espiral √2/90°.
    Quines són les proporcions d'aquest full?
    """

    filename        = "Example_02"
    symbol          = r"$\sqrt{2}$"
    K               = sqrt(2)
    angle           = 90

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((              -X,              -Y),
                            (scale*RR[9][0]-X,scale*RR[9][1]-Y),
                            1/sqrt(2))

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(D[0], D[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), output_style)
        
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_03(rectangle_style, input_style, output_style):
    """
    Divideix un rectangle en 3 parts iguals amb l'ajuda de l'espiral 3/360°.
    Fes-ho també amb l'ajuda de l'espiral 4/360°
    """

    filename        = "Example_03"
    symbol          = r"$3$"
    K               = 3
    angle           = 360

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((              -X,              -Y),
                            (scale*RR[3][0]-X,scale*RR[3][1]-Y),
                            1/2)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(scale*RR[27][0]-X, scale*RR[27][1]-Y, 0.25),
                              output_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_04(rectangle_style, input_style, output_style):
    """
    Divideix un rectangle en 3 parts iguals amb l'ajuda de l'espiral 3/360°.
    Fes-ho també amb l'ajuda de l'espiral 4/360°
    """

    filename        = "Example_04"
    symbol          = r"$4$"
    K               = 4
    angle           = 360

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((scale*RR[14][0]-X,scale*RR[14][1]-Y),
                            (scale*RR[26][0]-X,scale*RR[26][1]-Y),
                            1/2)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(-X, -Y, 0.25), output_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_05(rectangle_style, input_style, output_style):
    """
    Crea un rectangle de proporcions 1:√2 amb ajuda de l'espiral 4/360°
    """

    filename        = "Example_05"
    symbol          = r"$4$"
    K               = 4
    angle           = 360

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((scale*RR[26][0]-X,scale*RR[26][1]-Y),
                            (-X,-Y),
                            sqrt(2))

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(scale*RR[20][0]-X, scale*RR[20][1]-Y, 0.25),
                              output_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_06(rectangle_style, input_style, output_style):
    """
    Comprova quines són les proporcions dels catets d'un escaire
    amb l'ajuda de l'espiral √3/270°
    """

    filename        = "Example_06"
    symbol          = r"$\sqrt{3}$"
    K               = sqrt(3)
    angle           = 270

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((scale*RR[1][0]-X,scale*RR[1][1]-Y),
                            (-X,-Y),
                            1/sqrt(3))

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            #path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    CANVAS.stroke(path.circle(C[0], C[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25),
                              output_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_07(rectangle_style, input_style, output_style):
    """
    Comprova quina relació hi ha entre la diagonal i el costat d'un quadrat
    amb l'ajuda de l'espiral 2/90°
    """

    filename        = "Example_07"
    symbol          = r"$2$"
    K               = 2
    angle           = 90

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((scale*RR[8][0]-X,scale*RR[8][1]-Y),
                            (-X,-Y),
                            1)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(D[0], D[1], 0.25), output_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_08(rectangle_style, input_style, output_style):
    """
    Comprova que les targetes de crèdit tenen són rectangles auris
    amb l'ajuda de l'espiral Phi/270°
    """

    filename        = "Example_08"
    symbol          = r"$\phi$"
    K               = (1+sqrt(5))/2
    angle           = 270

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((scale*RR[15][0]-X,scale*RR[15][1]-Y),
                            (-X,-Y),
                            1/K)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(C[0], C[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), output_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_09(rectangle_style, input_style, output_style):
    """
    Divideix un segment en proporció àuria amb l'ajuda de l'espiral Phi/360°
    Fes-ho també amb l'ajuda de l'espiral Phi/180°
    """

    filename        = "Example_09"
    symbol          = r"$\phi$"
    K               = (1+sqrt(5))/2
    angle           = 360

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((              -X,              -Y),
                            (scale*RR[4][0]-X,scale*RR[4][1]-Y),
                            1/2)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(scale*RR[28][0]-X, scale*RR[28][1]-Y, 0.25),
                              output_style)    
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_10(rectangle_style, input_style, output_style):
    """
    Divideix un segment en proporció àuria amb l'ajuda de l'espiral Phi/360°
    Fes-ho també amb l'ajuda de l'espiral Phi/180°
    """

    filename        = "Example_10"
    symbol          = r"$\phi$"
    K               = (1+sqrt(5))/2
    angle           = 180

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((scale*RR[28][0]-X,scale*RR[28][1]-Y),
                            (scale*RR[16][0]-X,scale*RR[16][1]-Y),
                            1/3)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(-X, -Y, 0.25), output_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_11(rectangle_style, input_style, output_style):
    """
    Comprova que l'espiral de Fibonacci és una bona aproximació
    de l'espiral Phi/90°
    """

    filename        = "Example_11"
    symbol          = r"$\phi$"
    K               = (1+sqrt(5))/2
    angle           = 90

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw Fibonacci Spiral
    LAMBDA = 0.8
    ALPHA  = 90 *pi/180
    F = [None] * 18
    F[0] = (0,0)
    F[1] = (LAMBDA*cos(ALPHA), LAMBDA*sin(ALPHA))
    A,B,F[ 2],F[ 3] = get_rectangle(F[ 0], F[ 1], -1)
    A,B,F[ 4],F[ 5] = get_rectangle(F[ 0], F[ 3], -1)
    A,B,F[ 6],F[ 7] = get_rectangle(F[ 1], F[ 5], -1)
    A,B,F[ 8],F[ 9] = get_rectangle(F[ 2], F[ 7], -1)
    A,B,F[10],F[11] = get_rectangle(F[ 4], F[ 9], -1)
    A,B,F[12],F[13] = get_rectangle(F[ 6], F[11], -1)
    A,B,F[14],F[15] = get_rectangle(F[ 8], F[13], -1)
    A,B,F[16],F[17] = get_rectangle(F[10], F[15], -1)

    LINES = ((17,16),(16,14),(14,12),(17,12),(10,15),
             (8,13),(6,11),(4,9),(2,7),(1,5),(0,3))

    XX = X - 0.1
    YY = Y + 0.4

    CANVAS.stroke(path.path(path.moveto(F[17][0]-XX, F[17][1]-YY),
                            path.lineto(F[16][0]-XX, F[16][1]-YY),
                            path.lineto(F[14][0]-XX, F[14][1]-YY),
                            path.lineto(F[12][0]-XX, F[12][1]-YY),
                            path.closepath()),
                            rectangle_style)

    for A,B in LINES:
        CANVAS.stroke(path.path(path.moveto(F[A][0]-XX, F[A][1]-YY),
                                path.lineto(F[B][0]-XX, F[B][1]-YY)),
                                output_style + [style.linewidth.THIck,
                                                style.linestyle.dashed])

    ARCS = ()

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

    # Draw INPUT:
    #for f in F: CANVAS.stroke(path.circle(f[0]-X, f[1]-Y, 0.25), input_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_11b(rectangle_style, input_style, output_style):
    """
    Comprova que l'espiral de Fibonacci és una bona aproximació
    de l'espiral Phi/90°
    """

    filename        = "Example_11b"
    symbol          = r"$\phi$"
    K               = (1+sqrt(5))/2
    angle           = 90

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw Fibonacci Spiral
    LAMBDA = 0.8
    ALPHA  = 90 *pi/180
    F = [None] * 18
    F[0] = (0,0)
    F[1] = (LAMBDA*cos(ALPHA), LAMBDA*sin(ALPHA))
    A,B,F[ 2],F[ 3] = get_rectangle(F[ 0], F[ 1], -1)
    A,B,F[ 4],F[ 5] = get_rectangle(F[ 0], F[ 3], -1)
    A,B,F[ 6],F[ 7] = get_rectangle(F[ 1], F[ 5], -1)
    A,B,F[ 8],F[ 9] = get_rectangle(F[ 2], F[ 7], -1)
    A,B,F[10],F[11] = get_rectangle(F[ 4], F[ 9], -1)
    A,B,F[12],F[13] = get_rectangle(F[ 6], F[11], -1)
    A,B,F[14],F[15] = get_rectangle(F[ 8], F[13], -1)
    A,B,F[16],F[17] = get_rectangle(F[10], F[15], -1)

    LINES = ((17,16),(16,14),(14,12),(17,12),(10,15),
             (8,13),(6,11),(4,9),(2,7),(1,5),(0,3))

    XX = X - 0.1
    YY = Y + 0.4

    #CANVAS.stroke(path.path(path.moveto(F[17][0]-XX, F[17][1]-YY),
    #                        path.lineto(F[16][0]-XX, F[16][1]-YY),
    #                        path.lineto(F[14][0]-XX, F[14][1]-YY),
    #                        path.lineto(F[12][0]-XX, F[12][1]-YY),
    #                        path.closepath()),
    #                        rectangle_style)

    for A,B in LINES:
        CANVAS.stroke(path.path(path.moveto(F[A][0]-XX, F[A][1]-YY),
                                path.lineto(F[B][0]-XX, F[B][1]-YY)),
                                output_style + [style.linewidth.THICK,
                                                style.linestyle.dashed])

    ARCS = ()

    # Draw Logo:
    #CANVAS.fill(path.rect(X_top-3.35,Y_top-0.95, 3.35,0.95))
    #CANVAS.draw(*put_text(X_top-1.65,Y_top-0.75, r"{\huge \bfseries MMACA}",
    #                      [color.rgb.white]))

    # Draw Info:
    #info = r"{} / ${:3d}".format(symbol, angle) + r"^{\circ}$"
    #CANVAS.draw(*put_text(X_top-1.65,Y_top-1.65, r"{\Large "+info+"}"))
    
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

    # Draw INPUT:
    #for f in F: CANVAS.stroke(path.circle(f[0]-X, f[1]-Y, 0.25), input_style)
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_12(rectangle_style, input_style, output_style):
    """
    Divideix la longitud d'un segment entre 8 amb l'ajuda de l'espiral 2/360°
    """

    filename        = "Example_12"
    symbol          = r"$2$"
    K               = 2
    angle           = 360

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((              -X,              -Y),
                            (scale*RR[4][0]-X,scale*RR[4][1]-Y),
                            1/2)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(scale*RR[76][0]-X, scale*RR[76][1]-Y, 0.25),
                              output_style)    
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_13(rectangle_style, input_style, output_style):
    """
    Divideix la longitud d'un segment entre 9 amb l'ajuda de l'espiral 3/360°
    """

    filename        = "Example_13"
    symbol          = r"$3$"
    K               = 3
    angle           = 360

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((              -X,              -Y),
                            (scale*RR[2][0]-X,scale*RR[2][1]-Y),
                            1/2)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), input_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(scale*RR[50][0]-X, scale*RR[50][1]-Y, 0.25),
                              output_style)    
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_14(rectangle_style, input_style, output_style):
    """
    Fes-ho també amb l'ajuda de l'espiral Phi/90°
    """

    filename        = "Example_14"
    symbol          = r"$\phi$"
    K               = (1+sqrt(5))/2
    angle           = 90

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((              -X,              -Y),
                            (scale*RR[7][0]-X,scale*RR[7][1]-Y),
                            1/K)

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), output_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(scale*RR[13][0]-X, scale*RR[13][1]-Y, 0.25),
                              input_style)    
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

def example_15(rectangle_style, input_style, output_style):
    """
    Espiral 2/270º i la duplicació del cub
    """

    filename        = "Example_15"
    symbol          = r"2"
    K               = 2
    angle           = 270

    # Default values:    
    radii           =  24
    width           = 210
    height          = 297
    margin          =  15
    points_per_turn = 360
    turns           =  10
    min_radii       =   5

    # Compute K_per_turn:
    K_per_turn = K**(360/angle)

    # Select the best rotation angle (so one of the radii is vertical):
    rotation, scale = 0, 0
    for i in range(radii//4):
        P = logarithmic_spiral(K_per_turn, 1, points_per_turn, i*2*pi/radii)
        X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
        Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
        s = min((width  - 2*margin) / (X_max - X_min),
                (height - 2*margin) / (Y_max - Y_min)) / 10
        if scale < s: scale, rotation = s, i*2*pi/radii

    # Compute Points:
    P = logarithmic_spiral(K_per_turn, turns, points_per_turn, rotation)
    
    # Compute Radii:
    if radii: R = logarithmic_spiral(K_per_turn, 1, radii, rotation)
    else:     R = tuple()

    # Compute Center and Extremes
    X_min, X_max = min(p[0] for p in P), max(p[0] for p in P)
    Y_min, Y_max = min(p[1] for p in P), max(p[1] for p in P) 
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

    # Draw RECTANGLE
    RR = logarithmic_spiral(K_per_turn, 10, radii, rotation)

    A,B,C,D = get_rectangle((              -X,              -Y),
                            (scale*RR[10][0]-X,scale*RR[10][1]-Y),
                            1/(2**(1/3)))

    CANVAS.stroke(path.path(path.moveto(A[0], A[1]),
                            path.lineto(B[0], B[1]),
                            path.lineto(C[0], C[1]),
                            path.lineto(D[0], D[1]),
                            path.closepath()), rectangle_style)

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

    # Draw INPUT:
    CANVAS.stroke(path.circle(A[0], A[1], 0.25), input_style)
    CANVAS.stroke(path.circle(B[0], B[1], 0.25), output_style)
    
    # Draw OUTPUT:
    CANVAS.stroke(path.circle(scale*RR[16][0]-X, scale*RR[16][1]-Y, 0.25),
                              input_style)    
    
    # Output SVG:
    #CANVAS.writeSVGfile("./pictures/" + filename)

    # Draw Paper Border:
    if margin:
        CANVAS.stroke(path.path(path.moveto(-W, -H), path.lineto(-W,  H),
                                path.lineto( W,  H), path.lineto( W, -H),
                                path.closepath()),
                                BASE + [color.rgb.black, style.linewidth.THIN])

    # Output PDF:
    CANVAS.writePDFfile("./pictures/" + filename)

### MAIN #######################################################################

if __name__ == "__main__":

    # Setup LaTeX font
    text.set(text.LatexEngine)
    text.preamble(r"\renewcommand{\familydefault}{\sfdefault}")

    # Visual styles of the examples:
    input_style     = [style.linecap.round, style.linejoin.round,
                       style.linewidth.THICk, color.cmyk.Red]
    output_style    = [style.linecap.round, style.linejoin.round,
                       style.linewidth.THICk, color.cmyk.Blue]
    rectangle_style = [style.linecap.round, style.linejoin.round,
                       style.linewidth.THIN, color.cmyk.Goldenrod,
                       deco.filled([color.cmyk.Goldenrod])]

    # Draw examples:
    example_00(rectangle_style, input_style, output_style)
    example_00b(rectangle_style, input_style, output_style)
    example_01(rectangle_style, input_style, output_style)
    example_02(rectangle_style, input_style, output_style)
    example_03(rectangle_style, input_style, output_style)
    example_04(rectangle_style, input_style, output_style)
    example_05(rectangle_style, input_style, output_style)
    example_06(rectangle_style, input_style, output_style)
    example_07(rectangle_style, input_style, output_style)
    example_08(rectangle_style, input_style, output_style)
    example_09(rectangle_style, input_style, output_style)
    example_10(rectangle_style, input_style, output_style)
    example_11(rectangle_style, input_style, output_style)
    example_11b(rectangle_style, input_style, output_style)
    example_12(rectangle_style, input_style, output_style)
    example_13(rectangle_style, input_style, output_style)
    example_14(rectangle_style, input_style, output_style)
    example_15(rectangle_style, input_style, output_style)

    # Draw templates:
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

    for name in CONSTANTS:
        symbol, value, angles = CONSTANTS[name]
        for a in angles:
            template("Spiral_{}_{:03d}".format(name, a), symbol, value, a)
    
################################################################################
