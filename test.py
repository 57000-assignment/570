import os
from PIL import Image

# Input and output directories
input_folder = "results/selfie2anime/img"  # Replace with the folder containing the images
output_folder_first = "first_row"  # Replace with your desired output folder for first rows
output_folder_last = "last_row"  # Replace with your desired output folder for last rows

# Create output directories if they don't exist
os.makedirs(output_folder_first, exist_ok=True)
os.makedirs(output_folder_last, exist_ok=True)

# Loop through all files in the input folder
for file_name in os.listdir(input_folder):
    # Check if the file is an image
    if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
        # Load the image
        image_path = os.path.join(input_folder, file_name)
        image = Image.open(image_path)
        
        # Get the image dimensions
        row_height = 256
        image_width, image_height = image.size
        
        # Extract the first row
        first_row = image.crop((0, 0, image_width, row_height))
        # Extract the last row
        last_row = image.crop((0, image_height - row_height, image_width, image_height))
        
        # Save the extracted rows
        first_row.save(os.path.join(output_folder_first, f"first_{file_name}"))
        last_row.save(os.path.join(output_folder_last, f"last_{file_name}"))
        
        print(f"Processed {file_name}: First and last rows saved.")

print("Processing complete. Extracted rows are saved in the respective folders.")