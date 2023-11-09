from flask import Flask, request, jsonify, redirect
import random
import string
import json
import datetime


def load_data(file_name):
    """
    Load data from a JSON file.

    Args:
        file_name (str): The path to the JSON file to load.

    Returns:
        dict: The data loaded from the JSON file, or an empty dictionary if the file does not exist or it is invalid.
    """
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(file_name, data):
    """
    Save data to a JSON file.

    Args:
        file_name (str): The path to the JSON file to save data to.
        data (dict): The data to save.
    """
    with open(file_name, "w") as file:
        json.dump(data, file)


url_data = load_data("shortener_app_data.json")

app = Flask(__name__)


@app.route('/shorten', methods=['POST'])
def url_shortener():
    # data = {
    #     "url": "https://www.google.com/",
    #     "shortcode": None
    # }
    """
    Shorten a URL and return the shortcode.

    The client should send a JSON object containing the URL and an optional shortcode.
    If the shortcode is not provided, a random one will be generated.

    Returns:
        JSON response with the shortcode or an error message.
    """
    data = request.get_json()
    shortcode = data.get("shortcode")
    url = data.get("url")

    if not url:
        return jsonify({"error": "Url not present"}), 400

    if shortcode:
        if len(shortcode) != 6 or not all(char.isalnum() or char =='_' for char in shortcode):
            return jsonify(({"error": "The provided shortcode is invalid"})), 412
        if shortcode in url_data:
            return jsonify({"error": "Shortcode already in use"}), 409
    else:
        shortcode = ''.join(random.choice(string.ascii_letters + string.digits + "_") for _ in range(6))
    url_data[shortcode] = {
        "url": url,
        "created": datetime.datetime.now().isoformat(),
        "lastRedirect": None,
        "redirectCount": 0}
    save_data("shortener_app_data.json", url_data)

    return jsonify({"shortcode": shortcode})


@app.route('/<shortcode>', methods=['GET'])
def redirect_to_url(shortcode):
    """
    Redirect to the original URL based on the shortcode.

    Args:
        shortcode (str): The shortcode to look up.

    Returns:
        Redirect response to the original URL or a 404 error if the shortcode is not found.
    """

    data = url_data.get(shortcode)

    if not data:
        return jsonify({"error": "Shortcode not found"}), 404

    data["lastRedirect"] = datetime.datetime.now().isoformat()
    data["redirectCount"] += 1

    return redirect(data["url"], code=302)


@app.route('/<shortcode>/stats', methods=['GET'])
def get_stats(shortcode):
    """
    Get statistics for a given shortcode.

    Args:
        shortcode (str): The shortcode to get statistics for.

    Returns:
        JSON response with the statistics or a 404 error if the shortcode is not found.
    """

    data = url_data.get(shortcode)

    if not data:
        return jsonify({"error": "Shortcode not found"}), 404

    stats = {
        "created": data["created"],
        "lastRedirect": data["lastRedirect"],
        "redirectCount": data["redirectCount"]
    }

    return jsonify(stats), 200


if __name__ == '__main__':
    app.run(debug=True)
