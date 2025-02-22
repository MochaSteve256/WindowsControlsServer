import volume_funcs

import flask

app = flask.Flask(__name__)


@app.route("/volume", methods=["GET", "POST"])
def volume_api():
    if flask.request.method == "GET":
        try:
            return flask.jsonify({"volume": volume_funcs.get_master_volume()}), 200
        except Exception as e:
            return flask.jsonify({"error": str(e)}), 500
    elif flask.request.method == "POST":
        try:
            volume_funcs.set_master_volume(flask.request.json["volume"]) # type: ignore
            return flask.jsonify({"volume": volume_funcs.get_master_volume()}), 200
        except Exception as e:
            return flask.jsonify({"error": str(e)}), 500
    
    return flask.jsonify({"error": "Invalid request"}), 400


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)