import logging

from omens.models import Chapter

from .importer import Importer

logger = logging.getLogger(__name__)


class CreditsImporter(Importer):
    """
    Imports index files into the database
    """

    expected_columns = [
        "Animal",
        "Chapter",
        "Author",
        "Reviewer",
        "Proofreader",
        "Remarks",
    ]

    def save(self):
        """
        Saves witnesses in Witness model
        """
        for row in self.read_rows():
            if not row.get("Chapter"):
                continue
            chapter, created = Chapter.objects.update_or_create(
                chapter_name=row.get("Chapter").rstrip(".0"),
            )
            chapter.animal = row.get("Animal")
            chapter.author = row.get("Author")
            chapter.reviewer = row.get("Reviewer")
            chapter.proofreader = row.get("Proofreader")
            chapter.remarks = row.get("Remarks")

            try:
                chapter.save()
            except Exception as e:
                logger.error("Error saving credits for %s", self.fname)
                return {self.fname: repr(e)}

        return
