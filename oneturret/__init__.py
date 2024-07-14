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
import time

# Initialize the start time when the script is first run
start_time = time.time()


def calculate_lead_angle(turret_pos, enemy, bullet_speed):
    x_t, y_t = turret_pos
    x_e0, y_e0 = enemy[1] # location of enemy
    v_ex, v_ey = enemy[2] # velocity of enemy

    a = v_ex**2 + v_ey**2 - bullet_speed**2
    b = 2 * (v_ex * (x_e0 - x_t) + v_ey * (y_e0 - y_t))
    c = (x_e0 - x_t)**2 + (y_e0 - y_t)**2

    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None  # No solution, the bullet can't reach the enemy

    #t1 = (-b + sqrt(discriminant)) / (2 * a)
    t = (-b - sqrt(discriminant)) / (2 * a)
    #t = max(t1, t2)  # Choose the positive time

    # Calculate lead position
    x_r = max(-40, x_e0 + v_ex * t - x_t)
    y_r = max(-720, y_e0 + v_ey * t - y_t)

    # Calculate the angle
    theta = atan2(y_r, x_r)
    return degrees(theta), sqrt(x_r**2 + y_r**2)

def deadzone_query(target,thresh_x,thresh_y):
    if target[1][0] > thresh_x and target[1][1] < thresh_y:
        return True
    else:
        return False
def endzone_query(target):
    if 350 > target[1][0] > -60 and  245 > target[1][1] > -130:
        return True
    else:
        return False

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
    '''
    if not hasattr(twr_func, "dist"):
        twr_func.dist = 1
     # Calculate the elapsed time
    elapsed_time = time.time() - start_time

    Fire_fire = True
    targ_not_acq = True
    if tag == 'John_beast':
        new_target_dir = 90
        if len(LoT)>1:
            k = 0
            for j, target in enumerate(LoT):
                if target[0] == 'Beast Rider':
                    k = k+1
                    # if len(LoT) != (j+1):
                    #     print('aaaa')
                    #     if k == 8:
                    #         # if (elapsed_time % 4) > 2 and len(LoT)>2:
                    #         #     other = 1
                    #         # else:
                    #         #     other = 0
                    #         other = 0
                    #         print("8 Beast Riders")
                    #         targ = LoT[min(j-(k-1)+other, len(LoT)-1)]
                    #         if not deadzone_query(targ,-425,285):
                    #             targ_not_acq = False
                    #         break
                    # else:
                        # if (elapsed_time % 4) > 2 and len(LoT)>2:
                        #     other = 1
                        # else:
                        #     other = 0
                    other = 0
                    if LoT[min(j-(k-1)+other, len(LoT)-1)][1][1] == 409 and LoT[min(j-(k-1)+other+1, len(LoT)-1)][1][1] == 409:
                        other = 1
                        
                    targ = LoT[min(j-(k-1)+other, len(LoT)-1)]
                    if not deadzone_query(targ,-425,285):
                            targ_not_acq = False
                    break

            if (targ_not_acq):
                for i, target in enumerate(LoT):
                    if not deadzone_query(target,-300,-20):
                        break
                if (i+1) == len(LoT):
                    i = 0
                # if twr_func.dist > 600 and (elapsed_time % 3) > 1 and len(LoT)>2:
                #     targ = LoT[i+2]
                other = 0
                mid = 0
                targ = LoT[i+1+other+mid]
                if endzone_query(targ):
                    for target in LoT:
                        if target[0] == 'Evil Spider':
                            k = k+1
                        if k > 5:
                            mid = k - 4
                        else:
                            mid = k - 1
                else:
                    if (elapsed_time % 4) > 2 and len(LoT)>2:
                        other = 1
                    else:
                        other = 0
                    


                    
                    
                targ = LoT[i+1+other+mid]
                #targ = LoT[i+1]
            new_target_dir, twr_func.dist = calculate_lead_angle(coord, targ, 280)
    #print(new_target_dir)
    if new_target_dir > -50 and new_target_dir < -32:
        new_target_dir = -32
    #for target in LoT:
        #if target[0] == 'Howitzer':
         #   print(target)
    
    
    '''
    RETURNS
    -------
    target_dir
        As defined in `PARAMETERS`
    
    fire
        As defined in `PARAMETERS`
    
    target_dir_is_radians : bool
        Indicates if the output target_dir is in radians
    
    '''
    return (new_target_dir, Fire_fire, False)
#End-def
