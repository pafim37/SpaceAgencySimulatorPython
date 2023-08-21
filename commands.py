class Command(Enum):
    CREATE_OR_UPDATE_BODY = 1           # create or update custom body defined by user
    HANDLE_SUN = 2                      # create or remove sun
    HANDLE_EARTH = 3                    # create or remove earth
    HANDLE_MARS = 4                     # create or remove mars
    SET_HOME_CAMERA = 5             
    SET_POSITION_OX_CAMERA = 6
    SET_POSITION_OY_CAMERA = 7
    SET_POSITION_OZ_CAMERA = 8
    SET_CONFIGURATION = 9
    CALIBRATE_BARYCENTRUM_TO_ZERO = 10   # set center of the body system (barycentrum) to zero (origin of the global reference system) 