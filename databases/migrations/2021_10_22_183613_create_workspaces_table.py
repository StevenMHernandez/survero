"""CreateWorkspacesTable Migration."""

from masoniteorm.migrations import Migration


class CreateWorkspacesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("workspaces") as table:
            table.increments("id")
            table.string('collection_key')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("workspaces")
