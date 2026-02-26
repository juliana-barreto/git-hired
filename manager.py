from app import app
from app.services import save_job_to_db

# Importing the synchronous scrapers
from scraper.gupy_extractor import scrape_gupy
from scraper.linkedin_extractor import scrape_linkedin

def run_manager():
    # Enter the global app context to access the database configuration
    with app.app_context():
        
        print("Starting GitHired...")
        
        # Main target keyword for your stack
        target_keyword = "Java"
        
        # Run LinkedIn Engine
        print("\n--- Starting LinkedIn Engine ---")
        linkedin_jobs = scrape_linkedin(target_keyword)
        for job in linkedin_jobs:
            success, result = save_job_to_db(job)
            if success:
                print(f"Saved: {job['title']} at {job['company']}")
            else:
                print(f"Skipped: {result}")
            
        # Run Gupy Engine
        print("\n--- Starting Gupy Engine ---")
        gupy_jobs = scrape_gupy(target_keyword)
        for job in gupy_jobs:
            success, result = save_job_to_db(job)
            if success:
                print(f"Saved: {job['title']} at {job['company']}")
            else:
                print(f"Skipped: {result}")
            
        print("\nExtraction cycle completed successfully!")


if __name__ == '__main__':
    run_manager()