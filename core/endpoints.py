import windows_tracker
from flask import Flask, render_template, url_for, request
from flask import render_template

app = Flask(__name__)
blacklist_file = open("blacklist.txt", "w")

@app.route('/')
def index():
    return render_template('templates/index.html')
    # pass
    # return "Hello"
    # return render_template("index.html", user="Petros")


@app.route('/startapp')
def startapp():
    # os.system("python windows_tracker.py")
    windows_tracker.run()


@app.route('/dataendpoint', methods=['POST'])
def getFormData():
    # TODO: Add key values to file which have the on value.
    if request.method == 'POST':
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
        study_time = data.get('study_time')
        break_time = data.get('break_time')

        blcllst = ['9gag', 'twitter', 'tumblr', 'instagram', 'World of Warcraft', 'minecraft', 'fortnite',
                   'letmewatchthis', 'netflix', 'steam', 'epic']
        kys = data.keys()
        print(kys)

        for key in kys:
            if key in blcllst:
                blacklist_file.write(key + "\n")

        blacklist_file.close()
        return data
    else:
        return "Post endpoint."


if __name__ == '__main__':
    app.run(debug=True)
