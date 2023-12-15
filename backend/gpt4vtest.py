import os
import openai


def analyze_image(image_path, openai_api_key):
    """
    Analyze an image using OpenAI's vision capabilities.
    :param image_path: Path to the image file.
    :param openai_api_key: Your OpenAI API key.
    :return: The response from the OpenAI API.
    """
    openai.api_key = openai_api_key

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    try:
        response = openai.Image.create(
            image_data=image_data,
            # Add additional parameters as required
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Replace with your OpenAI API key
    api_key = "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"
    # Replace with the path to your image
    image_path = "/backendbackend/assets/LOSTSF6.png"
    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
    else:
        response = analyze_image(image_path, api_key)
        print(response)
