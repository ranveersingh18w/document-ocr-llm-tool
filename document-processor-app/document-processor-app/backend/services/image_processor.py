from PIL import Image
import os

def process_images(image_files):
    processed_images = []
    
    for image_file in image_files:
        try:
            with Image.open(image_file) as img:
                # Example processing: resize image
                img = img.resize((800, 800))
                
                # Save processed image to outputs directory
                output_path = os.path.join('outputs', os.path.basename(image_file))
                img.save(output_path)
                
                processed_images.append(output_path)
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
    
    return processed_images

def convert_image_format(image_file, format='JPEG'):
    try:
        with Image.open(image_file) as img:
            output_path = os.path.splitext(image_file)[0] + f'.{format.lower()}'
            img.convert('RGB').save(output_path, format=format)
            return output_path
    except Exception as e:
        print(f"Error converting {image_file}: {e}")
        return None