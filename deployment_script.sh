#!/bin/bash

# Navigate to your project directory
cd /home/anagh129/linkShare/

# Pull the latest changes from the main branch on GitHub
git pull origin master

# Activate your virtual environment
source /home/anagh129/env/bin/activate

# Install/update dependencies
pip install -r requirements.txt

echo "Deployment finished!"
