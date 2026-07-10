import re


class OCRCleaner:

    def clean(self, text):

        text = re.sub(
            r"([A-Za-z])\s(?=[A-Za-z]\s)",
            r"\1",
            text)

        text = re.sub(r"[_]{2,}",
            "",
            text)

        text = re.sub(r"[-]{5,}",
            "",
            text)

        text = re.sub(r"\|{2,}",
            "",
            text)

        text = re.sub(r"\*{3,}",
            "",
            text)

        return text