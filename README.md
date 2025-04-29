# GingerPlantAnomaly

An unsupervised ginger plant anomaly detection model.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Setup and Dataset](./README_setup.md)
- [Training and Testing](./README_traintest.md)
- [Results](./results/README.md)
- [Class Documentation](./classes/README.md)
- [Discord UI](./README_discord.md)
- [License](./LICENSE)

## Introduction
GingerPlantAnomaly is a general-purpose project designed to address the challenges of image anomaly detection, with a specific focus on detecting anomalies in ginger plants. Anomalies in ginger plants can include defects such as discoloration, deformities, or other irregularities that may affect their quality. This project aims to provide a robust and efficient solution for identifying such anomalies, which is critical for applications in agriculture, food processing, and quality control.

The project provides a flexible framework that can be adapted to various domains beyond agriculture, including industrial inspection and medical imaging. By leveraging state-of-the-art libraries such as PyCaret, Anomalib, and Ollama VLM, GingerPlantAnomaly offers a modular and scalable approach to anomaly detection. These libraries enable the use of advanced machine learning and deep learning techniques, ensuring high accuracy and reliability in detecting anomalies.

The project primarily focuses on the **Anomalib** library, as it has produced the best results for anomaly detection in ginger plants. Among the models available in Anomalib, the following have been selected for their superior performance:
- **CFLOW**: Conditional Normalizing Flows 
- **FASTFLOW**: Fast Flow 
- **PATCHCORE**: PatchCore 
- **REVERSE_DISTILLATION**: Reverse Distillation 
- **STFPM**: Student-Teacher Feature Pyramid Matching 

These models were chosen based on their ability to handle complex datasets and their effectiveness in identifying subtle anomalies in images. The modular design of the project allows users to experiment with these models and customize the pipeline to suit their specific needs.

In addition to its technical capabilities, GingerPlantAnomaly is designed to be user-friendly. The repository includes clear documentation, example scripts, and a Discord bot UI for managing anomaly detection tasks interactively. This makes it accessible to a wide range of users, from researchers and developers to practitioners in the field.

For example images of ginger plant anomalies and their detection results, refer to the following:
- [Example Image 1](./images/example1.png)
- [Example Image 2](./images/example2.png)
- [Example Image 3](./images/example3.png)

By providing a comprehensive solution for anomaly detection, GingerPlantAnomaly aims to contribute to advancements in quality control and automation across various industries. Whether you are working with agricultural products, industrial components, or medical images, this project offers the tools and flexibility needed to achieve your goals.

