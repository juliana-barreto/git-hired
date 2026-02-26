from app import app
from app.services import save_job_to_db
from scraper.gupy_extractor import scrape_gupy

def run_manager():
	# Enter the global app context to access the database configuration
	with app.app_context():
			
			print("Starting GitHired...")
			
			# Main target keyword for your stack
			target_keyword = "Java"
					
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