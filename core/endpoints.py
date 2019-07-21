import windows_tracker
import webbrowser
from flask import Flask, request, json
from flask import render_template

# import os
app = Flask(__name__, template_folder='template')

webbrowser.open_new('http://localhost:5000')

study_time = 0

@app.route('/')
def index():
    return render_template('index.html')
    # pass
    # return "Hello"
    # return render_template("index.html", user="Petros")


@app.route('/user_information')
def user_info():
    return render_template('inputpage.html')


@app.route('/startapp')
def startapp():
    # os.system("python windows_tracker.py")
    windows_tracker.run(study_time)
    return render_template('success.html')


@app.route('/dataendpoint', methods=['POST'])
def getFormData():
    # TODO: Add key values to file which have the on value.

    if request.method == 'POST':
        blacklist_file = open("blacklist.txt", "w")
        data = request.form
        #
        # for obj in data.keys():
        #     if obj.get() == 'on':
        #
        ninegag = data.get('9gag')
        facebook = data.get('facebook')

        wow = data.get('WoW')
        fortnite = data.get('fortnite')
        graph = data.get('graph')
        info = data.get('info')
        instagram = data.get('instagram')
        minecraft = data.get('minecraft')
        messenger = data.get('messenger')
        tumblr = data.get('tumblr')
        letmewatchthis = data.get('letmewatchthis')
        netflix = data.get('netflix')
        steam = data.get('steam')
        epic = data.get('epic')

        num_cycle = data.get('num_cycle')
        study_time = float(data.get('study_time'))

        print("Duration: %f " % study_time)

        break_time = data.get('break_time')

        blcllst = ['9gag', 'twitter', 'tumblr', 'instagram', 'World of Warcraft', 'minecraft', 'fortnite',
                   'letmewatchthis', 'netflix', 'steam', 'epic', 'facebook', 'messenger']
        kys = data.keys()
        print(kys)

        for key in kys:
            if key in blcllst:
                blacklist_file.write(key + "\n")

        blacklist_file.close()
        # return data
        return render_template('success.html', name=data)
    else:
        return "Post endpoint."


if __name__ == '__main__':
    app.run(debug=True)
