"""CreateScreenshotsTable Migration."""

from masoniteorm.migrations import Migration


class CreateScreenshotsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("screenshots") as table:
            table.increments("id")
            table.string('paper_key')
            table.string('file_name')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("screenshots")
