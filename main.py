from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, habits, goals, dashboard, analytics, personal, food, meal_plan, recipe
from config.database import init_db

# Initialize database tables
try:
    init_db()
    print("Database connected successfully")
except Exception as e:
    print("Database connection failed:", e)
app = FastAPI(
    title="Habit Tracker & Goal Planner API",
    description="MySQL-powered backend for premium productivity dashboard",
    version="1.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(goals.router)
app.include_router(dashboard.router)
app.include_router(analytics.router)
app.include_router(personal.router)
app.include_router(personal.calorie_router)
app.include_router(personal.period_router)
app.include_router(food.router)
app.include_router(meal_plan.router)
app.include_router(recipe.router)

@app.get("/")
async def root():
    # Healthcheck endpoint
    return {
        "message": "Welcome to Habit Tracker & Goal Planner API (MySQL Edition)",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
