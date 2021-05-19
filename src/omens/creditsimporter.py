from omens.models import Chapter

from .importer import Importer


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
                animal=row.get("Animal"),
                author=row.get("Author"),
                reviewer=row.get("Reviewer"),
                proofreader=row.get("Proofreader"),
                remarks=row.get("Remarks"),
            )
            try:
                chapter.save()
            except Exception as e:
                return {self.fname: repr(e)}

        return
