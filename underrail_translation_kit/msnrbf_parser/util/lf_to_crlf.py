import re

def lf_to_crlf(string: str) -> str:
    """
    replaces all LF to CRLF, avoiding making CRLF to CRCRLF
    :param string: string to replace
    :return: replaced string
    """
    return re.sub("\r?\n", "\r\n", string)