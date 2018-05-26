from flask import Flask, request, jsonify
from classes import Predict
from functions import split_string_new_issue, get_accuracy

app = Flask(__name__)


@app.route('/check', methods=['POST'])
def parse_request():

    text = request.form
    
    if len(text) == 0 or len(text) > 1 or 'content' not in text.keys():
        return jsonify(
            success=False,
            message='В запросе должен быть только параметр content'
                    ), 400

    if not text['content']:
        return jsonify(
            success=False,
            message='Параметр content пуст'
                    ), 400

    if len(text['content']) > 1000:
        return jsonify(
            success=False,
            message='Параметр content должен содержать не более 1000 символов'
                    ), 400

    if len(split_string_new_issue(text['content'])) < 2:
        return jsonify(
            success=False,
            message='Параметр content должен содержать не меньше двух слов',
                    ), 400

    sub = Predict()
    accuracy = get_accuracy()

    return jsonify(
        success=True,
        result=(sub.predict(text['content'])
                ),
        algorithm_accuracy=accuracy), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