## Features
### PyCaret
- [PyCaret](https://pycaret.org/) is a low-code machine learning library that simplifies anomaly detection.
- Documentation: [PyCaret Anomaly Detection](https://pycaret.readthedocs.io/en/stable/api/anomaly.html)
- GitHub: [PyCaret GitHub Repository](https://github.com/pycaret/pycaret/tree/master)
- Supported Models:
  - `'abod'` - Angle-base Outlier Detection
  - `'cluster'` - Clustering-Based Local Outlier
  - `'cof'` - Connectivity-Based Outlier Factor
  - `'histogram'` - Histogram-based Outlier Detection
  - `'iforest'` - Isolation Forest
  - `'knn'` - k-Nearest Neighbors Detector
  - `'lof'` - Local Outlier Factor
  - `'svm'` - One-class SVM detector
  - `'pca'` - Principal Component Analysis
  - `'mcd'` - Minimum Covariance Determinant
  - `'sod'` - Subspace Outlier Detection
  - `'sos'` - Stochastic Outlier Selection

### Anomalib
- [Anomalib](https://github.com/open-edge-platform/anomalib) is a library for anomaly detection using deep learning.
- Documentation: [Anomalib Documentation](https://anomalib.readthedocs.io/en/v2.0.0/)
- Models: [Anomalib Models](https://anomalib.readthedocs.io/en/v2.0.0/markdown/guides/reference/models/index.html)
- Supported Models:
  - **AI_VAD**: Accurate and Interpretable Video Anomaly Detection
  - **CFA**: Coupled-hypersphere-based Feature Adaptation
  - **CFLOW**: Conditional Normalizing Flows 🟢
  - **CSFLOW**: Cross-Scale-Flows
  - **DRÆM**: Discriminatively Trained Reconstruction Anomaly Embedding Model
  - **DFKDE**: Deep Feature Kernel Density Estimation
  - **DFM**: Deep Feature Modelling
  - **DSR**: Dual Subspace Re-Projections
  - **EFFICIENT_AD**: Efficient Anomaly Detection
  - **FASTFLOW**: Fast Flow 🟢
  - **FRE**: Feature Reconstruction Error
  - **GANOMALY**: Generative Adversarial Networks for Anomaly Detection
  - **PADIM**: Patch Distribution Modeling
  - **PATCHCORE**: PatchCore 🟢
  - **REVERSE_DISTILLATION**: Reverse Distillation 🟢
  - **RKDE**: Region-Based Kernel Density Estimation
  - **STFPM**: Student-Teacher Feature Pyramid Matching 🟢
  - **UFLOW**: U-shaped Normalizing Flow
  - **VLM_AD**: Visual Language Model for Anomaly Detection
  - **WIN_CLIP**: Windowed-Based Contrastive Language-Image Pre-training
- Example Results:
  - [CFLOW Result](./images/cflow_result.png)
  - [FASTFLOW Result](./images/fastflow_result.png)
  - [PATCHCORE Result](./images/patchcore_result.png)
- **Note**: This project uses version `1.2.0` of Anomalib. The latest version (`2.0.0`) is not compatible with the current implementation.

### Ollama VLM
- [Ollama VLM](https://ollama.com/) is a vision-language model library for advanced anomaly detection.
- Models: [Ollama Models](https://ollama.com/library)
- GitHub: [Ollama Python SDK](https://github.com/ollama/ollama-python)
- Supported Models:
  - **WIN_CLIP**: Windowed-Based Contrastive Language-Image Pre-training
  - **LLaVA-phi3**
  - **moondream**
  - **minicpm-v**
  - **bakllava**
  - **LLaVA-llama3**
  - **LLaVA**

## Training and Testing Status
- **PyCaret**:
  - Training: Done (File-based execution, no UI, no latest dataset input sequence).
  - Testing: **Not Yet Done**.
- **Anomalib**: File-based and API based. Discord UI. Latest Dataset Input Sequence.
  - Training: Done.
  - Testing: Done.
- **Ollama VLM**:
  - Preliminary implementation for training and testing.

## Installation

### Software Requirements
1. Install [Ollama](https://ollama.com/) if you plan to use Ollama VLM for anomaly detection.
2. Install Python version `3.11.9`. You can download it from the [official Python website](https://www.python.org/).

### Python Dependencies
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/GingerPlantAnomaly.git
   cd GingerPlantAnomaly
   ```
2. Install the required dependencies using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### Environment and Configuration
Details about preparing the `.env` file, setting up the Discord bot, and organizing the dataset can be found in the [Setup and Dataset README](./README_setup.md).

### Important Notes
- This project uses **Anomalib version `1.2.0`**. The latest version (`2.0.0`) is not compatible with the current codebase.
- For more information on setting up the environment and configuration, refer to the [Setup and Dataset README](./README_setup.md).

## Usage
This project is implemented using Object-Oriented Programming (OOP) principles. All core functionalities are encapsulated in classes, which can be found in the [`classes`](./classes/README.md) folder. The classes act as a package, providing modular and reusable components for anomaly detection.

Additionally, the `channel_template.py` file serves as a factory for implementing a one-server chat room bot. It allows the creation of OOP-based bot command rooms, where each room can have its own set of command words to interact with the bot. This design ensures flexibility and scalability for managing bot interactions.

For more details on the Discord bot UI and its functionality, refer to the [Discord UI README](./README_discord.md).

Refer to the [Setup and Dataset](./README_setup.md) and [Training and Testing](./README_traintest.md) documentation for detailed usage instructions.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.