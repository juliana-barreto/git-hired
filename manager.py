from app import app
from app.services import save_job_to_db
from scraper.extractors.gupy_extractor import scrape_gupy

def run_manager():
   with app.app_context():
        print("Starting job search...")
        
        
        jobs = scrape_gupy("java")
        
        for job in jobs:
            success, result = save_job_to_db(job)
            if success:
                print(f"New job added: {job['title']}")
            
        print(f"Cycle finished. {len(jobs)} jobs processed.")


if __name__ == '__main__':
  run_manager()