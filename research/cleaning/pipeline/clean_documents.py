from src.cleaning.cleaner import DocumentCleaner
from src.cleaning.header_footer import HeaderFooterCleaner
from src.cleaning.duplicate import DuplicateCleaner
from src.cleaning.ocr_cleanup import OCRCleaner


class CleaningPipeline:

    def __init__(self):

        self.cleaner = DocumentCleaner()

        self.header = HeaderFooterCleaner()

        self.duplicate = DuplicateCleaner()

        self.ocr = OCRCleaner()

    def clean(self, document):

        text = document.page_content

        text = self.cleaner.normalize_unicode(text)

        text = self.cleaner.normalize_whitespace(text)

        text = self.header.remove_headers(text)

        text = self.header.remove_footers(text)

        text = self.duplicate.remove_duplicate_lines(text)

        text = self.ocr.clean(text)

        if len(text.strip()) < 30:
            return None

        document.page_content = text

        return document