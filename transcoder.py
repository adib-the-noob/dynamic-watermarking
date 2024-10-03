import subprocess

def transcode_to_hls(input_file, output_playlist, segment_duration=10):
    """
    Transcode a video into multiple segments for HLS using FFmpeg.
    
    Args:
        input_file (str): Path to the input video file.
        output_playlist (str): Path for the output HLS playlist (.m3u8 file).
        segment_duration (int): Duration of each segment in seconds (default: 10 seconds).
    """
    try:
        # Build the FFmpeg command
        command = [
            'ffmpeg',
            '-i', input_file,                # Input video file
            '-c:v', 'libx264',               # Transcode video to H.264
            '-c:a', 'aac',                   # Transcode audio to AAC
            '-strict', '-2',                 # Allow experimental AAC encoder
            '-crf', '20',                    # Constant rate factor for quality (lower is better)
            '-start_number', '0',            # Segment numbering starts from 0
            '-hls_time', str(segment_duration), # Duration of each segment in seconds
            '-hls_list_size', '0',           # Keep all segments in the playlist
            '-f', 'hls',                     # Output format set to HLS
            output_playlist                  # Path to the output .m3u8 playlist
        ]
        
        # Run the command
        subprocess.run(command, check=True)
        print(f"Transcoding completed. Playlist and segments saved to {output_playlist}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred during transcoding: {e}")

# Example usage
input_video = "SAMPLE-1080p.mp4"           # Path to the input video file
output_m3u8 = "output/output.m3u8"  # Path to the output HLS playlist
segment_duration = 10               # Segment duration in seconds

transcode_to_hls(input_video, output_m3u8, segment_duration)
