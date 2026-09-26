import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.decisions import router as decisions_router
from .routes.leads import router as leads_router
from .routes.sources import router as sources_router

app = FastAPI(
    title="DecisionGraph API",
    description="Evidence-grounded AI Sales Decision Engine Backend",
    version="1.0.0"
)

# Enable CORS for frontend workspace
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(decisions_router)
app.include_router(leads_router)
app.include_router(sources_router)

@app.get("/")
def read_root():
    return {
        "engine": "DecisionGraph",
        "description": "Evidence-grounded AI Sales Decision Engine",
        "status": "ONLINE",
        "architecture": "Deterministic analytics + RAG + AI orchestration + evidence + human approval"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("decisiongraph.backend.main:app", host="127.0.0.1", port=8000, reload=True)
