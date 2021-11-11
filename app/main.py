# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask
from flask import request
from google.api_core.client_options import ClientOptions
import googleapiclient.discovery

import os

REGION = '' # put your region here
PROJECT_ID = '' # put your project id here
VERSION_NAME = 'v1_0'
MODEL_NAME = '' # put your model name here

client_options = ClientOptions(api_endpoint='https://{}-ml.googleapis.com'.format(REGION))
service = googleapiclient.discovery.build('ml', 'v1',
    client_options=client_options)
name = 'projects/{}/models/{}'.format(PROJECT_ID, MODEL_NAME)
name += '/versions/{}'.format(VERSION_NAME)

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def form():
    """Return a form for inputting the penguin's measurements."""
    html = '''
        Penguin classifier<br>
        <form action="predict" method="post">
            Bill length [mm]: <input type="text" name="bill_length_mm" value="39.1"></input></br>
            Bill depth [mm]: <input type="text" name="bill_depth_mm" value="18.7"></input></br>
            Flipper length [mm]: <input type="text" name="flipper_length_mm" value="181.0"></input></br>
            Body mass [g]: <input type="text" name="body_mass_g" value="3750.0"></input></br>
            <input type="submit">
        </form>
    '''
    return html

@app.route('/predict',methods=['POST'])
def predict():
    """Run a prediction."""
    species = {0:'Adelie',1:'Chinstrap',2:'Gentoo'}
    data = [[
        float(request.form['bill_length_mm']),
        float(request.form['bill_depth_mm']),
        float(request.form['flipper_length_mm']),
        float(request.form['body_mass_g']),
    ]] 
    responses = service.projects().predict(
        name=name,
        body={'instances': data}
    ).execute()

    if 'error' in responses:
        return 'error: ' + str(responses['error'])

    return species[responses['predictions'][0]]

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
