#!/usr/bin/env bash

## Complete the following steps to get Docker running locally

# Step 1:
# Build image and add a descriptive tag
docker build --tag video-conv .
# Step 2: 
# List docker images
docker images list
# Step 3: 
# Run flask app
docker run --publish 8000:80  -v ~/.aws:/home/ec2-user/.aws --env BUCKET=biesy2 flask-app --env-file ~/.aws/credentials