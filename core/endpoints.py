import windows_tracker
from flask import Flask, render_template, url_for, request

app = Flask(__name__)


@app.route('/')
def welcome():
    name = request.args.get("name", "hello")
    return name


@app.route('/startapp')
def startapp():
    # os.system("python windows_tracker.py")
    windows_tracker.run()


@app.route('/dataendpoint', methods=['POST'])
def getFormData():
    if request.method == 'POST':
        data = request.form
        messenger = request.form.get('allowMsgr')
        facebook = request.form.get('allowFcbk')
        # facebook = request.form.get('allowFcbk')

        return data
    else:
        return "Post endpoint."


if __name__ == '__main__':
    app.run(debug=True)
