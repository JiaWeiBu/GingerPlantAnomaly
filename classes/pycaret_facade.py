# This file provides a facade interface for integrating PyCaret's anomaly detection capabilities.
# It wraps PyCaret's functionality into a simplified interface, allowing users to easily perform
# anomaly detection tasks such as model training, prediction, and evaluation without dealing with
# low-level PyCaret configurations. This facade abstracts away the complexities of PyCaret,
# making it user-friendly for those who need efficient anomaly detection.
"""
Variables naming convention
- GLOBAL_VARIABLE 
- class_variable_
- ClassName
- variable_name
- k_constant_variable
- FunctionName

Class : PyCaretAnomalyFacade
Purpose : A facade class that leverages PyCaret's anomaly detection models. It simplifies the setup,
          training, and usage of anomaly detection models, offering high-level methods that 
          encapsulate the essential PyCaret functions for quick and easy implementation.

Methods :
  - __init__ : Initializes PyCaret settings for anomaly detection.
  - Setup : Sets up the PyCaret environment with the provided dataset.
  - CreateModel : Initializes and trains a specific PyCaret anomaly detection model.
  - AssignModel : Assigns a trained model to the facade for further operations.
  - PlotModel : Generates a plot for the trained model.
  - EvaluateModel : Evaluates the performance of the trained model.
  - PredictModel : Predicts anomalies using the trained model.
  - DeployModel : Deploys the trained model for future use.
  - SaveModel : Saves the trained model to a file.
  - LoadModel : Loads a pre-trained model from a file.
  - Pull : Returns table of models available in the model library.
  - Models : Returns table of models available in the model library.
  - GetLogs : Returns a table of experiment logs. Only works when "log_experiment" is True when initializing the "Setup" function.
  - GetConfig : This function is used to access global environment variables.
  - SetConfig : This function is used to reset global environment variables.
  - SaveExperiment : Saves the experiment to a pickle file.
  - LoadExperiment : Load the experiment from a pickle file.
  - SetCurrentExperiment :
  - GetCurrentExperimetn : 
"""

class PyCaretAnomalyFacade:
    