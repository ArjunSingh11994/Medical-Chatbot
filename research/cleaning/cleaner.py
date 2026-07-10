import re
import unicodedata
from ftfy import fix_text


class DocumentCleaner:

    def __init__(self):
        pass

    ####################################################
    # Unicode Normalization
    ####################################################

    def normalize_unicode(self, text: str):

        text = fix_text(text)

        text = unicodedata.normalize(
            "NFKC",
            text
        )

        return text

    ####################################################
    # Whitespace
    ####################################################

    def normalize_whitespace(self, text):

        text = re.sub(r"\r", "\n", text)

        text = re.sub(r"\n{3,}", "\n\n", text)

        text = re.sub(r"[ \t]+", " ", text)

        text = text.strip()

        return text