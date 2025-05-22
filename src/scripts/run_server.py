import uvicorn
import sys
from improved_config import test_connection

def main():
    
    print("=== Starting FastAPI Server ===")
    
    print("\nChecking database connection...")
    if not test_connection():
        print("\n❌ Failed to connect to database!")
        print("Please check:")
        print("1. PostgreSQL is running")
        print("2. Database 'project_db' exists")
        print("3. User credentials are correct")
        print("4. Tables are created using the SQL script")
        sys.exit(1)
    
    print("✅ Database connection successful!")
    print("\nStarting server...")
    print("API will be available at:")
    print("- http://localhost:8000")
    print("- Swagger UI: http://localhost:8000/docs")
    print("- ReDoc: http://localhost:8000/redoc")
    print("\nPress CTRL+C to stop the server\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
