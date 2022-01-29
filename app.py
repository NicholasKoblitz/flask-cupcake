"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request
from models import db, connect_db, Cupcake, serialize_cupcake


app = Flask(__name__)

app.config["SECRET_KEY"] = "qwteyruwi1735173jkruyrol"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///cupcakes'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True


connect_db(app)


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
    image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    serialized_cupcake = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized_cupcake), 201)


