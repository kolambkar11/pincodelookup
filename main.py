from fastapi import FastAPI
from exception import (
    PinCodeNotFoundError,
    pincode_not_found_handler,
    InvalidPinCodeError,
    invalid_pincode_handler,
)
from data import pincode_db

from models import LocationResponse, BulkResponse, BulkRequest

app = FastAPI(
    title="Pincode Lookup API",
    description="Auto fill city and state from india pincode during checkout",
)

# register your custom exception handler

app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(
    InvalidPinCodeError, pincode_not_found_handler
)  # recheck this


@app.get("/")
def root():
    return {"message": "Pincode Lookup"}


@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pincode(code: str):
    print("code-------inpincode")
    if len(code) != 6 or not code.isdigit():
        raise InvalidPinCodeError(code, "Must be exaclty 6 digit")
    if code not in pincode_db:
        raise PinCodeNotFoundError(code)
    return pincode_db[code]

@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkRequest):
    results = []
    missing = []
    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)
    return BulkResponse(
        found=len(results), not_found=len(missing), reuslts=results, missing=missing
    )
