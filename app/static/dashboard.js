// Global variable to hold the Chart.js instance so we can update it later
let jobChart = null;

// Initializes and updates the Doughnut Chart based on current DOM elements.

function updateChart() {
    // Select all job cards currently rendered on the page
    const cards = document.querySelectorAll('.job-card');
    
    // Initialize a counter object for each status
    let counts = { pending: 0, applied: 0, interview: 0, rejected: 0 };
    
    // Tally up the statuses directly from the HTML data attributes
    cards.forEach(card => {
        const status = card.getAttribute('data-status');
        if (counts[status] !== undefined) {
            counts[status]++;
        }
    });

    const canvas = document.getElementById('statusChart');
    if (!canvas) return; // Failsafe in case the chart canvas isn't on the page

    const ctx = canvas.getContext('2d');
    
    // Chart.js requires destroying the old instance before drawing a new one over it
    if (jobChart) {
        jobChart.destroy(); 
    }

    // Create the new doughnut chart
    jobChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Pending', 'Applied', 'Interview', 'Rejected'],
            datasets: [{
                data: [counts.pending, counts.applied, counts.interview, counts.rejected],
                // Colors matching Tailwind palettes: Blue, Orange, Purple, Red
                backgroundColor: ['#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444'], 
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } }
            },
            cutout: '70%' // Controls the thickness of the doughnut ring
        }
    });
}

// Filters the job cards displayed on the screen based on the selected criteria.

function filterJobs(filterType) {
    const cards = document.querySelectorAll('.job-card');
    
    cards.forEach(card => {
        const status = card.getAttribute('data-status');
        const score = parseFloat(card.getAttribute('data-score'));
        let showCard = false;

        // Determine if the card meets the filter criteria
        if (filterType === 'all') {
            showCard = true;
        } else if (filterType === 'pending' && status === 'pending') {
            showCard = true;
        } else if (filterType === 'top-match' && score >= 80) {
            showCard = true;
        } else if (filterType === 'interview' && status === 'interview') {
            showCard = true;
        }

        // Apply visual toggle using Flexbox display
        if (showCard) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

// Asynchronously sends written technical feedback to the backend REST API.

async function saveFeedback(jobId) {
    const feedbackText = document.getElementById(`feedback-${jobId}`).value;
    const statusSpan = document.getElementById(`feedback-status-${jobId}`);

    try {
        const response = await fetch(`/jobs/${jobId}/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ feedback: feedbackText }),
        });

        if (response.ok) {
            // Provide visual feedback to the user by showing a 'Saved!' text for 2 seconds
            statusSpan.classList.remove("hidden");
            setTimeout(() => {
                statusSpan.classList.add("hidden");
            }, 2000);
        } else {
            alert("Failed to save feedback on the server.");
        }
    } catch (error) {
        console.error("Error saving feedback:", error);
    }
}

// Updates the job status via API and refreshes the chart to reflect the new state.

async function updateJobStatus(jobId, newStatus) {
    try {
        const response = await fetch(`/jobs/${jobId}/status`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus }),
        });

        if (response.ok) {
            // Update the HTML data-status attribute so the chart counts it correctly
            document.getElementById(`card-${jobId}`).setAttribute('data-status', newStatus);
            // Redraw the chart with the updated metrics
            updateChart();
        } else {
            alert("Failed to update status on the server.");
        }
    } catch (error) {
        console.error("Error updating job:", error);
    }
}

// Deletes a job from the database, removes its HTML element, and updates metrics.

async function deleteJob(jobId) {
    // Add a safety check to prevent accidental deletions
    if (!confirm("Are you sure you want to delete this job?")) return;

    try {
        const response = await fetch(`/jobs/${jobId}`, {
            method: "DELETE",
        });

        if (response.ok) {
            // Physically remove the HTML node from the DOM
            const cardElement = document.getElementById(`card-${jobId}`);
            cardElement.remove();

            // Decrease the total count displayed at the top of the dashboard
            const countElement = document.getElementById("total-count");
            countElement.innerText = parseInt(countElement.innerText) - 1;
            
            // Redraw the chart since a data point was removed
            updateChart();
        } else {
            alert("Failed to delete the job.");
        }
    } catch (error) {
        console.error("Error deleting job:", error);
    }
}

// Automatically draw the chart when the HTML finishes loading
document.addEventListener('DOMContentLoaded', updateChart);