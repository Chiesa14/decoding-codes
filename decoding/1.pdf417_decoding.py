import cv2
import numpy as np
import subprocess
import os

# Configuration
javase_jar = "javase-3.5.0.jar"
core_jar = "core-3.5.0.jar"
jcommander_jar = "jcommander-1.82.jar"
barcode_image = "decoding/image-id.png"

# Validate required files with absolute paths
required_files = {
    "javase": os.path.abspath(javase_jar),
    "core": os.path.abspath(core_jar),
    "jcommander": os.path.abspath(jcommander_jar),
    "image": os.path.abspath(barcode_image)
}

for name, path in required_files.items():
    if not os.path.exists(path):
        print(f"Error: {name} file not found at {path}")
        exit(1)

# Build Java command with Linux-specific syntax
java_command = [
    "java",
    "-cp",
    f"{required_files['javase']}:{required_files['core']}:{required_files['jcommander']}",  # Use colon separator
    "com.google.zxing.client.j2se.CommandLineRunner",
    required_files['image']  # Use direct file path instead of file://
]

print("Running command:", " ".join(java_command))

try:
    result = subprocess.run(
        java_command,
        capture_output=True,
        text=True,
        check=True
    )
    output = result.stdout.strip()
    print("Decoded Output:")
    print(output)
except subprocess.CalledProcessError as e:
    print("Error during decoding:")
    print("STDERR:", e.stderr)
    print("STDOUT:", e.stdout)
    exit(1)

# Parse points with error checking
points = []
for line in output.splitlines():
    if line.strip().startswith("Point"):
        try:
            coords = line.split(":")[1].strip().strip("()").split(",")
            x = int(float(coords[0].strip()))
            y = int(float(coords[1].strip()))
            points.append((x, y))
        except (IndexError, ValueError) as e:
            print(f"Warning: Skipping invalid coordinate line: {line}")
            continue

if len(points) >= 4:
    try:
        image = cv2.imread(required_files['image'])
        if image is None:
            raise FileNotFoundError("Failed to load image after decoding")
            
        points_array = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(image, [points_array], isClosed=True, color=(0, 255, 0), thickness=2)
        
        annotated_image_path = "annotated_barcode.png"
        cv2.imwrite(annotated_image_path, image)
        print(f"Annotated image saved as {annotated_image_path}")
        
        cv2.imshow("Detected Barcode", image)
        print("Press any key to close the window.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"Image processing error: {str(e)}")
        exit(1)
else:
    print("No valid bounding box points detected.")
    print("Raw ZXing output:")
    print(output)