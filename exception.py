from fastapi.responses import JSONResponse
from fastapi import Request


class PinCodeNotFoundError(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode


class InvalidPinCodeError(Exception):
    def __init__(self, pincode: str, reason: str = "Invalid Format"):
        self.pincode = pincode
        self.reason = reason


# custom handler


async def pincode_not_found_handler(reqeust: Request, exe: PinCodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "pincode_not_found",
            "message": f"No location for pincode: {exe.pincdode}",
            "pincode": exe.pincode
        },
    )


async def invalid_pincode_handler(reqeust: Request, exe: PinCodeNotFoundError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "invalid_pincode",
            "message": f"Pincode: {exe.pincdode} is invalid",
            "pincode": exe.reason
        },
    )
