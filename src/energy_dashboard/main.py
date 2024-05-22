import uvicorn

if __name__ == "__main__":
    # Run the app using uvicorn
    uvicorn.run("src/energy_dashboard.routes:app", host="0.0.0.0", port=8000, reload=True)
