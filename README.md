# Weather Monitoring System

## Overview
This is a Flask-based rule engine application that allows users to create and evaluate rules based on specified conditions. The application features a user-friendly interface for entering rules and data, displaying evaluation results, and visualizing the internal representation of rules.


## Build Instructions

### Prerequisites
- Docker or Podman
- Python 3.12.4
- Flask
- SQLite


### Setup
1. **Clone the repository**
    ```bash
    git clone https://github.com/Syamsundarchegu/Zepto_ast_project.git

    ```

2. **Create a virtual environment**
    ```bash

    conda create -name zepto_ast #For creating a virtual environment
    conda activate zepto_ast  #For activating the virtual environment
    conda deactivate zepto_ast  #For deactivating the virtual environment

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**
    ```bash
    python app.py  # This will initialize the database
    ```

5. **Run the application**
    ```bash
    python app.py
    ```

6. **Access the application**
    Open your web browser and go to `http://127.0.0.1:3000`.


### Docker Setup(Optional)
1. **Build the Docker image**
    ```bash

    docker build -t -p syamsundarchegu/zepto_ast:latest .
    docker run -d syamsundarchegu/zepto_ast:latest
    docker ps -a
    docker logs <container_object>
    
    ```

2. **Run the Docker container**
    ```bash
    docker run -t -p 3000:3000 syamsundarchegu/zepto_ast:latest
    ```

## Maditory Step
Access the application at `http://127.0.0.1:3000`.


### Design Choices
- **Flask**: Chosen for its simplicity and ease of use to create a web server.
- **SQLite**: Lightweight database suitable for development and quick prototyping.
- **Docker**: Ensures the application can run consistently across different environments.
