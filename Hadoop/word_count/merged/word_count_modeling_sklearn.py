import pandas as pd
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

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

# Extract features and labels
def extract_features_labels(df, feature_exclude=['Datetime', 'Anomaly'], label_col='Anomaly'):
    X = df.drop(columns=feature_exclude)
    y = df[label_col].astype(int)
    return X, y

# Evaluate and print model performance
def evaluate_model(y_true, y_pred, model_name, process_time):
    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
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
    df = load_and_prepare_data('parsed-word-count-aggregated.csv')
    
    # Split data
    train_df, val_df, test_df = split_data(df)
    
    # Extract features and labels
    X_train, y_train = extract_features_labels(train_df)
    X_val, y_val = extract_features_labels(val_df)
    X_test, y_test = extract_features_labels(test_df)
    
    # Models to train
    models = {
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
    }
    
    # Train, predict, and evaluate each model
    print('~' * 40)
    for model_name, model in models.items():
        start_time = time.time()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        end_time = time.time()  # End timing

        process_time = end_time - start_time
        evaluate_model(y_test, y_pred, model_name, process_time)

# Run the pipeline
if __name__ == "__main__":
    main()
