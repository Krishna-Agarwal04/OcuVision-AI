import torch
from torchvision import transforms, models
import torch.nn as nn
from PIL import Image
import io

class OcuVisionModel:
    def __init__(self, model_path="../model.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes = ['Mild', 'Moderate', 'No DR', 'Proliferative DR', 'Severe']
        # Based on train_model.py, dataset.classes would be ordered alphabetically by folder name,
        # but the train_model.py doesn't print the exact order.
        # Wait, the train_model.py uses ImageFolder, so it's alphabetical.
        # Let's verify dataset folder names: Gaussian filtered images usually have classes:
        # 'Mild', 'Moderate', 'No_DR', 'Proliferate_DR', 'Severe'. We will assume standard alphabetical order:
        # 0: Mild, 1: Moderate, 2: No_DR, 3: Proliferate_DR, 4: Severe.
        # Let's map them to UI friendly names.
        
        self.model = models.resnet50(weights=None)
        self.model.fc = nn.Linear(self.model.fc.in_features, 5)
        
        try:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model = self.model.to(self.device)
            self.model.eval()
            self.is_loaded = True
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_loaded = False
            
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, image_bytes):
        if not self.is_loaded:
            # Fallback for dev without model
            return "No DR", 99.9

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            confidence, predicted_idx = torch.max(probabilities, 0)
            
            # Map index to class
            predicted_class = self.classes[predicted_idx.item()]
            
            # Map back to UI names
            if predicted_class == 'No_DR' or predicted_class == 'No DR':
                label = 'No DR'
            elif predicted_class == 'Proliferate_DR' or predicted_class == 'Proliferative DR':
                label = 'Proliferative DR'
            else:
                label = predicted_class
                
            return label, confidence.item() * 100

model_instance = OcuVisionModel()
