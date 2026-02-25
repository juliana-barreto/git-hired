from app import app
from app.services import save_job_to_db

def run_manager():
    """
    The main orchestrator function.
    """
    # Enter the global app context to access the database configuration
    with app.app_context():
        print("Starting Smart Job Tracker Manager...")
        
        # 1. Here you will eventually call your Playwright scrapers
        # example: gupy_jobs = scrape_gupy()
        
        # 2. For now, create a fake job list to test the database insertion logic
        fake_jobs = [
            {
                "title": "Desenvolvedor Java Junior",
                "company": "Tech Corp",
                "description": "Requisitos: Java, Spring Boot, MySQL. Vaga de estágio.",
                "url": "https://example.com/job/1"
            },
            {
                "title": "Analista Salesforce Pleno",
                "company": "Cloud Inc",
                "description": "Experiência com Apex e LWC.",
                "url": "https://example.com/job/2"
            }
        ]
        
        # 3. Loop through the extracted jobs and pass them to the save function
        for job in fake_jobs:
            save_job_to_db(job)
            
        print("Extraction cycle completed.")


if __name__ == '__main__':
  run_manager()