import unidecode

def get_simple_string(s):
    """
    Remove uppercase and accent in a string.

    Parameters:
        s (str): The string to simplify.

    Returns:
        str: The simplified string.
    """
    return unidecode.unidecode(s.lower())