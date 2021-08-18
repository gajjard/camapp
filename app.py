from flask import Flask, render_template, request, send_file, make_response
import pandas as pd
import math
import matplotlib.pyplot as plt
import plotly.express as px

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("app.html")


@app.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        h = int(request.form['h'])
        SHMR = int(request.form['SHMR'])
        dwell = int(request.form['dwell'])
        SHMF = int(request.form['SHMF'])
        N = int(request.form['N'])
        dia = int(request.form['dia'])
        dwell2 = 360 - SHMR - SHMF - dwell

        w = N * 2 * math.pi / 60

        # angle
        angle = []
        for i in range(0, 361):
            angle.append(i)

        # SHM Rise
        displacement = []
        velocity = []
        acceleration = []
        jerk = []
        beta = SHMR * (math.pi / 180)
        for i in range(0, SHMR + 1):
            deg = i * (math.pi / 180)
            dis = ((h / 2) * (1 - math.cos((math.pi * deg) / beta)))
            vel = (h / 2) * ((math.pi * w) / beta) * math.sin((math.pi * deg) / beta) * 0.001
            acc = (h / 2) * (((math.pi * w) / beta) ** 2) * math.cos((math.pi * deg) / beta) * 0.001
            j = -1 * (h / 2) * (((math.pi * w) / beta) ** 3) * math.sin((math.pi * deg) / beta) * 0.001
            displacement.append(dis)
            velocity.append(vel)
            acceleration.append(acc)
            jerk.append(j)

        # dwell
        for i in range(SHMR + 2, SHMR + dwell + 2):
            f = h
            vel = 0
            acc = 0
            j = 0
            displacement.append(f)
            velocity.append(vel)
            acceleration.append(acc)
            jerk.append(j)

        # SHM Fall
        j = 0
        beta = SHMF * (math.pi / 180)
        for i in range(SHMR + dwell + 2, SHMR + dwell + SHMF + 2):
            deg = (SHMF - j) * (math.pi / 180)
            dis = ((h / 2) * (1 - math.cos((math.pi * deg) / beta)))
            vel = -1 * (h / 2) * ((math.pi * w) / beta) * math.sin((math.pi * deg) / beta) * 0.001
            acc = (h / 2) * (((math.pi * w) / beta) ** 2) * math.cos((math.pi * deg) / beta) * 0.001
            j1 = (h / 2) * (((math.pi * w) / beta) ** 3) * math.sin((math.pi * deg) / beta) * 0.001
            j = j + 1
            displacement.append(dis)
            velocity.append(vel)
            acceleration.append(acc)
            jerk.append(j1)

        # dwell2
        for i in range(SHMR + dwell + SHMF + 2, SHMR + dwell + SHMF + dwell2 + 2):
            f = 0
            vel = 0
            acc = 0
            j = 0
            displacement.append(f)
            velocity.append(vel)
            acceleration.append(acc)
            jerk.append(j)

        dummy = []
        for i in range(0, 361):
            val = dia / 2
            dummy.append(val)

        dict1 = {'Cam_radius': dummy, 'angles': angle, 'displacement': displacement, 'velocity': velocity,
                 'acceleration': acceleration, 'jerk': jerk}

        df = pd.DataFrame(dict1)

        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"

        fig = px.line(x=angle, y=displacement, labels={'x': "Theta (θ)", 'y': 'Displacement (mm)'})
        fig2 = px.line(x=angle, y=velocity, labels={'x': "Theta (θ)", 'y': 'Velocity (mm/s)'})
        fig3 = px.line(x=angle, y=acceleration, labels={'x': "Theta (θ)", 'y': 'acceleration (mm/s²)'})
        fig4 = px.line(x=angle, y=jerk, labels={'x': "Theta (θ)", 'y': 'Jerk (mm/s³)'})
        fig.show()
        fig2.show()
        fig3.show()
        fig4.show()
        return resp

    else:
        return render_template('app.html')


if __name__ == "__main__":
    app.run(debug=True)
