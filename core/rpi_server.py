from flask import request, app, Flask

app = Flask(__name__)

@app.route('/matrixdata', methods=['POST'])
def matrix_data():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        matrix = float(data.get('matrix'))
        rgb = float(data.get('rgb'))

        return {'rgb': rgb, 'matrix': matrix}

    if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0')