# Define a Flask app to host the webservice for returning the concepts of input strings.

from flask import Flask, request, abort, make_response, jsonify
from flask.ext.cache import Cache
from concept_store import ConceptStore

# Define the webapp
app = Flask(__name__)
# Initialise a cache used to store the concept store
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@cache.cached(timeout=3600)
def get_concept_store():
    """
    Build and return the concept store and keep it in cache for a day.
    """
    return ConceptStore(
        ['Indian',
         'Thai',
         'Sushi',
         'Caribbean',
         'Italian',
         'West Indian',
         'Pub',
         'East Asian',
         'BBQ',
         'Chinese',
         'Portuguese',
         'Spanish',
         'French',
         'East European'])


@app.route('/vq', methods=['POST'])
def vq_post():
    """
    Method to process POST request to /vq

    :return:
        - A the matched concepts in the given string as a list in a json object:
          {result:[list_of_matches]}
        - 400: if request data is not plain text.
    """
    if request.headers['Content-Type'] == 'text/plain':
        # Process the input string and return the matches
        string = str(request.data)
        print string
        matches = get_concept_store().find_matches(str(request.data))
        return jsonify({'result':matches})
    else:
        # Return a 400 error
        abort(make_response("Content was not a plain string", 400))


@app.route('/vq', methods=['GET'])
def vq_get():
    """
    Method to process GET requests to /vq

    :return:
        A message instructing to use POST requests.
    """
    return 'VQ is a webservice where you can POST a string, and which will return a json with concept matches for the given string'


if __name__ == "__main__":
    # Run the webapp
    app.run()