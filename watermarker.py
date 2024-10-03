import os
import random
import subprocess

from row_counter import stampingInfoRow

def generate_dynamic_positions():
    """
    Generates a random (x, y) position for watermark placement.
    
    Returns:
        tuple: A random (x, y) position.
    """
    # Example screen size (you can adjust based on your actual video resolution)
    max_x = 1920  # Max width of the video
    max_y = 1080  # Max height of the video
    
    # Generate random positions within the screen size
    x = random.randint(0, max_x - 100)  # 100 is the width of watermark (adjust as needed)
    y = random.randint(0, max_y - 50)   # 50 is the height of watermark (adjust as needed)
    
    return (x, y)


def apply_watermark_to_segment(input_segment, output_segment, watermark_image, position):
    """
    Applies a watermark to a video segment using FFmpeg.
    
    Args:
        input_segment (str): Path to the input video segment file.
        output_segment (str): Path to the output watermarked video segment file.
        watermark_image (str): Path to the watermark image.
        position (tuple): (x, y) coordinates for the watermark position.
    """
    try:
        x, y = position
        # FFmpeg command to overlay the watermark at the given position
        command = [
            'ffmpeg',
            '-i', input_segment,                # Input video segment
            '-i', watermark_image,              # Watermark image
            '-filter_complex', f'overlay={x}:{y}',  # Apply watermark at x:y position
            '-c:a', 'copy',                     # Copy the audio as-is (no re-encoding)
            output_segment                      # Output file with watermarked segment
        ]
        subprocess.run(command, check=True)
        print(f"Watermark applied to {input_segment}, saved as {output_segment}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while applying watermark: {e}")

def watermark_segments_with_dynamic_position(output_dir, watermark_image, row_size=5):
    """
    Processes each segment and applies a watermark with dynamically changing positions.
    
    Args:
        output_dir (str): Directory containing the original video segments.
        watermark_image (str): Path to the watermark image.
        row_size (int): Number of segments per row.
    """
    # Get the list of segment rows
    segment_rows = stampingInfoRow(output_dir, row_size)

    # Loop through each row and segment
    for row_index, row in enumerate(segment_rows):
        for segment_index, segment in enumerate(row):
            input_segment = os.path.join(output_dir, segment)
            output_segment = os.path.join(output_dir, f"watermarked_{segment}")

            # Generate a dynamic position for watermark
            position = generate_dynamic_positions()

            # Apply the watermark to the segment
            apply_watermark_to_segment(input_segment, output_segment, watermark_image, position)

# Example usage:
output_dir = "output"              # Directory where the segments are stored
watermark_image = "text.png"   # Path to the watermark image
row_size = 5                        # Number of segments per row

# Process and watermark the segments
watermark_segments_with_dynamic_position(output_dir, watermark_image, row_size)