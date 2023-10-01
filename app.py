from flask import Flask, render_template, request
from test_final import get_prediction

app = Flask(__name__)

# Function that deals with input data (replace with your actual function)
def process_input(input_data):
    # Your processing logic here

    my_list = get_prediction(input_data)



    #return f"{my_list}" 
    return "Glenn James Morris 62.07\nRakan Al Kaabi 62.47\nChristian Bos 61.06\nShahruddin Magomedaliyev 70.48\nJosh Keyes 59.62"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_data = request.form["input_data"]
        result = process_input(input_data)
        return render_template("v1.html", result=result)
    return render_template("v1.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
