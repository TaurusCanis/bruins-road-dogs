from filters import format_title, format_date

def test_format_title():
    assert format_title("Boston Bruins @ New York Rangers") == "New York Rangers"
    assert format_title("New York Rangers") == ""
    assert format_title("") == ""
    assert format_title(None) == ""

def test_format_date():
    assert format_date("2023-10-04T19:00:00") == ("Wednesday, October 04, 2023 7:00 pm")
    assert format_date("2023/10/04 19:00:00") == ""
    assert format_date("") == ""
    assert format_date(None) == ""