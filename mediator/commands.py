class Command(Enum):
    CREATE_OR_UPDATE_BODY = "CREATE_OR_UPDATE_BODY"                     # create or update custom body defined by user
    REMOVE_BODY = "REMOVE_BODY"                                         # remove body
    SET_HOME_CAMERA = "SET_HOME_CAMERA"             
    SET_POSITION_OX_CAMERA = "SET_POSITION_OX_CAMERA"
    SET_POSITION_OY_CAMERA = "SET_POSITION_OY_CAMERA"
    SET_POSITION_OZ_CAMERA = "SET_POSITION_OZ_CAMERA"
    SET_CONFIGURATION = "SET_CONFIGURATION"
    CALIBRATE_BARYCENTRUM_TO_ZERO = "CALIBRATE_BARYCENTRUM_TO_ZERO"     # set center of the body system (barycentrum) to zero (origin of the global reference system) 
    FOCUS_ON_BODY = "FOCUS_ON_BODY"
    THRUST_PLAYER = "THRUST_PLAYER"
    GET_PLAYER = "GET_PLAYER"