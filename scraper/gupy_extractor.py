from playwright.sync_api import sync_playwright

def intercept_gupy_api(response, extracted_jobs):
    # Intercept only the specific jobs API endpoint
    if "/jobs?jobName=" in response.url and response.status == 200:
        try:
            data = response.json()
            
            # Extract relevant job details from the JSON payload
            for job in data.get('data', []):
                
                city = job.get('city', 'N/A')
                state = job.get('state', '')
                w_type = job.get('workplaceType', 'presencial')
                
                loc_string = f"{city} - {state}" if state else city
                location_final = f"{loc_string} ({w_type})"

                formatted_job = {
                    "title": job.get('name'),               
                    "company": job.get('careerPageName'),   
                    "description": job.get('description'),   
                    "url": job.get('jobUrl'),               
                    "location": location_final,
                    "date": job.get('publishedDate')      
                }
                extracted_jobs.append(formatted_job)
                
        except Exception as e:
            print(f"Error parsing Gupy JSON: {e}")

def scrape_gupy(keyword):
    extracted_jobs = []
    
    with sync_playwright() as p:
        # Launch browser silently
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Attach the network listener to capture API payloads
        page.on("response", lambda response: intercept_gupy_api(response, extracted_jobs))
        
        search_url = f"https://portal.gupy.io/job-search/term={keyword}"
        print(f"Navigating to Gupy: {search_url}")
        page.goto(search_url)
        
        page.wait_for_timeout(3000) 
        
        # Trigger pagination by scrolling down multiple times
        print("Scrolling to load more jobs...")
        for _ in range(5):
            page.keyboard.press("End")
            page.wait_for_timeout(2000) 
            
        browser.close()
        
    return extracted_jobs