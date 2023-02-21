import os
import mlflow
import pandas as pd
from pathlib import Path
import joblib



def init():
    global model
    global output_path

    # AZUREML_MODEL_DIR is an environment variable created during deployment
    # It is the path to the model folder
    # Please provide your model's folder name if there's one:
    #model_path = os.path.join(os.environ["AZUREML_MODEL_DIR"], model_path1)
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR", default=""),
                              "model.pkl")
    print(model_path)
    output_path = os.environ['AZUREML_BI_OUTPUT_PATH']
    #model = mlflow.pyfunc.load_model(model_path)
    model = joblib.load(model_path)

def run(mini_batch):
    for file_path in mini_batch:
        data = pd.read_csv(file_path)
        pred = model.predict(data)
        
        data['prediction'] = pred
        
        output_file_name = Path(file_path).stem
        output_file_path = os.path.join(output_path, output_file_name + '.csv')
        data.to_csv(output_file_path)
        
    return mini_batch
