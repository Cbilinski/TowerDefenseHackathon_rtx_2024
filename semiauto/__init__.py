# DO NOT EDIT -->
from pathlib    import Path
from typing     import Tuple

THIS_FOLDER = Path(__file__).resolve().parent
TWR_POS = []
with open(THIS_FOLDER / 'twr.csv', 'r') as twr_h:
    for ln in twr_h:
        ln_parts = ln.strip().split(',') + [None]
        for idx in range(1, 3): ln_parts[idx] = int(ln_parts[idx])
        TWR_POS += [tuple(ln_parts + [None])]
    #End-for
#End-with
# <-- DO NOT EDIT

from math import sqrt, atan2, degrees

def twr_func(coord, tag : str, LoT : list, fire : bool, current_dir : float, target_dir : float) -> Tuple[float, bool, bool]:
    '''
    Add in your turret logic here
    
    Notes:
    - "2D-Vector" == pygame.math.Vector2d using pixels
    - angle == float in degrees
    
    PARAMETERS
    ----------
    coord : 2D-Vector
        Location of the subject tower relative to the home base
    
    tag : str
        An identifier defined by you
    
    LoT : list
        "List of Targets", each entry in this list has the following structure
        - Target Type : str
        - Target Position : 2D-Vector
        - Target Velocity : 2D-Vector
    
    fire : bool
        Indicates whether or not the next round will be fired when chambered
    
    current_dir : angle
        Current bearing of the gun
    
    target_dir : angle
        Target bearing of the gun
    
    RETURNS
    -------
    target_dir
        As defined in `PARAMETERS`
    
    fire
        As defined in `PARAMETERS`
    
    target_dir_is_radians : bool
        Indicates if the output target_dir is in radians
    
    '''
    angle = 80
    if tag == 'a' and len(LoT) > 2:
        angle = 90

    if tag == 'b':
        if len(LoT) == 3 or len(LoT) < 10:
            angle = calculate_lead_angle(coord, LoT[2], 280)
        elif len(LoT) > 3:
            br = False
            for l in LoT:
                if l[0] == 'Beast Rider':
                    angle = calculate_lead_angle(coord, l, 280)
                    br = True
                    break
                angle = calculate_lead_angle(coord, LoT[3], 280)

    return (angle, True, False)
#End-def

def calculate_lead_angle(turret_pos, enemy, bullet_speed):
    x_t, y_t = turret_pos
    x_e0, y_e0 = enemy[1]
    v_ex, v_ey = enemy[2]

    a = v_ex**2 + v_ey**2 - bullet_speed**2
    b = 2 * (v_ex * (x_e0 - x_t) + v_ey * (y_e0 - y_t))
    c = (x_e0 - x_t)**2 + (y_e0 - y_t)**2

    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None

    t = (-b - sqrt(discriminant)) / (2 * a)

    x_r = x_e0 + v_ex * t - x_t
    y_r = y_e0 + v_ey * t - y_t

    theta = atan2(y_r, x_r)
    return degrees(theta)
