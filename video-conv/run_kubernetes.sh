#!/usr/bin/env bash

# This tags and uploads an image to Docker Hub

# Step 1:
# This is your Docker ID/path
dockerpath=noital/video-conv

# Step 2
# Run the Docker Hub container with kubernetes
kubectl create deployment video-conv --image noital/video-conv --e
kubectl apply -f video-conv-pod.yml
# Step 3:
while [[ $(kubectl get pods -l app=flask-app -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do sleep 1; done
# List kubernetes pods
kubectl get pods
# Step 4:
# Forward the container port to a host
kubectl port-forward deployment/video-conv 8000:80
