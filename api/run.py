from flask import Flask

app = Flask(__name__)

@app.route("/create_image", methods=["GET"])
def create_image():
    create_image()
    return jsonify(path), 200


if __name__ == "__main__":
    app.run(debug=True)