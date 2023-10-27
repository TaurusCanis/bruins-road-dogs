from datetime import datetime


def format_title(title):
    """
    Extracts the title from a string in the format "BOSTON BRUINS @ VISITING TEAM".
    If the input string is empty or does not contain a title, it returns an empty string.
    
    Args:
        title: A string in the format "BOSTON BRUINS @ VISITING TEAM".
        
    Returns:
        A string representing the extracted title, or an empty string if no title was found.
    """
    if not title:
        return ""
    try:
        return title.split("@")[1].strip()
    except IndexError:
        return ""

def format_date(date):
    """
    Formats a date string in the format "YYYY-MM-DDTHH:MM:SS" to a human-readable format.
    If the input string is empty or cannot be parsed, it returns an empty string.
    
    Args:
        date: A string representing a date in the format "YYYY-MM-DDTHH:MM:SS".
        
    Returns:
        A string representing the formatted date in the format "Weekday, Month Day, Year Hour:Minute am/pm",
        or an empty string if the input string is empty or cannot be parsed.
    """
    if not date:
        return ""
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        formatted_date_without_time = date_obj.strftime("%A, %B %d, %Y")
        formatted_time = date_obj.strftime("%I:%M %p").lstrip("0").replace("PM", "pm").replace("AM", "am")
        formatted_date = f"{formatted_date_without_time} {formatted_time}"
        return formatted_date
    except ValueError:
        return ""