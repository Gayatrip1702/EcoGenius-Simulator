# app.py

from flask import Flask, render_template, request, redirect, url_for
import time

# Initialize the Flask application
app = Flask(__name__)

# --- 1. Homepage Route ---
@app.route('/')
def index():
    # Render the input form
    return render_template('index.html')

# --- 2. Simulation Handler ---
@app.route('/simulate', methods=['POST'])
def simulate():
    # Get input data from the form
    try:
        carbon_target = int(request.form.get('carbon_target'))
        product_name = request.form.get('product')
    except ValueError:
        # Set default values if input is not a valid number
        carbon_target = 30
        product_name = 'Default Product'
    
    # Simulate AI processing time (3 seconds)
    print(f"Starting simulation for {product_name} with target {carbon_target}%...")
    time.sleep(3) 

    # Redirect to the results page, passing key inputs as URL parameters
    return redirect(url_for('results', target=carbon_target, product=product_name))


# --- 3. Results Page Route ---
@app.route('/results')
def results():
    
    # Get inputs from the URL parameters
    target_reduction = int(request.args.get('target', 30)) 
    product_name = request.args.get('product', 'Generic Product') 
    
    # -----------------------------------------------------
    # DUMMY AI SIMULATION LOGIC (FINALIZED) - Results based on user input
    # -----------------------------------------------------

    # Default (Old) values for comparison
    old_carbon = 100
    old_cost = 50
    
    # Calculate New Carbon based on user's target
    new_carbon_value = old_carbon * (1 - target_reduction / 100.0)
    
    if target_reduction >= 40:
        # High Reduction Target = High Cost Increase (25%)
        new_cost_value = old_cost * 1.25 
        debate_summary = f"Conclusion: The {target_reduction}% target for {product_name} was extremely challenging. It was achieved with high conflict, resulting in a 25% cost increase and longer lead times."
        
    elif target_reduction >= 20:
        # Medium Reduction Target = Minor Cost Increase (5%)
        new_cost_value = old_cost * 1.05 
        debate_summary = f"Conclusion: The {target_reduction}% target was achieved efficiently. Agents found a compromise using rail and local sourcing, resulting in only a 5% cost increase."
        
    else:
        # Low Reduction Target = Minimal Cost Increase (1%)
        new_cost_value = old_cost * 1.01 
        debate_summary = f"Conclusion: Optimal win-win. The low-risk, high-profit solution was found easily by the Orchestrator agent for the {target_reduction}% target."

    # 1. Multi-Agent Debate Log
    debate_log = [
        {"agent": "Carbon Agent", "text": f"Target: Reduce Carbon by {target_reduction}%. Current shipping emissions are unacceptable.", "color": "green"},
        {"agent": "Cost Agent", "text": "We cannot accept a cost increase exceeding 5% to maintain financial viability.", "color": "red"},
        {"agent": "Logistics Agent", "text": "A maximum of 10 days shipping delay is acceptable for this product.", "color": "default"},
        {"agent": "Genius Orchestrator", "text": debate_summary, "color": "blue"},
    ]
    
    # 2. Final Visualization Data
    final_data = {
        "old_carbon": old_carbon,
        "new_carbon": round(new_carbon_value, 2),
        "old_cost": old_cost,
        "new_cost": round(new_cost_value, 2),
        "reduction_percent": target_reduction 
    }

    # Render the results template, passing the dynamic data
    return render_template('results.html', debate_log=debate_log, final_data=final_data)


# Run the application
if __name__ == '__main__':
    # debug=True allows the server to restart automatically when you save changes
    app.run(debug=True)