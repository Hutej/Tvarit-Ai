from fastapi import FastAPI
from app.schemas.input_schema import InputRequest
from app.pipeline.injection_pipeline import run_pipeline

app = FastAPI()


@app.post("/preauth/validate")
async def validate(request: InputRequest):
    data = request.model_dump()   # ✅ correct
    result = run_pipeline(data)
    return result