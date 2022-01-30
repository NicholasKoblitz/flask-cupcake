"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake, serialize_cupcake


app = Flask(__name__)

app.config["SECRET_KEY"] = "qwteyruwi1735173jkruyrol"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///cupcakes'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True


connect_db(app)

# -----------------------API Routes -----------------------------
@app.route("/api/cupcakes")
def get_cupcakes():
    """Gets all cupcake data"""

    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [serialize_cupcake(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Gets a single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized_cupcake)


@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """Create a new cupcake"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    if request.json["image"] == '':
        image = "https://tinyurl.com/demo-cupcake"
    else:
        image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    serialized_cupcake = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized_cupcake), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake's data"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()

    serialized_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized_cupcake)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)

    return jsonify(message="Deleted")

# ------------------End of API Routes----------------------------------------

# --------------------Web Page Routes----------------------------------------
@app.route("/")
def home_page():
    """Shows Homepage"""

    return render_template("home_page.html")