// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDzFikflLPAzMTg0fbl6IgVvHZTRLMs_pk",
  authDomain: "creditcard-approval-prediction.firebaseapp.com",
  projectId: "creditcard-approval-prediction",
  storageBucket: "creditcard-approval-prediction.firebasestorage.app",
  messagingSenderId: "977150912531",
  appId: "1:977150912531:web:5b2157c385ab89fd6677e6",
  measurementId: "G-591N2M3LL8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// DOM Elements
const navBtns = document.querySelectorAll('.nav-btn');
const viewSections = document.querySelectorAll('.view-section');
const form = document.getElementById('prediction-form');
const submitBtn = document.getElementById('submit-btn');
const btnText = submitBtn.querySelector('span');
const spinner = document.getElementById('spinner');
const resultContainer = document.getElementById('result-container');
const resultBadge = document.getElementById('result-badge');
const resultTitle = document.getElementById('result-title');
const probFill = document.getElementById('prob-fill');
const probText = document.getElementById('approval-prob');
const resultMessage = document.getElementById('result-message');

// API Endpoint
const API_URL = '/api/predict';

// Navigation Logic
navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all
        navBtns.forEach(b => b.classList.remove('active'));
        viewSections.forEach(v => v.classList.add('hidden'));
        viewSections.forEach(v => v.classList.remove('active'));
        
        // Add active class to clicked
        btn.classList.add('active');
        const targetId = btn.getAttribute('data-target');
        const targetView = document.getElementById(targetId);
        targetView.classList.remove('hidden');
        targetView.classList.add('active');
    });
});

// Form Submission Logic
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // UI Loading State
    btnText.textContent = 'Processing...';
    spinner.classList.remove('hidden');
    submitBtn.disabled = true;
    resultContainer.classList.add('hidden');
    
    // Gather Data
    const data = {
        income: document.getElementById('income').value,
        employment_duration: document.getElementById('employment').value,
        existing_loan_balance: document.getElementById('loan-balance').value,
        credit_inquiries: document.getElementById('inquiries').value,
        payment_status: document.getElementById('payment-status').value
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const result = await response.json();
        
        // Handle Error from Server
        if (result.error) {
            throw new Error(result.error);
        }
        
        // Update UI with Result
        showResult(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error connecting to prediction server. Ensure the Flask backend is running on localhost:5000.');
    } finally {
        // Reset UI
        btnText.textContent = 'Predict Approval';
        spinner.classList.add('hidden');
        submitBtn.disabled = false;
    }
});

function showResult(result) {
    resultContainer.classList.remove('hidden');
    
    // Calculate percentage
    const probability = Math.round(result.probability.approve * 100);
    probText.textContent = `${probability}%`;
    
    // Trigger animation
    setTimeout(() => {
        probFill.style.width = `${probability}%`;
    }, 100);
    
    if (result.approved) {
        resultBadge.textContent = 'APPROVED';
        resultBadge.className = 'badge approved';
        probFill.style.background = 'var(--success)';
        resultTitle.textContent = 'Congratulations!';
        resultMessage.textContent = 'Based on the provided information, our AI model predicts that you are highly likely to be approved for a credit card. Your low-risk profile aligns with our criteria.';
    } else {
        resultBadge.textContent = 'REJECTED';
        resultBadge.className = 'badge rejected';
        probFill.style.background = 'var(--danger)';
        resultTitle.textContent = 'Application Flagged';
        resultMessage.textContent = 'Our AI model predicts a high likelihood of rejection. This is typically due to factors such as existing loan burdens, recent credit inquiries, or past payment history. Consider reducing debt before applying.';
    }
}
const connectBtn = document.getElementById("connect-crm-btn");
const csvFile = document.getElementById("csv-file");
const crmResults = document.getElementById("crm-results");

if (connectBtn) {

    connectBtn.addEventListener("click", () => {
        csvFile.click();
    });

    csvFile.addEventListener("change", async () => {

        if (csvFile.files.length === 0) return;

        const formData = new FormData();
        formData.append("file", csvFile.files[0]);

        try {

            const response = await fetch("/api/upload_csv", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            console.log(data);

let approved = 0;
let rejected = 0;

data.forEach(r => {
    if (r.approved)
        approved++;
    else
        rejected++;
});

console.log("Total:", data.length);
console.log("Approved:", approved);
console.log("Rejected:", rejected);

console.log(document.getElementById("total-count"));
            if (data.error) {
                alert(data.error);
                return;
            }


document.getElementById("total-count").innerText = data.length;
document.getElementById("approved-count").innerText = approved;
document.getElementById("rejected-count").innerText = rejected;
document.getElementById("crm-summary").style.display = "flex";

let html = `
<h2 style="margin-top:30px;">Prediction Results</h2>

<table class="crm-table">

<thead>
<tr>
<th>Income</th>
<th>Employment</th>
<th>Loan Balance</th>
<th>Probability</th>
<th>Decision</th>
</tr>
</thead>

<tbody>
`;

data.forEach(row=>{

html +=`

<tr>

<td>₹${Number(row.income).toLocaleString()}</td>

<td>${row.employment_duration} Years</td>

<td>₹${Number(row.existing_loan_balance).toLocaleString()}</td>

<td>${row.approval_probability}%</td>

<td>

<span class="${row.approved?'approved-pill':'rejected-pill'}">

${row.approved?'Approved':'Rejected'}

</span>

</td>

</tr>

`;

});

html +=`

</tbody>

</table>

`;

crmResults.innerHTML = html;
        } catch (err) {
            console.error(err);
            alert("Unable to upload CSV.");
        }

    });

}