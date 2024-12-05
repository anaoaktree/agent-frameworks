#!/bin/bash

# Check if framework argument is provided
if [ $# -eq 0 ]; then
    echo "Please provide a framework name (langgraph, llamaindex, dspy, or vanilla)"
    exit 1
fi

FRAMEWORK=$1
VENV_NAME=".venv-${FRAMEWORK}"

# Function to validate framework name
validate_framework() {
    case $FRAMEWORK in
        langgraph|llamaindex|dspy|vanilla)
            return 0
            ;;
        *)
            echo "Invalid framework. Please choose from: langgraph, llamaindex, dspy, or vanilla"
            exit 1
            ;;
    esac
}

# Function to create or just activate virtual environment
setup_venv() {
    if [ -d "$VENV_NAME" ]; then
        echo "Virtual environment $VENV_NAME already exists. Skipping creation."
    else
        echo "Creating virtual environment: $VENV_NAME"
        python3 -m venv $VENV_NAME
    fi

    # Activate virtual environment
    source $VENV_NAME/bin/activate

    # Upgrade pip
    pip install --upgrade pip
}


# Function to install requirements
install_requirements() {
    echo "Installing requirements for $FRAMEWORK"
        # Upgrade pip
    pip install -r requirements-$FRAMEWORK.txt
}

# Main execution
validate_framework
setup_venv
install_requirements

echo "Setup complete! Virtual environment '$VENV_NAME' is now active."
echo "To deactivate the virtual environment, run: deactivate"