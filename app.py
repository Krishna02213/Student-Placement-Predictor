from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the trained placement prediction model
with open("placement_model.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form inputs
        cgpa = float(request.form["cgpa"])
        communication_skills = float(request.form["communication_skills"])
        resume_score = float(request.form["resume_score"])
        coding_score = float(request.form["coding_score"])
        attendance_placement = float(request.form["attendance_placement"])

        # Create feature array
        features = np.array([
            [cgpa, communication_skills, resume_score, coding_score, attendance_placement]
        ])

        # Predict placement
        prediction = model.predict(features)[0]

        # Display result
        if prediction == 1:
            status = "Placed 🎉"
        else:
            status = "Not Placed 😔"

        return render_template(
            "index.html",
            prediction_text=f"Placement Verdict: {status}"
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)