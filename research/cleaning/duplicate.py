from rapidfuzz import fuzz


class DuplicateCleaner:

    def remove_duplicate_lines(self, text):

        lines = text.split("\n")

        cleaned = []

        previous = ""

        for line in lines:

            if fuzz.ratio(previous, line) > 97:
                continue

            cleaned.append(line)

            previous = line

        return "\n".join(cleaned)

    
    