CUSTOM_CSS = """
<style>
/* Hide Streamlit's default rainbow decoration bar at the top */
[data-testid="stDecoration"],
#stDecoration {
    display: none !important;
    visibility: hidden !important;
    background-image: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
    background-image: none !important;
}

/* Blue sidebar */
section[data-testid="stSidebar"] {
    background-color: #dbeafe !important;
}

section[data-testid="stSidebar"] > div {
    background-color: #dbeafe !important;
}

/* Base styles */
body {
    color: #1a1a1a;
    background-color: #f8f9fa;
}

/* Final verdict styles */
.final-verdict {
    margin: 20px auto;
    padding: 20px;
    color: #1a1a1a;
    border-radius: 10px;
    text-align: center;
    font-weight: normal;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: white;
    border: 2px solid #e0e0e0;
    max-width: 800px;
}

.verdict-outcome {
    font-size: 1.5em;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: bold;
    padding: 10px;
    border-radius: 8px;
    color: white;
}

.verdict-explanation {
    font-size: 1.1em;
    line-height: 1.5;
    color: #1a1a1a;
    padding: 10px;
}

.verdict-summary {
    color: #1a1a1a;
    font-size: 1.1em;
    margin-bottom: 15px;
}

.verdict-pro .verdict-outcome {
    background-color: #0066cc;
}

.verdict-con .verdict-outcome {
    background-color: #cc0000;
}

.verdict-tie .verdict-outcome {
    background-color: #666666;
}

/* Message styles — chat bubbles, Pro left / Con right */
.pro-message, .con-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
    color: #1a1a1a;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 70%;
}

.pro-message {
    margin-right: auto;
    border-left: 4px solid #0066cc;
    background-color: #f8f9ff;
}

.con-message {
    margin-left: auto;
    border-right: 4px solid #cc0000;
    background-color: #fff0f0;
}

/* Large Pro/Con label as its own header line inside each bubble */
.pro-message strong, .con-message strong {
    display: block;
    font-size: 1.3em;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

/* Fact check styles */
.fact-check {
    margin-top: 8px;
    margin-left: 20px;
    padding: 10px;
    border-radius: 6px;
    font-size: 0.9em;
    background-color: #ffffff;
    color: #1a1a1a;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    max-width: 65%;
    width: fit-content;
}

.fact-check-verified {
    border-left: 4px solid #28a745;
    background-color: #f8fff8;
}

.fact-check-partial {
    border-left: 4px solid #ffc107;
    background-color: #fffff8;
}

.fact-check-unverified {
    border-left: 4px solid #dc3545;
    background-color: #fff8f8;
}

/* Round score styles */
.round-score {
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    padding: 15px;
    margin: 15px 0;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border: 1px solid #dee2e6;
    color: #1a1a1a;
}

.score-pro {
    color: #0066cc;
}

.score-con {
    color: #cc0000;
}

.score-divider {
    color: #666666;
    margin: 0 10px;
}

.score-reason {
    font-weight: normal;
    font-size: 0.85em;
    color: #555555;
    margin-top: 8px;
    font-style: italic;
}

/* Server error styles */
.server-error {
    background-color: #fef2f2;
    border: 2px solid #dc2626;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
    color: #991b1b;
}

.server-error h3 {
    margin: 0 0 10px 0;
    color: #dc2626;
}

.server-error ul {
    margin: 10px 0;
    padding-left: 20px;
}
</style>
"""
