import ffmpeg
import os
import sys

def compress_video(input_path, output_path, target_size_mb, resolution):
    # Calculate target size in bytes
    target_size = target_size_mb * 1024 * 1024
    
    # First pass to calculate bitrate
    probe = ffmpeg.probe(input_path)
    duration = float(probe['format']['duration'])
    
    # Calculate video and audio bitrates
    audio_bitrate = 128000  # 128 kbps
    video_bitrate = (target_size - audio_bitrate * duration / 8) / (duration / 8)
    
    ffmpeg.input(input_path).output(
        output_path,
        vcodec='libx264',
        vf=f'scale={resolution}',  # Scale video to the desired resolution
        video_bitrate=video_bitrate,
        max_muxing_queue_size=9999,
        strict='experimental',
        audio_bitrate=audio_bitrate,
        format='mp4'
    ).run()

    print(f"Video compressed and saved to {output_path}")

def get_video_size(file_path):
    size = os.path.getsize(file_path)
    return size / (1024 * 1024)  # Convert size to MB

def main():
    input_path = input("Enter the path to the input video file: ")
    target_size_mb = float(input("Enter the desired output file size in MB: "))
    resolution = '1920:1080' #input("Enter the desired resolution (e.g., 1920:1080 for Full HD): ")

    # Extract the extension from the input file
    input_extension = os.path.splitext(input_path)[1]
    output_path = input("Enter the name of the compressed video file: ") + input_extension

    compress_video(input_path, output_path, target_size_mb, resolution)

    final_size = get_video_size(output_path)
    print(f"Final video size: {final_size:.2f} MB")

if __name__ == "__main__":
    main()