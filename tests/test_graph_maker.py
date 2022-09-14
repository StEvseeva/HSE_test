from main.graph_maker import split_text

def test_split_text():
    string1 = 'short string'
    string2 = 'very very long string'
    string0 = ''

    assert split_text(string1) == 'short string'
    assert split_text(string2) == 'very very \nlong string'
    assert split_text(string0) == ''