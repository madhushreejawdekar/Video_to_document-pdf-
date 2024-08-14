import os
import openai
import time
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image
import textwrap

# Set your OpenAI API key
openai.api_key = 'your_api_key'

def enhance_text(original_text):
    retry_count = 0
    max_retries = 5
    while retry_count < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" if you prefer
                messages=[
                    {"role": "system", "content": "You are an assistant that improves text descriptions for a visual guide. Enhance the given text to make it more descriptive and aligned with a step-by-step explanation of an image, without seeing the image itself."},
                    {"role": "user", "content": f"Enhance this text to be more descriptive and suitable for a step-by-step visual guide: {original_text}"}
                ],
                max_tokens=150
            )
            enhanced_text = response.choices[0].message['content'].strip()

            # Ensure the text ends with a full stop
            if not enhanced_text.endswith(('.', '!', '?')):
                enhanced_text += '.'

            return enhanced_text
        except openai.error.RateLimitError:
            print("Rate limit reached, waiting before retrying...")
            retry_count += 1
            time.sleep(60)  # Wait for 60 seconds before retrying
        except Exception as e:
            print(f"Error in enhancing text: {str(e)}")
            return original_text  # Return original text if enhancement fails

    # If maximum retries are reached and still failed, return original text
    print("Max retries reached, returning original text.")
    return original_text

def read_and_merge_text(text_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        full_text = file.read()

    # Merge text into paragraphs (split by double newlines)
    paragraphs = full_text.split('\n\n')
    return paragraphs

def align_text_with_frames(paragraphs, num_frames):
    if len(paragraphs) < num_frames:
        # If we have fewer paragraphs than frames, repeat the last paragraph
        paragraphs.extend([paragraphs[-1]] * (num_frames - len(paragraphs)))

    aligned_text = [paragraphs[i] for i in range(num_frames)]
    return aligned_text

def create_guide_from_selected_frames(frames_folder, text_file, output_pdf):
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith(('.jpg', '.png'))])
    num_frames = len(frame_files)

    paragraphs = read_and_merge_text(text_file)
    aligned_text = align_text_with_frames(paragraphs, num_frames)

    c = canvas.Canvas(output_pdf, pagesize=landscape(letter))
    width, height = landscape(letter)
    styles = getSampleStyleSheet()

    left_margin = inch
    right_margin = inch
    top_margin = inch
    bottom_margin = 2 * inch

    img_width = width - left_margin - right_margin
    img_height = height - top_margin - bottom_margin - inch  # Adjusted for text space

    for i, (frame_file, text) in enumerate(zip(frame_files, aligned_text)):
        frame_path = os.path.join(frames_folder, frame_file)

        print(f"Processing frame {i+1} of {num_frames}")
        enhanced_text = enhance_text(text)

        # Create text frame and wrap text
        text_frame_width = width - 2 * left_margin
        text_frame = Frame(left_margin, height - top_margin - 2 * inch, text_frame_width, 2 * inch, showBoundary=0)
        wrapped_text = textwrap.fill(enhanced_text, width=80)  # Adjust text width as needed
        story = [Paragraph(wrapped_text, styles['Normal'])]
        text_frame.addFromList(story, c)

        # Adjust image position based on text size
        text_height = text_frame.height
        img_y_position = height - top_margin - text_height - img_height

        img = Image.open(frame_path)
        aspect = img.width / img.height
        if img_width / aspect > img_height:
            img_height = img_width / aspect
        else:
            img_width = img_height * aspect
        c.drawImage(frame_path, left_margin, img_y_position, width=img_width, height=img_height)

        # Add page number
        c.setFont("Helvetica", 10)
        c.drawString(width - right_margin - 50, bottom_margin - 10, f"Page {i+1}")

        c.showPage()

    c.save()
    print(f"Enhanced guide generated and saved as {output_pdf}")

# Example usage
frames_folder = "path/to/cropped/extracted_frames_folder"
text_file = "path/to/transcript/file.txt"
output_pdf = "path/to/store/output_obtained_after_aligning"

create_guide_from_selected_frames(frames_folder, text_file, output_pdf)
