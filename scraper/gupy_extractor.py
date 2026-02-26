from playwright.sync_api import sync_playwright

async def intercept_gupy_api(response, extracted_jobs):
  # Search for the specific Gupy API endpoint in the network traffic
  if "/jobs?jobName=" in response.url and response.status == 200:
    try:
      data = response.json()
        
      # Navigate through the JSON structure found in the Gupy API response and extract relevant job details
      for job in data.get('data', []):
    
        # Extract location details, handling cases where city or state might be missing
        city = job.get('city', 'N/A')
        state = job.get('state', '')
        w_type = job.get('workplaceType', 'presencial')

        # Format location as "City - State (WorkplaceType)" but handle missing state 
        loc_string = f"{city} - {state}" if state else city
        location_final = f"{loc_string} ({w_type})"

        # Format the extracted data into a consistent structure for later database insertion
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


async def scrape_gupy(keyword):
    
    extracted_jobs = []
    
    # Use Playwright to launch a headless browser and navigate to the Gupy job search page with the specified keyword
    with sync_playwright() as playwright:
        # Keep headless=True for production, set to False for debugging to see the browser in action
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Attach our spy listener to the network responses
        page.on("response", lambda response: intercept_gupy_api(response, extracted_jobs))
        
        # Navigate to the Gupy portal with your specific keyword
        search_url = f"https://portal.gupy.io/job-search/term={keyword}"
        page.goto(search_url)
        
        # Wait a few seconds for the JavaScript to load and the API to respond
        page.wait_for_timeout(5000) 
        
        # Close the browser
        browser.close()
        
    return extracted_jobs