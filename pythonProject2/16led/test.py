import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# Tải mô hình EfficientNet-B0 đã được huấn luyện trước
model = models.efficientnet_b0(pretrained=True)

# Tiền xử lý ảnh đầu vào
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Tải và tiền xử lý ảnh
path_to_image = "/home/lqptoptvt/Desktop/0000.jpg"
image = Image.open(path_to_image)
input_tensor = transform(image)
input_batch = input_tensor.unsqueeze(0)

# Tiến hành dự đoán
model.eval()
with torch.no_grad():
    output = model(input_batch)

# Lấy chỉ số lớp được dự đoán
_, predicted_idx = torch.max(output, 1)
print("Chỉ số lớp dự đoán:", predicted_idx.item())