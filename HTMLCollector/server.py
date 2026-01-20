from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

DATA_DIR = "data"
MAX_SAMPLES = 50
os.makedirs(DATA_DIR, exist_ok=True)

# Khmer letters from ក to អ
KHMER_LETTERS = [
    "ក","ខ","គ","ឃ","ង","ច","ឆ","ជ","ឈ","ញ",
    "ដ","ឋ","ឌ","ឍ","ណ","ត","ថ","ទ","ធ","ន",
    "ប","ផ","ព","ភ","ម","យ","រ","ល","វ",
    "ស","ហ","ឡ","អ","០","១","២","៣","៤","៥","៦","៧","៨","៩"
]

def count_samples(char):
    path = os.path.join(DATA_DIR, f"{char}.txt")
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)

@app.route("/")
def index():
    return render_template("draw.html", letters=KHMER_LETTERS)

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    char = data["char"]
    strokes = data["strokes"]

    path = os.path.join(DATA_DIR, f"{char}.txt")
    current_count = count_samples(char)

    if current_count >= MAX_SAMPLES:
        return jsonify({"status": "full", "count": current_count})

    # Convert coordinates to integers like Tkinter version
    stroke_strings = []
    for stroke in strokes:
        points = " ".join([f"{int(round(x))} {int(round(y))}" for x, y in stroke])
        stroke_strings.append(points)

    line = f"{char} " + " # ".join(stroke_strings) + " #\n"

    with open(path, "a", encoding="utf-8") as f:
        f.write(line)

    return jsonify({"status": "saved", "count": current_count + 1})

if __name__ == "__main__":
    app.run(host="172.20.10.2", port=5000)
