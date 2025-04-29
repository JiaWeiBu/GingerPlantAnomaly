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
GingerPlantAnomaly is a general-purpose project designed to address the challenges of image anomaly detection. This project provides a flexible framework that can be adapted to various domains, including industrial inspection, medical imaging, agriculture, and more. By leveraging state-of-the-art libraries such as PyCaret, Anomalib, and Ollama VLM, it offers robust and efficient solutions for detecting anomalies in images.

The project is built with scalability and modularity in mind, allowing users to experiment with different anomaly detection techniques and customize the pipeline to suit their specific needs. Whether you are working with RGB images, grayscale images, or specialized datasets, GingerPlantAnomaly provides the tools to preprocess, train, and evaluate models effectively.

One of the key strengths of this project is its ability to integrate multiple anomaly detection models, such as PaDiM and PatchCore, and compare their performance. Additionally, the inclusion of Ollama VLM enables the exploration of vision-language models for anomaly detection, opening up new possibilities for innovative applications.

This repository is designed to be user-friendly, with clear documentation and examples to help users get started quickly. Whether you are a researcher, developer, or practitioner, GingerPlantAnomaly aims to provide a comprehensive solution for your anomaly detection needs.

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
  - **CFLOW**: Conditional Normalizing Flows
  - **CSFLOW**: Cross-Scale-Flows
  - **DRÆM**: Discriminatively Trained Reconstruction Anomaly Embedding Model
  - **DFKDE**: Deep Feature Kernel Density Estimation
  - **DFM**: Deep Feature Modelling
  - **DSR**: Dual Subspace Re-Projection
  - **EFFICIENT_AD**: Efficient Anomaly Detection
  - **FASTFLOW**: Fast Flow
  - **FRE**: Feature Reconstruction Error
  - **GANOMALY**: Generative Adversarial Networks for Anomaly Detection
  - **PADIM**: Patch Distribution Modeling
  - **PATCHCORE**: PatchCore
  - **REVERSE_DISTILLATION**: Reverse Distillation
  - **RKDE**: Region-Based Kernel Density Estimation
  - **STFPM**: Student-Teacher Feature Pyramid Matching
  - **UFLOW**: U-shaped Normalizing Flow
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