from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import json

app = FastAPI(title="Packet Roulette Dashboard")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Mock user data (replace with your auth/database)
current_user = {
    "name": "Digital Detective",
    "email": "detective@packetroulette.com",
    "plan": "Pro",
    "usage": {
        "api_calls": 1247,
        "limit": 5000,
        "storage_mb": 245,
        "storage_limit": 1000
    }
}

# Mock apps/wizards
wizard_apps = [
    {"name": "🔮 Prompt Wizard", "url": "/wizards/prompt", "desc": "AI prompt generator"},
    {"name": "📜 ToS Analyzer", "url": "/wizards/tos", "desc": "Analyze Terms of Service"},
    {"name": "🕵️ Digital Autopsy", "url": "/wizards/autopsy", "desc": "Deep dive internet investigations"},
    {"name": "🛡️ Privacy Scanner", "url": "/wizards/privacy", "desc": "Check website privacy risks"},
    {"name": "📊 Data Visualizer", "url": "/wizards/visualize", "desc": "Create data visualizations"},
    {"name": "🤖 API Builder", "url": "/wizards/api", "desc": "Build custom API endpoints"},
]

# ========== ROUTES ==========

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": current_user,
        "wizards": wizard_apps,
        "page": "dashboard"
    })

@app.get("/account", response_class=HTMLResponse)
async def account_page(request: Request):
    """Account settings"""
    return templates.TemplateResponse("account.html", {
        "request": request,
        "user": current_user,
        "page": "account"
    })

@app.get("/payments", response_class=HTMLResponse)
async def payments_page(request: Request):
    """Billing & payments"""
    plans = [
        {"name": "Free", "price": 0, "features": ["1,000 API calls/month", "Basic wizards"]},
        {"name": "Pro", "price": 19, "features": ["5,000 API calls/month", "All wizards", "Priority support"]},
        {"name": "Enterprise", "price": 99, "features": ["Unlimited API", "Custom wizards", "Dedicated support"]}
    ]
    return templates.TemplateResponse("payments.html", {
        "request": request,
        "user": current_user,
        "plans": plans,
        "page": "payments"
    })

@app.get("/usage", response_class=HTMLResponse)
async def usage_page(request: Request):
    """Usage statistics"""
    return templates.TemplateResponse("usage.html", {
        "request": request,
        "user": current_user,
        "page": "usage"
    })

@app.get("/help", response_class=HTMLResponse)
async def help_page(request: Request):
    """Help center"""
    faqs = [
        {"q": "How do I use the ToS Analyzer?", "a": "Paste any Terms of Service URL..."},
        {"q": "What's my API limit?", "a": "Check your Usage page for current limits."},
        {"q": "How do I cancel my subscription?", "a": "Go to Payments > Cancel Plan."}
    ]
    return templates.TemplateResponse("help.html", {
        "request": request,
        "user": current_user,
        "faqs": faqs,
        "page": "help"
    })

@app.get("/tos", response_class=HTMLResponse)
async def tos_page(request: Request):
    """Terms of Service"""
    return templates.TemplateResponse("tos.html", {
        "request": request,
        "user": current_user,
        "page": "tos"
    })

# ========== WIZARD APPS ==========

@app.get("/wizards/{wizard_name}", response_class=HTMLResponse)
async def wizard_app(request: Request, wizard_name: str):
    """Individual wizard apps"""
    # Here you would load the specific wizard
    return templates.TemplateResponse(f"wizards/{wizard_name}.html", {
        "request": request,
        "user": current_user,
        "wizard": wizard_name
    })

# ========== API ENDPOINTS ==========

@app.get("/api/usage")
async def get_usage():
    """API endpoint for usage data (for AJAX updates)"""
    return current_user["usage"]

@app.get("/api/wizards")
async def get_wizards():
    """API endpoint for wizard list"""
    return {"wizards": wizard_apps}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
