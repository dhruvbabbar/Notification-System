import enum 
class Codes(enum.Enum): 
    success=200
    exceptionWhileSending=301
    badRequest=400
    unauthorised=401
    unprocessable=422