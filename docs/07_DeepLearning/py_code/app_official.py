# app_official.py
from ultralytics import solutions

inf = solutions.Inference(model="yolo26n.pt")
inf.inference()
