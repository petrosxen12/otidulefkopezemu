from flask import request, Flask

app = Flask(__name__)


@app.route('/matrixdata', methods=['POST'])
def matrix_data():
    if request.method == 'POST':
        data = request.get_json()
        matrix = float(data.get('matrix'))
        return {'matrix': matrix}

    if request.method == 'GET':
        data = request.get_json()
        rgb = float(data.get('rgb'))
        return {'rgb': rgb}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
