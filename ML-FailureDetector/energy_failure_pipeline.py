import os
import numpy as np
import requests
import pandas as pd
import joblib
from prefect import task, flow
from datetime import datetime
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@task
def create_timestamped_folder():
    timestamp = pd.Timestamp.now().strftime('%Y%m%d%H%M%S')
    folder_path = os.path.join('results', timestamp)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

@task(retries=20, retry_delay_seconds=10)
def verify_system_online(folder_path):
    system_check_url = 'http://127.0.0.1:9088/StatusPing'
    try:
        response = requests.get(system_check_url)
        state = response.json().get('state', '')
        log_message = f"{datetime.now()} - INFO - System check successful, state: {state}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        return response.status_code == 200 and state == 'RUNNING'
    except requests.RequestException as e:
        log_message = f"{datetime.now()} - ERROR - Failed to verify system online: {e}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        raise e

@task(retries=20, retry_delay_seconds=10)
def check_device_state(folder_path):
    device_state_url = 'http://127.0.0.1:9088/system/webdev/ML/check_device_state'
    try:
        response = requests.get(device_state_url)
        state = response.json().get('state', '')
        log_message = f"{datetime.now()} - INFO - Device check successful, state: {state}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        return response.status_code == 200 and state == 'running'
    except requests.RequestException as e:
        log_message = f"{datetime.now()} - ERROR - Failed to check device state: {e}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        raise e

@task(retries=20, retry_delay_seconds=10)
def check_database_state(folder_path):
    database_state_url = 'http://127.0.0.1:9088/system/webdev/ML/check_database_state'
    try:
        response = requests.get(database_state_url)
        state = response.json().get('state', '')
        log_message = f"{datetime.now()} - INFO - Database check successful, state: {state}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        return response.status_code == 200 and state == 'running'
    except requests.RequestException as e:
        log_message = f"{datetime.now()} - ERROR - Failed to check database state: {e}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        raise e

