import cv2
import matplotlib.pyplot as plt

# Load image
image = cv2.imread("/home/ashrafbarakat/Downloads/134.jpeg")

# Crop the image
croppedImage = image[0:150, 0:200]

# Convert BGR to RGB for Matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cropped_rgb = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)

# Display side by side
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image_rgb)
axes[0].set_title("Original Image")
axes[0].axis("off")

axes[1].imshow(cropped_rgb)
axes[1].set_title("Cropped Image")
axes[1].axis("off")

plt.tight_layout()
plt.show()