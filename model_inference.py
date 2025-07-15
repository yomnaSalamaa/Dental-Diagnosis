from ultralytics import YOLO
import os
import uuid
import cv2

# Load models once
teeth_model = YOLO("models/best_teeth_detection.pt")
disease_model = YOLO("models/best_diseases.pt")

def save_uploaded_image(uploaded_file, save_dir="uploads/input/"):
    os.makedirs(save_dir, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(save_dir, f"{file_id}.jpg")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def run_model(model, image_path, model_name, return_count=False, return_labels=False):
    results = model(image_path)
    output_dir = "uploads/output"
    os.makedirs(output_dir, exist_ok=True)
    result_image = results[0].plot()
    result_filename = f"{model_name}_{uuid.uuid4().hex}.jpg"
    result_path = os.path.join(output_dir, result_filename)
    cv2.imwrite(result_path, result_image)

    boxes = results[0].boxes
    class_ids = boxes.cls.tolist() if boxes is not None else []

    if return_count:
        num_detections = len(class_ids)
        return result_path, num_detections

    if return_labels:
        names = model.names
        class_names = [names[int(cls_id)] for cls_id in class_ids]
        return result_path, class_names

    return result_path


def run_teeth_model(image_path):
    output_path, detected_teeth = run_model(teeth_model, image_path, "teeth", return_count=True)
    expected_teeth = 32  # Typical adult dentition
    missing_teeth = max(0, expected_teeth - detected_teeth)
    return output_path, missing_teeth


def run_disease_model(image_path):
    return run_model(disease_model, image_path, "disease", return_labels=True)


def run_both_models(image_path):
    teeth_result = run_teeth_model(image_path)
    disease_result = run_disease_model(image_path)
    return teeth_result, disease_result