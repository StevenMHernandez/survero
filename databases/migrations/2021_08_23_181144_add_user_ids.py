"""AddUserIds Migration."""

from masoniteorm.migrations import Migration


class AddUserIds(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("screenshots") as table:
            table.unsigned_integer("user_id").default(1)

        with self.schema.table("tags") as table:
            table.unsigned_integer("user_id").default(1)
        #
        with self.schema.table("notes") as table:
            table.unsigned_integer("user_id").default(1)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table("screenshots") as table:
            table.drop_column('user_id')

        with self.schema.table("tags") as table:
            table.drop_column('user_id')

        with self.schema.table("notes") as table:
            table.drop_column('user_id')
