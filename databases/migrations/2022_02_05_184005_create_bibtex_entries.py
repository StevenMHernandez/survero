"""CreateBibtexEntries Migration."""

from masoniteorm.migrations import Migration


class CreateBibtexEntries(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("bibtex_entries") as table:
            table.increments("id")
            table.string('paper_key')
            table.text('bibtex')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("bibtex_entries")
