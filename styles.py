CUSTOM_CSS = """
<style>
/* Previous styles remain the same */

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
    color: #333;
    padding: 10px;
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

/* Message styles */
.pro-message, .con-message {
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
    background-color: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.pro-message {
    border-left: 4px solid #0066cc;
}

.con-message {
    border-left: 4px solid #cc0000;
}

/* Fact check styles */
.fact-check {
    margin-top: 8px;
    margin-left: 20px;
    padding: 10px;
    border-radius: 6px;
    font-size: 0.9em;
    background-color: #f8f9fa;
}

.fact-check-verified {
    border-left: 4px solid #28a745;
}

.fact-check-partial {
    border-left: 4px solid #ffc107;
}

.fact-check-unverified {
    border-left: 4px solid #dc3545;
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
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border: 1px solid #dee2e6;
}

.score-pro {
    color: #0066cc;
}

.score-con {
    color: #cc0000;
}

.score-divider {
    color: #666;
    margin: 0 10px;
}
</style>
"""
