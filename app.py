from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json  # Get the JSON data from the AJAX request
    # Process the data here (save to database, etc.)
    return jsonify({"message": data}), 200
    
if __name__ == '__main__':
    app.run(debug=True)
