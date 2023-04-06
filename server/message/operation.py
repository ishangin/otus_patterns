from enum import Enum


class OPERATION(Enum):
    Game_New = 0
    Command_Move = 1
    Command_Rotate = 2
    Command_CheckFuel = 3
    Get_Token = 12  # GET_JWT
    Auth_Response = 13
    Create_Object = 14
