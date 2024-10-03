import os

def stampingInfoRow(
    output_dir: str,
    row_size : int = 5
) -> list:
    segmented_files = [
        f for f in os.listdir(output_dir) if f.endswith('.ts')
    ]
    segmented_files.sort()
    
    segment_rows = [segmented_files[i:i + row_size] for i in range(0, len(segmented_files), row_size)]

    print("\nSegment rows:")
    for index, row in enumerate(segment_rows):
        print(f"Row {index}: {row}")

    return segment_rows
