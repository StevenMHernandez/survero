"""CreateNotesTable Migration."""

from masoniteorm.migrations import Migration


class CreateNotesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("notes") as table:
            table.increments("id")
            table.string('paper_key')
            table.string('note')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("notes")
