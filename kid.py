import os
import torch
import numpy as np
from torchvision import models, transforms
from PIL import Image
from scipy.linalg import eigh

# Define feature extraction
def extract_features(image_dir, device='cuda'):
    """Extract features from images in the given directory using InceptionV3."""
    model = models.inception_v3(pretrained=True, transform_input=False)
    model.fc = torch.nn.Identity()  # Remove the final classification layer
    model.eval()
    model.to(device)

    preprocess = transforms.Compose([
        transforms.Resize((299, 299)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    features = []
    for img_file in sorted(os.listdir(image_dir)):
        img_path = os.path.join(image_dir, img_file)
        img = Image.open(img_path).convert("RGB")
        input_tensor = preprocess(img).unsqueeze(0).to(device)
        with torch.no_grad():
            feature = model(input_tensor).cpu().numpy()
        features.append(feature.flatten())

    return np.array(features)

# Polynomial kernel
def polynomial_kernel(x, y, degree=3, gamma=None, coef0=1):
    if gamma is None:
        gamma = 1.0 / x.shape[1]
    return (gamma * np.dot(x, y.T) + coef0) ** degree

# MMD^2 calculation
def compute_mmd2(X, Y, kernel=polynomial_kernel):
    XX = kernel(X, X)
    XY = kernel(X, Y)
    YY = kernel(Y, Y)
    return XX.mean() - 2 * XY.mean() + YY.mean()

# Calculate KID
def calculate_kid(real_dir, generated_dir, degree=3, gamma=None, coef0=1, device='cuda'):
    real_features = extract_features(real_dir, device=device)
    generated_features = extract_features(generated_dir, device=device)

    kernel = lambda x, y: polynomial_kernel(x, y, degree, gamma, coef0)
    kid_value = compute_mmd2(real_features, generated_features, kernel)
    return kid_value

# Example usage
real_images_dir = "first_row"
generated_images_dir = "last_row"
kid_score = calculate_kid(real_images_dir, generated_images_dir, device='cuda')
print(f"KID Score: {kid_score}")
