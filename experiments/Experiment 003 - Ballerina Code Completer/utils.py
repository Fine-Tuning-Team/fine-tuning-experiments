import os

def get_most_recent_file_with_prefix(directory: str, prefix: str) -> str:
    """
    Get the most recent file with the given prefix in a directory.
    
    Args:
        directory (str): Path to the directory to search in
        prefix (str): Prefix to filter files by
        
    Returns:
        str: The full path to the most recent file with the prefix
             or None if no matching files found
    """
    # Check if directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} does not exist")
        
    # Get all files with the prefix
    matching_files = [
        f for f in os.listdir(directory) 
        if os.path.isfile(os.path.join(directory, f)) and f.startswith(prefix)
    ]
    
    # If no matching files found
    if not matching_files:
        return None
    
    # Sort files in descending order (newest first)
    # The timestamp format YYYY-MM-DD_HH-MM-SS sorts correctly as strings
    matching_files.sort(reverse=True)
    
    # Return the full path to the most recent file
    return os.path.join(directory, matching_files[0])
