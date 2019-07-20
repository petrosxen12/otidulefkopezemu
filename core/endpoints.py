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
        ninegag = data.get('9gag')
        facebook = data.get('facebook')
        wow = data.get('WoW')
        fortnite = data.get('fortnite')
        graph = data.get('graph')
        info = data.get('info')
        instagram = data.get('instagram')
        minecraft = data.get('minecraft')
        tumblr = data.get('tumblr')
        letmewatchthis = data.get('letmewatchthis')
        netflix = data.get('netflix')
        steam = data.get('steam')
        epic = data.get('epic')

        num_cycle = data.get('num_cycle')
        study_time = data.get('study_time')
        break_time = data.get('break_time')

        return data
    else:
        return "Post endpoint."


if __name__ == '__main__':
    app.run(debug=True)
