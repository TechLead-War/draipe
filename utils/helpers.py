# Check if phone number if correct.
# check for valid email
import os


async def delete_local_temporary_files(file_path: str) -> None:
    """
    This function is responsible for deleting temporary files
    from local storage
    Args:
        file_path : local file path
    """
    if os.path.exists(file_path):
        os.remove(file_path)