@task(retries=20, retry_delay_seconds=2)
def get_data(folder_path):
    data_url = 'http://127.0.0.1:9088/system/webdev/ML/get_data'
    try:
        response = requests.get(data_url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        if 't_stamp' in df.columns:
            df.set_index('t_stamp', inplace=True)
        log_message = f"{datetime.now()} - INFO - Data retrieval successful\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        return df
    except requests.RequestException as e:
        log_message = f"{datetime.now()} - ERROR - Failed to get data: {e}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        raise e

@task
def clean_data(df, folder_path):
    if df.empty:
        return df
    df_cleaned = df.replace({np.nan: None})
    df_cleaned = df_cleaned.replace({np.nan: 0})
    
    df_cleaned.to_csv(os.path.join(folder_path, 'power_data.csv'), index=True)
    
    log_message = f"{datetime.now()} - INFO - Data cleaning successful\n"
    with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
        log_file.write(log_message)
    
    return df_cleaned

@task(retries=5, retry_delay_seconds=5)
def load_model(folder_path):
    model_filename = 'trained_random_forest_pipeline_model.pkl'
    feature_names_filename = 'feature_names.pkl'
    try:
        pipeline = joblib.load(model_filename)
        feature_names = joblib.load(feature_names_filename)
        log_message = f"{datetime.now()} - INFO - Model loading successful\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        return pipeline, feature_names
    except Exception as e:
        log_message = f"{datetime.now()} - ERROR - Failed to load model or feature names: {e}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        return None, None

@task
def make_predictions(pipeline, feature_names, df_cleaned, folder_path):
    if pipeline is not None and not df_cleaned.empty:
        try:
            df_cleaned = df_cleaned[feature_names]
            predictions = pipeline.predict(df_cleaned)
            log_message = f"{datetime.now()} - INFO - Predictions made successfully\n"
            with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
                log_file.write(log_message)
            print(predictions)
            return predictions
        except Exception as e:
            log_message = f"{datetime.now()} - ERROR - Failed to make predictions: {e}\n"
            with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
                log_file.write(log_message)
            return None
    else:
        log_message = f"{datetime.now()} - ERROR - Pipeline or data is not available for making predictions\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        return None

@task
def evaluate_pipeline(pipeline, df_cleaned, predictions, folder_path):
    if pipeline is not None and not df_cleaned.empty and predictions is not None:
        try:
            y_true = df_cleaned.pop('cfcfe6/g6failure')
            y_pred = predictions

            f1 = f1_score(y_true, y_pred, average='weighted')
            cm = confusion_matrix(y_true, y_pred)
            if np.all(y_pred == 0):
                cm = np.array([[len(y_true), 0], [0, 0]])
            report = classification_report(y_true, y_pred)

            log_message = f"{datetime.now()} - INFO - Evaluation successful\n"
            with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
                log_file.write(log_message)

            print(report)
            print('F1 Score:', f1)
            print('Confusion Matrix:')
            print(cm)

            return report, f1, cm
        except KeyError as e:
            log_message = f"{datetime.now()} - ERROR - Failed to evaluate pipeline: {e}\n"
            with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
                log_file.write(log_message)
            return None, None, None
    else:
        log_message = f"{datetime.now()} - ERROR - Pipeline or data is not available for evaluation\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
        return None, None, None

@task
def save_metrics(report, f1, cm, folder_path):
    try:
        with open(os.path.join(folder_path, 'metrics.txt'), 'w') as metrics_file:
            metrics_file.write(report)
            metrics_file.write(f'\nF1 Score: {f1}\n')
            metrics_file.write(f'Confusion Matrix:\n{cm}\n')
        
        plt.figure(figsize=(10, 7))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Confusion Matrix')
        plt.colorbar()
        tick_marks = [0, 1]
        labels = ['No Failure', 'Failure']
        plt.xticks(tick_marks, labels)
        plt.yticks(tick_marks, labels)
        plt.xlabel('True label')
        plt.ylabel('Predicted label')

        thresh = cm.max() / 2.
        for i, j in np.ndindex(cm.shape):
            plt.text(j, i, f'{cm[i, j]}',
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.savefig(os.path.join(folder_path, 'confusion_matrix.png'), transparent=True)
        plt.close()

        log_message = f"{datetime.now()} - INFO - Metrics saved successfully\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)
    except Exception as e:
        log_message = f"{datetime.now()} - ERROR - Failed to save metrics: {e}\n"
        with open(os.path.join(folder_path, 'logs.txt'), 'a') as log_file:
            log_file.write(log_message)

@flow(name="Machine Failure Detection")
def prefect_pipeline(run_count: int = 0, max_runs: int = 3):
    folder_path = create_timestamped_folder()

    if run_count >= max_runs:
        print("Maximum number of runs reached.")
        return

    system_online = verify_system_online(folder_path)

    if system_online:
        device_running = check_device_state(folder_path)
        
        if device_running:
            database_online = check_database_state(folder_path)
            
            if database_online:
                df = get_data(folder_path)
                if not df.empty:
                    df_cleaned = clean_data(df, folder_path)
                    pipeline, feature_names = load_model(folder_path)
                    predictions = make_predictions(pipeline, feature_names, df_cleaned, folder_path)
                    report, f1, cm = evaluate_pipeline(pipeline, df_cleaned, predictions, folder_path)
                    if report and f1 and cm is not None:
                        save_metrics(report, f1, cm, folder_path)

    print(f"Run {run_count + 1} completed. Scheduling next run.")
    prefect_pipeline(run_count=run_count + 1, max_runs=max_runs)

if __name__ == "__main__":
    from prefect.deployments import Deployment
    from prefect.client.schemas.schedules import IntervalSchedule
    from prefect.client.schemas.schedules import RRuleSchedule
    from datetime import timedelta
    import argparse

    parser = argparse.ArgumentParser(description='Run the Prefect pipeline with specified interval and max runs.')
    parser.add_argument('--interval_seconds', type=int, default=30, help='Interval in seconds between pipeline runs')
    parser.add_argument('--max_runs', type=int, default=3, help='Maximum number of pipeline runs')

    args = parser.parse_args()

    interval_seconds = args.interval_seconds
    max_runs = args.max_runs
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=interval_seconds * max_runs)

    schedule = RRuleSchedule(
        rrule=f"DTSTART:{start_time.strftime('%Y%m%dT%H%M%SZ')}\nRRULE:FREQ=SECONDLY;INTERVAL={interval_seconds};UNTIL={end_time.strftime('%Y%m%dT%H%M%SZ')}"
    )

    deployment = Deployment.build_from_flow(
        flow=prefect_pipeline,
        name="machine-failure-detection-scheduled",
        schedule=schedule,
    )

    deployment.apply()
    prefect_pipeline(max_runs=max_runs)