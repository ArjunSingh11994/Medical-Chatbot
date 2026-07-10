from pathlib import Path


def normalize_metadata(doc):

    metadata = {

        "source": Path(
            doc.metadata.get("source", "")
        ).name,

        "page": int(
            doc.metadata.get("page", 0)
        ),

        "title": doc.metadata.get(
            "title",
            ""
        ).strip(),

        "author": doc.metadata.get(
            "author",
            ""
        ).strip()

    }

    return metadata