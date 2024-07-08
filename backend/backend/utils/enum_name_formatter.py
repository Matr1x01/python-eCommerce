def enum_name_formatter(method):
    words = method.lower().split('_')  # Split the string by underscore and convert to lowercase
    formatted_words = [word.capitalize() for word in words]  # Capitalize the first letter of each word
    return ' '.join(formatted_words)