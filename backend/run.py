#!/usr/bin/env python3
"""
Startup script for the Note Taking App.
Run this file to start the application server.
"""
import sys
import os

# Add the noteapp directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Note Taking & To-Do List App...")
    print("📍 Server will be available at: http://127.0.0.1:8003")
    print("📚 API Documentation: http://127.0.0.1:8003/api/docs")
    print("❤️  Health Check: http://127.0.0.1:8003/health")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8003,
        reload=True,
        log_level="info"
    )
