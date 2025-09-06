import funcs

import flask

app = flask.Flask(__name__)


@app.route("/volume", methods=["GET", "POST"])
def volume_api():
    if flask.request.method == "GET":
        try:
            return flask.jsonify({"volume": funcs.get_master_volume()}), 200
        except Exception as e:
            return flask.jsonify({"error": str(e)}), 500
    elif flask.request.method == "POST":
        try:
            funcs.set_master_volume(flask.request.json["volume"]) # type: ignore
            return flask.jsonify({"volume": funcs.get_master_volume()}), 200
        except Exception as e:
            return flask.jsonify({"error": str(e)}), 500
    
    return flask.jsonify({"error": "Invalid request"}), 400

@app.route("/music", methods=["POST"])
def music_api():
    if flask.request.method != "POST" or "action" not in flask.request.json: # type: ignore
        return flask.jsonify({"error": "Invalid request"}), 400
    action = flask.request.json["action"] # type: ignore
    if action == "play_pause":
        funcs.play_pause_music()
    elif action == "next":
        funcs.next_track()
    elif action == "previous":
        funcs.previous_track()
    return flask.jsonify({"message": "Music action successful"}), 200

@app.route("/shutdown", methods=["GET"])
def shutdown_api():
    funcs.shutdown()
    return flask.jsonify({"message": "Shutdown successful"}), 200

@app.route("/lock", methods=["GET"])
def lock_api():
    funcs.lock_screen()
    return flask.jsonify({"message": "Lock successful"}), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)