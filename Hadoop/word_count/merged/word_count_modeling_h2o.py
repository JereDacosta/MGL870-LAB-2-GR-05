import h2o
import logging
import pandas as pd
import time
from h2o.frame import H2OFrame
from h2o.estimators.random_forest import H2ORandomForestEstimator
from h2o.estimators.glm import H2OGeneralizedLinearEstimator
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

# Initialize H2O
h2o.init()

logging.getLogger("py4j").setLevel(logging.ERROR)
h2o.no_progress()

# Load and preprocess the data
def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.sort_values(by='Datetime')
    return df

# Split data into train, validation, and test sets
def split_data(df, train_frac=0.6, val_frac=0.2):
    train_size = int(train_frac * len(df))
    val_size = int(val_frac * len(df))
    
    train_data = df.iloc[:train_size]
    val_data = df.iloc[train_size:train_size + val_size]
    test_data = df.iloc[train_size + val_size:]
    
    return train_data, val_data, test_data

# Convert Pandas DataFrame to H2O Frame
def to_h2o_frame(df, feature_exclude=['Datetime', 'Anomaly'], label_col='Anomaly'):
    features = df.drop(columns=feature_exclude)
    labels = df[label_col].astype(int)
    h2o_df = h2o.H2OFrame(pd.concat([features, labels], axis=1))
    h2o_df[label_col] = h2o_df[label_col].asfactor()  # Ensure target is categorical
    return h2o_df

# Evaluate and print model performance
def evaluate_model(y_true, y_pred, model_name, process_time):
    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred),
        "AUC": roc_auc_score(y_true, y_pred),
    }
    
    print(f"{model_name} Performance:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")
    print(f"Process Time: {process_time:.2f} seconds")
    print('~' * 40)

# Main processing
def main():
    # Load data
    df = load_and_prepare_data('parsed-word-count-aggregated_3_mins.csv')
    
    # Split data
    train_df, val_df, test_df = split_data(df)
    
    # Convert to H2O frames
    train_h2o = to_h2o_frame(train_df)
    val_h2o = to_h2o_frame(val_df)
    test_h2o = to_h2o_frame(test_df)
    
    # Define features and target
    features = list(train_df.drop(columns=['Datetime', 'Anomaly']).columns)
    target = 'Anomaly'
    
    # Models to train
    models = {
        "Random Forest": H2ORandomForestEstimator(ntrees=50, max_depth=20, seed=1234),
        "Logistic Regression": H2OGeneralizedLinearEstimator(family="binomial"),
        "Decision Tree": H2OGradientBoostingEstimator(ntrees=1, max_depth=5, seed=1234),  # Simplified GBM as Decision Tree
    }
    
    # Train, predict, and evaluate each model
    print('~' * 40)
    for model_name, model in models.items():
        start_time = time.time()
        model.train(x=features, y=target, training_frame=train_h2o, validation_frame=val_h2o)
        predictions = model.predict(test_h2o).as_data_frame()['predict'].astype(int)
        end_time = time.time()
        
        process_time = end_time - start_time
        evaluate_model(test_df['Anomaly'], predictions, model_name, process_time)

# Run the pipeline
if __name__ == "__main__":
    main()
