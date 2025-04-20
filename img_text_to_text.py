# from PIL import Image
# import pytesseract
# import cv2
# import numpy as np

# def image_to_text(image_path):
#     """
#     Convert image to text using OCR.
    
#     Parameters:
#     image_path (str): Path to the image file
    
#     Returns:
#     str: Extracted text from the image
#     """
#     try:
#         # Read the image using OpenCV
#         image = cv2.imread(image_path)
        
#         # Convert to grayscale
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
#         # Apply thresholding to preprocess the image
#         threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
#         # Perform noise removal using median blur
#         processed_image = cv2.medianBlur(threshold, 3)
        
#         # Convert the OpenCV image to PIL format
#         pil_image = Image.fromarray(processed_image)
        
#         # Extract text from image
#         text = pytesseract.image_to_string(pil_image)
        
#         return text.strip()
    
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# # Example usage
# if __name__ == "__main__":
#     # Replace with your image path
#     image_path = "iim.png"
    
#     # Extract text
#     extracted_text = image_to_text(image_path)
    
#     # Print results
#     print("Extracted Text:")
#     print("-" * 50)
#     print(extracted_text)



from PIL import Image
import pytesseract
import cv2
import numpy as np
import google.generativeai as genai

def image_to_text(image_path):
    """
    Convert image to text using OCR.
    
    Parameters:
    image_path (str): Path to the image file
    
    Returns:
    str: Extracted text from the image
    """
    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to preprocess the image
        threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Perform noise removal using median blur
        processed_image = cv2.medianBlur(threshold, 3)
        
        # Convert the OpenCV image to PIL format
        pil_image = Image.fromarray(processed_image)
        
        # Extract text from image
        text = pytesseract.image_to_string(pil_image)
        
        return text.strip()
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

def summarize_text(text):
    """
    Summarize extracted text using Gemini API.
    
    Parameters:
    text (str): Extracted text to summarize
    
    Returns:
    str: Summarized text
    """
    try:
        genai.configure(api_key='AIzaSyBtIde2acvfjEzz2uPHnksYh4ubz0iF8dA')
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Summarize this text: {text}")
        return response.text.strip()
    except Exception as e:
        return f"An error occurred while summarizing: {str(e)}"

# if __name__ == "__main__":
#     # Replace with your image path
#     image_path = "ii.png"
    
#     # Extract text
#     extracted_text = image_to_text(image_path)
    
#     # Summarize text
#     summarized_text = summarize_text(extracted_text)
    
#     # Print results
#     print("Extracted Text:")
#     print("-" * 50)
#     print(extracted_text)
#     print("\nSummarized Text:")
#     print("-" * 50)
#     print(summarized_text)