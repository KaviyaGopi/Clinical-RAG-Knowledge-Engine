from api.exceptions import ApplicationError

def read_file(file):
    """Read and decode the uploaded file."""
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        raise ApplicationError(f"Failed to read file: {e}", status_code=400)