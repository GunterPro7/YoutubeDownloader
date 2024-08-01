def append_or_create_file(file_name: str, *content: str):
    """
    Appends content to the file if it exists, otherwise creates a new file with the provided content.

    :param file_name: The name of the file to append or create.
    :param content: Content strings to be written to the file.
    """
    # Open the file in append mode
    with open(file_name, 'a') as file:
        for line in content:
            file.write(line + '\n')
