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
    if tag == "2":
        # Check if "Onyx Golem" is present in LoT and Beast Riders below 7
        if any(target[0] == "Onyx Golem" for target in LoT) and sum(1 for target in LoT if target[0] == "Beast Rider") < 3:
            # Check if length of LoT is less than 10
            if len(LoT) < 10:
                target_dir = 33
            else:
                target_dir = 74
        else:
            target_dir = 90
    else:
        if any(target[0] == "Beast Rider" for target in LoT):
            target_dir = 270
        elif any(target[0] == "Onyx Golem" for target in LoT):
            if len(LoT) < 10:
                target_dir = 245
            else:
                pass
        else:
            target_dir = 175

    return (target_dir, True, False)
    
    
    #return (coord.as_polar()[1], True, False)
    #return (target_dir, True, False)
#End-def
