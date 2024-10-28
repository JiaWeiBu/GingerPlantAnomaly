# unsupervised anomaly detection model
# Isolation Forest with pycaret

# import libraries
import pycaret.anomaly as anomaly_model
from pycaret.datasets import get_data

data = get_data('anomaly')

exp = anomaly_model.setup(data=data, normalize=True, use_gpu=True)

model = anomaly_model.create_model('knn', fraction=0.1)

anomaly_model.evaluate_model(model)

predictions = anomaly_model.predict_model(model=model, data=data)

# save predictions into a csv file
predictions.to_csv('predictions.csv')

anomaly_model.save_model(model, 'knn_model')
