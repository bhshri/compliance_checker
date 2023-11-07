import traceback
from pydantic import BaseModel, Field
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.responses import RedirectResponse

from src.compliance_checker import ComplianceChecker

app = FastAPI(title='COMPLIANCE CHECKER', description="COMPLIANCE CHECKER")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

compliance_checker = ComplianceChecker()


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

class ComplianceCheckInputData(BaseModel):
    webpage_url: str = Field()

        
@app.post("/getnoncompliantresults")
async def get_non_compliant_results(complianceCheckInputData: ComplianceCheckInputData) -> Response:
    try:
        response_json = compliance_checker.get_noncompliant_results(complianceCheckInputData.webpage_url)
        return JSONResponse(response_json)
    except Exception as error:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(error))      

        
if __name__ == "__main__":
    uvicorn.run(app, debug=True)
