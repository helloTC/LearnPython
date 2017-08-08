import re

def re_matchelm(strlist, keyword):
    """
    Identified specific string by keyword in strlist
    Keyword could satisfied regular expression

    Parameters:
    -----------
    strlist: a list with each element as a string
    keyword: pattern of regular expression

    Return:
    -------
    match_elm: matched element

    Example:
    --------
    >>> match_elm = re_matchelm(['S0001', 'S0001_1', 'S0005'], 'S0001_\w')
    >>> ['S0001_1']
    """
    p = re.compile(keyword)
    matchlist = [p.findall(sl) for sl in strlist]
    matchidx = [i for i,j in enumerate(matchlist) if j]
    return [strlist[i] for i in matchidx]

    
