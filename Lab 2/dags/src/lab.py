import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
from sklearn.datasets import load_iris
import pickle
import os
import base64

def load_data():
    """
    Loads Iris dataset, serializes it, and returns the serialized data.
    Returns:
        str: Base64-encoded serialized data (JSON-safe).
    """
    print("Loading Iris dataset")
    # Load the Iris dataset
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target  
    
    serialized_data = pickle.dumps(df)                   
    return base64.b64encode(serialized_data).decode("ascii") 

def data_preprocessing(data: str):
    """
    Deserializes base64-encoded pickled data, performs preprocessing,
    and returns base64-encoded pickled clustered data.
    """
    
    data_bytes = base64.b64decode(data)
    df = pickle.loads(data_bytes)

    df = df.dropna()
    # Use all 4 features from Iris dataset for clustering
    clustering_data = df[["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"]]

    min_max_scaler = MinMaxScaler()
    clustering_data_minmax = min_max_scaler.fit_transform(clustering_data)

    
    clustering_serialized_data = pickle.dumps(clustering_data_minmax)
    return base64.b64encode(clustering_serialized_data).decode("ascii")


def build_save_model(data: str, filename: str):
    """
    Builds a KMeans model on the preprocessed data and saves it.
    Returns the SSE list.
    """
   
    data_bytes = base64.b64decode(data)
    df = pickle.loads(data_bytes)

    kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
    sse = []
    for k in range(1, 50):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df)
        sse.append(kmeans.inertia_)

  
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "wb") as f:
        pickle.dump(kmeans, f)

    return sse  


def load_model_elbow(filename: str, sse: list):
    """
    Loads the saved model and uses the elbow method to report k.
    Returns the first prediction (as a plain int) for test data.
    """
    # load the saved (last-fitted) model
    output_path = os.path.join(os.path.dirname(__file__), "../model", filename)
    loaded_model = pickle.load(open(output_path, "rb"))

    # elbow for information/logging
    kl = KneeLocator(range(1, 50), sse, curve="convex", direction="decreasing")
    print(f"Optimal no. of clusters: {kl.elbow}")

 
    iris = load_iris()
    test_data = iris.data[0:1]  
    
    # Scale the test data using the same scaler approach
    min_max_scaler = MinMaxScaler()
    test_data_scaled = min_max_scaler.fit_transform(test_data)
    
    pred = loaded_model.predict(test_data_scaled)[0]


    try:
        return int(pred)
    except Exception:
   
        return pred.item() if hasattr(pred, "item") else pred
