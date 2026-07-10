import re


class HeaderFooterCleaner:

    def remove_headers(self, text):

        patterns = [

            r"Page\s+\d+",

            r"Confidential",

            r"Hospital Guidelines",

            r"Copyright.*",

            r"www\..*",

        ]

        for pattern in patterns:
            text = re.sub(
                pattern,
                "",
                text,
                flags=re.IGNORECASE
            )

        return text

    def remove_footers(self, text):

        footer_patterns = [

            r"All Rights Reserved",

            r"Generated on.*",

            r"\d+\s*$",

        ]

        for pattern in footer_patterns:
            text = re.sub(
                pattern,
                "",
                text,
                flags=re.IGNORECASE
            )

        return text