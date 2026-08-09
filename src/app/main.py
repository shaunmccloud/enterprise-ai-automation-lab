from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Automation Lab",
    description="Secure, AI-assisted enterprise workflow automation.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Enterprise AI Automation Lab",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
