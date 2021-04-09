# Check if stirng is empty
def empty_check(input_string):
    return "".__eq__(input_string)

# Strips whitespace and dots


def string_stripper(input_string):
    return input_string.upper().replace(
        " ", "").replace(".", "")
