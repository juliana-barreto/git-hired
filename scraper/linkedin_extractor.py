from playwright.sync_api import sync_playwright

def scrape_linkedin(keyword):
    extracted_jobs = []
    
    # LinkedIn public search URL. 
    # f_TPR=r86400 filters for jobs posted in the last 24 hours
    search_url = f"https://br.linkedin.com/jobs/search?keywords={keyword}&location=Brazil&f_TPR=r86400"

    with sync_playwright() as playwright:
        # Keep headless=True for background execution, False for debugging
        browser = playwright.chromium.launch(headless=True) 
        page = browser.new_page()

        print(f"Accessing public LinkedIn for: {keyword}...")
        page.goto(search_url)
        
        # Wait dynamically for the job list to appear in the DOM (timeout of 10 seconds)
        page.wait_for_selector("ul.jobs-search__results-list > li", timeout=10000)

        # Get job cards loaded on the left panel
        job_cards = page.locator("ul.jobs-search__results-list > li").all()
        
        print(f"Found {len(job_cards)} job cards on the first page.")

        # Limit to 10 jobs per run to avoid LinkedIn rate limits/blocks
        for card in job_cards[:10]:
            try:
                # Scroll the card into the viewport before clicking to avoid errors
                card.scroll_into_view_if_needed()
                card.click()

                # Wait dynamically for the right panel description to become visible
                page.wait_for_selector(".show-more-less-html__markup", state="visible", timeout=5000)

                # Extract basic info
                title = card.locator(".base-search-card__title").inner_text().strip()
                company = card.locator(".base-search-card__subtitle").inner_text().strip()
                location = card.locator(".job-search-card__location").inner_text().strip()
                
                # Clean tracking parameters from the URL to maintain the UNIQUE constraint
                raw_url = card.locator("a.base-card__full-link").get_attribute("href")
                clean_url = raw_url.split("?")[0] if raw_url else "URL not found"

                # Extract description for the match_score processing
                description_locator = page.locator(".show-more-less-html__markup")
                if description_locator.count() > 0:
                    description = description_locator.inner_text().strip()
                else:
                    description = "Description not loaded."

                formatted_job = {
                    "title": title,
                    "company": company,
                    "description": description,
                    "url": clean_url,
                    "location": location,
                    "date": None # The database model sets the default datetime
                }
                
                extracted_jobs.append(formatted_job)
                print(f"Extracted: {title} at {company}")

            except Exception as e:
                print(f"Error extracting specific job: {e}")

        browser.close()
        
    return extracted_jobs