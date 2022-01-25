import json
from fastapi import APIRouter, Body, Response
from apps.controllers.LoanController import ControllerLoan as loan

router = APIRouter()

example_input_cifno = json.dumps({
    "cif": "1",
}, indent=2)

@router.post("/get_loan_by_cif")
async def get_loan_by_cif(response: Response, input_data=Body(..., example=example_input_cifno)):
    result = loan.get_loan_by_cif(input_data=input_data)
    response.status_code = result.status
    return result

@router.post("/get_loan_by_cif_debug")
async def get_loan_by_cif_debug(response: Response, input_data=Body(..., example=example_input_cifno)):
    result = loan.get_loan_by_cif_debug(input_data=input_data)
    response.status_code = result.status
    return result