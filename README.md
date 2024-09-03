# Fast Healthcare Interoperability Resources (FHIR) Copilot

## Description

This repository serves as a comprehensive toolbox designed to automize the extraction, mapping, and validation of clinical entities from clinical notes. The toolbox functions as a copilot by leveraging state-of-the-art pretrained language models and established healthcare standards.

### Key Features

1. **Clinical Entity Extraction**: 
   - The toolbox utilizes the pretrained large language model [microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) to extract clinical entities from a given clinical note.
   - The extraction process is guided by the identification of relevant FHIR (Fast Healthcare Interoperability Resources) resource types, ensuring that the entities are categorized and structured according to healthcare standards.

2. **SNOMED CT Term Prediction**:
   - After extracting clinical entities, the toolbox maps these entities to potential corresponding terms from the SNOMED CT terminology.
   - This mapping process involves predicting the most appropriate SNOMED CT term for each entity, facilitating a standardized representation of clinical information.

3. **Entity Matching and Validation**:
   - The mapped entities are further validated by connecting to a SNOMED CT terminology server, specifically snowstorm-lite, which functions as a FHIR server.
   - To enhance the accuracy of the mapping, the toolbox computes cosine similarity scores, representing semantic similarity between the entities and the SNOMED CT terms.
   - This is achieved using the pretrained language model [dmis-lab/biobert-base-cased-v1.1](https://huggingface.co/dmis-lab/biobert-base-cased-v1.1), which is specialized in the biomedical domain. The model helps in identifying the most relevant and accurate match for each clinical entity.

This toolbox is designed to streamline the process of clinical data standardization, making it easier for healthcare systems to achieve interoperability and improve the accuracy of clinical documentation.

## Project Structure

The project is organized into the following directories and files:

### `/frontend`
- **Description**: This directory contains the Vue.js application that serves as the frontend for the toolbox.
- **Contents**: 
  - All Vue.js components, assets, and configuration files necessary to build and run the frontend of the application.

### `/model_cache`: 

#### (Note: If this directory does not exist, please create a new folder named `model_cache` and download and place both [Phi-3-mini-4k-instruct](https://drive.google.com/drive/folders/1nZlwLlidMqp_Pw-MhLT7y6TVHEU9Y72N?usp=sharing) and [biobert-base-cased-v1.1](https://drive.google.com/drive/folders/1SUbpT7rSLpK9XYfHy1BPsKMzzcHBzOQy?usp=sharing) into this folder. This step prevents the models from being automatically downloaded during runtime, reducing the time required to run the application.)
- **Description**: This directory includes downloaded pretrained models from Hugging Face.
- **Contents**: 
  - The pretrained models and tokenizers that are used for text generation and text embedding processes. Caching these models locally helps avoid repeated downloads, enhancing performance and reducing latency.

### `main.py`
- **Description**: This file sets up the FastAPI application that provides the backend API services.
- **Key Functions**:
  - **Endpoints**: Provides endpoints for:
    - Extracting prompts.
    - Chatting.
    - Mapping entities to SNOMED CT.
    - Validating entities with SNOMED CT.
  - **Technologies**: Utilizes Pydantic models for data validation, CORS middleware for handling cross-origin requests, and functions for generating chat completions and interacting with SNOMED CT.
  - **Execution**: The application is run using Uvicorn, a lightning-fast ASGI server.

### `completion_phi.py`
- **Description**: This script sets up a text generation pipeline using a pretrained model and tokenizer from the transformers library.
- **Key Functions**:
  - **Text Generation**: Defines a function `create_chat_completion` that generates text completions based on a list of prompts.
  - **Model Caching**: The model and tokenizer are cached locally to optimize performance and reduce the need for repeated downloads.
  - **Generation Control**: Specific generation arguments are used to control the output of the text generation process.

### `get_snomed.py`
- **Description**: This script defines functions for embedding text using a pretrained BioBERT model and interacting with SNOMED CT terminology.
- **Key Functions**:
  - **Text Embedding**: Embeds text using the BioBERT model to facilitate semantic similarity calculations.
  - **SNOMED CT Retrieval**: Retrieves SNOMED CT terms from a FHIR server.
  - **Cosine Similarity Calculation**: Computes the cosine similarity between embeddings to find the most relevant SNOMED CT terms.
  - **Model Caching**: Similar to `completion_phi.py`, the model and tokenizer are cached locally to optimize performance.

### `docker-compose.yml`
- **Description**: This file contains the Docker Compose configuration for setting up the project’s services.
- **Key Features**:
  - **Docker Setup**: Builds Docker images for both frontend and backend services.
  - **Service Communication**: Starts containers, allowing the frontend to communicate with the backend using the service name `backend` as the hostname.

### `clinical_text_examples.txt`
- **Description**: A file containing 10 synthetic examples of clinical texts.
- **Purpose**:
  - **Testing**: These examples can be used to test and demonstrate the functionality of the toolbox.

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git): Required for cloning the repository.
- [Docker](https://docs.docker.com/engine/install/) and Docker Compose: Required for containerizing and running the application.
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html): Necessary for utilizing GPU acceleration within Docker containers.

#### In the Case of Running Without Docker:

- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html): Required for managing Python environments and dependencies.
- [Node.js](https://nodejs.org/en/) (version 14 or higher recommended) and npm (comes with Node.js): Required for running the frontend built with Vue.js.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/omidvosoughi/fast-healthcare-interoperability-resources-copilot.git
   cd fast-healthcare-interoperability-resources-copilot
   ```

2. **Build and Run**:

- Using Docker Compose:
  - On Linux:
  ```bash
  sudo docker-compose up --build
  ```
  - On Windows: 
  ```bash
  docker-compose up --build
  ```
- Without Docker:
  - Create an Environment:
  ```bash
  conda create -n fhir_copilot python=3.10.14
  ```
  - Activate the Environment:
  ```bash
  conda activate fhir_copilot
  ```
  - Install the Backend Requirements:
  ```bash
  pip install -r requirements.txt
  ```
  - Install the Frontend:
  ```bash
  cd frontend
  npm install
  ```
  - Running the Frontend:
  ```bash
  npm run serve
  ```
  - Running the Backend:
  ```bash
  cd ..
  uvicorn main:app --reload
  ```

3. **Access the Application**

Open your web browser and navigate to `http://localhost:8080` to access the frontend.

## Usage

To test the application, you can use one of the clinical notes provided in the `clinical_text_examples.txt` file. This file contains 10 synthetic examples of clinical texts that you can copy and use to evaluate the functionality of the toolbox.

### Steps to Test:

1. **Start the Application**:
   - Ensure that the frontend and backend services are running either through Docker or by manually starting them as described in the installation steps.

2. **Copy a Clinical Note**:
   - Open the `clinical_text_examples.txt` file located in the root directory of the project.
   - Select and copy one of the clinical notes provided in the file.

3. **Use the Frontend Interface**:
   - Navigate to the frontend application in your web browser (e.g., `http://localhost:8080`).
   - Paste the copied clinical note into the designated input area.

4. **Run the Extraction and Mapping**:
   - Submit the clinical note using the frontend interface to trigger the extraction of clinical entities, mapping to SNOMED CT terms, and validation with the SNOMED CT server.

5. **Review the Results**:
   - The application will process the input and display the extracted entities, the corresponding SNOMED CT terms, and the validation results with the corresponding cosine similarity scores.

This process allows you to evaluate the application's capabilities and see how it handles real-world clinical text scenarios.
