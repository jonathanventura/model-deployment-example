# Google Cloud ML model deployment example
This repo provides a simple example of deploying a machine learning model with Google Cloud AI Platform and App Engine.

By deploying a model, you can make the model available to end users through a public interface, or integrate model into a larger system that will use its predictions in some way.

Google Cloud currently supports deployment of Tensorflow, Scikit-Learn, and XGBoost models.

### Creating the ML model with scikit-learn

Run `create_ml_model.ipynb` to create the model file (model.joblib).  You will need to upload this file to a Google Cloud Storage bucket.

### Deploying the model to AI Platform

Install and initialize the [Cloud SDK](https://cloud.google.com/sdk/docs/install).

Authorize the SDK: `gcloud auth login`

You also need to enable the AI Platform Training & Prediction API through the Google Cloud console.

First, create a model in the AI Platform.  You need to specify the project, region, and model name.

    gcloud ai-platform models create <model name> --region <region> --project <project name>
    
Now you are ready to create your first model version:

    gcloud ai-platform versions create <version> \
     --project <project name> \
     --model <model name> \
     --origin=gs://<bucket name>/<folder containing model file> \
     --runtime-version=2.6 \
     --framework=scikit-learn \
     --python-version=3.7 \
     --region=<region> \
     --machine-type=n1-standard-2

This can take several minutes.

### Testing the model

You can interact with the model through a REST api.  Google provides a Python API to make this easy.
First, create the service object:

    from google.api_core.client_options import ClientOptions
    import googleapiclient.discovery

    client_options = ClientOptions( api_endpoint=f'https://{REGION}-ml.googleapis.com')
    service = googleapiclient.discovery.build('ml', 'v1', client_options=client_options)
    
    f'projects/{PROJECT_ID}/models/{MODEL_NAME}'
    name += f'/versions/{VERSION_NAME}'

    data = [[ 39.1,18.7,181.0,3750.0 ]] # example row from penguins dataset
    responses = service.projects().predict(
        name=name,
        body={'instances': data}
    ).execute()

### Creating a simple web app with App Engine

Now you can run ML predictions from a web app in Flask.

Before you start, be sure to activate the [Cloud Build API](https://console.cloud.google.com/flows/enableapi?apiid=cloudbuild.googleapis.com&_ga=2.28942524.1043283823.1636399520-1345860708.1538421268).

First, create the app:

    gcloud app create --project <project name> --region <region>
    
In the `app` directory, modify `main.py` and specify your region, project ID, and model name.  Then run `gcloud app deploy`.  Then you should be able to access the web app in your web browser -- `glcoud app browse` will pull up the page for you.



