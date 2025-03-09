class ProfileRouter:
    """
    A database router that directs Profile-related operations
    to both the centralized and subsidiary databases.
    """

    def db_for_read(self, model, **hints):
        """Specify which database to read from."""
        if model._meta.app_label == 'Authentication':
            return 'default'  # Read from centralized database
        return None

    def db_for_write(self, model, **hints):
        """Specify which database to write to."""
        if model._meta.app_label == 'Authentication':
            return 'default'  # Write to centralized database first
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations between objects in different databases."""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrations for profiles on all databases."""
        if app_label == 'Authentication':
            return db in ['default', 'ilp']
        return None