import os

def save_uploaded_image(uploaded_file, save_dir="uploads") -> str:
    os.makedirs(save_dir, exist_ok=True)
    image_path = os.path.join(save_dir, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return image_path
