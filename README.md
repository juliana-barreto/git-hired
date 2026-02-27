# GitHired - Smart Job Tracker
#### Video Demo:  <URL_HERE>
#### Description:

GitHired is a pragmatic, automated Personal CRM (Customer Relationship Management) system built specifically for software developers to manage their job application pipelines. Job hunting can quickly become a chaotic process of managing dozens of browser tabs, generic job aggregators, and lost application statuses. GitHired solves this by combining an automated web scraping engine with a reactive, analytical web dashboard.

Unlike generic job boards, GitHired is highly opinionated. It is tailored for the Backend and Salesforce ecosystem (Java, Spring Boot, Apex, LWC, SOQL), calculating a custom "Match Score" for each job based on targeted keywords and seniority levels (e.g., Junior, Internship). This ensures that the most relevant opportunities bubble up to the top of the dashboard automatically.

## 🚀 Features

* **Automated Data Extraction:** A background worker intercepts network API payloads from complex job portals to extract clean job data automatically.
* **Strategic Match Engine:** Calculates an affinity score for each job based on title and description, allowing the user to focus only on high-value applications.
* **Anti-Duplication Architecture:** The database schema enforces unique constraints on job URLs, ensuring the dashboard remains clean regardless of how many times the extraction cycle runs.
* **Interactive SPA Dashboard:** A Single Page Application feel. Users can filter jobs, update application statuses (Pending, Applied, Interview, Rejected), and save technical notes asynchronously without page reloads.
* **Visual Analytics:** Integrates Chart.js to provide a real-time, reactive doughnut chart summarizing the current state of the application pipeline.

## 🛠️ Technology Stack

* **Backend:** Python 3, Flask
* **Database:** SQLite, SQLAlchemy ORM
* **Automation/Scraping:** Playwright
* **Frontend:** HTML5, TailwindCSS, JavaScript, Jinja2, Chart.js

## 📂 Project Structure and Files

The project follows a modular architecture separating the data extraction pipeline from the web server logic:

* `manager.py`: The entry point for the background worker. It orchestrates the scraping engine and interacts with the database to save new jobs. It also features a command-line interface (e.g., `--reset`) to wipe and reinitialize the database.
* `app/__init__.py`: Initializes the global Flask application context and configures the SQLite database URI.
* `app/models.py`: Defines the database schema using SQLAlchemy, including the `Job` model and data types (Enum for statuses, unique constraints for URLs).
* `app/routes.py`: The RESTful API and controller layer. It handles GET requests to render the template and POST/PUT/DELETE requests for the async frontend operations.
* `app/services.py`: Contains the core business logic, including the `TARGET_KEYWORDS` dictionary and the `calculate_match_score` algorithm. It bridges the raw scraped data with the database models.
* `app/enums.py`: Strictly defines the allowable states for a job application (`PENDING`, `APPLIED`, `INTERVIEW`, `REJECTED`).
* `scraper/gupy_extractor.py`: A robust Playwright script that launches a headless Chromium instance, navigates to the target portal, and intercepts XHR/Fetch API responses to bypass traditional DOM scraping limitations.
* `templates/index.html`: The main user interface, utilizing TailwindCSS for responsive design and Jinja2 templating to render backend data.
* `static/dashboard.js`: Handles all client-side logic, including the Chart.js instantiation, DOM filtering, and async `fetch` calls to the Flask API.

## 🧠 Design Decisions

While building GitHired, several architectural choices were made to prioritize performance and maintainability:

1.  **SQLite over MySQL:** Initially, a robust client-server DB like MySQL was considered. However, since this is a personal, single-user application designed to run locally on a Linux desktop environment, SQLite was chosen. It removes the need for background database daemons while still providing ACID compliance and relational integrity.
2.  **Playwright Network Interception vs. BeautifulSoup:** Modern job portals like Gupy are heavily built on React/Angular and load data dynamically via internal APIs. Traditional HTML parsing (BeautifulSoup) would fail here. Instead of trying to parse the DOM, Playwright was implemented to intercept the raw JSON API responses directly from the network tab, making the scraper incredibly fast and resilient to UI changes.
3.  **Vanilla JS vs. Frontend Framework:** To keep the project lightweight, I opted out of using heavy frameworks like React or Vue. Instead, Vanilla JavaScript coupled with the modern `Fetch API` is used to update the DOM dynamically. This achieves the desired Single Page Application (SPA) reactivity—such as saving notes and updating the chart instantly—without the overhead of node_modules and complex build steps.
4.  **Database-Driven Charting:** The Chart.js instance does not rely on a separate API endpoint to fetch its data. Instead, it parses the `data-status` attributes directly from the rendered HTML DOM. This ensures the chart and the UI are always perfectly in sync and reduces the load on the Flask server.

## 💻 How to Run

1.  Clone the repository and navigate to the project folder.
2.  Install the required dependencies: `pip install flask flask-sqlalchemy playwright python-dateutil`
3.  Install the Playwright browser binaries: `playwright install chromium`
4.  Run the background manager to populate the database: `python manager.py`
5.  Start the Flask web server: `export FLASK_APP=app` followed by `flask run`
6.  Open your browser and navigate to `http://127.0.0.1:5000`.
