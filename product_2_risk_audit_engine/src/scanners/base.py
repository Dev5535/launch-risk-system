class BaseScanner:
    def __init__(self, registry):
        self.registry = registry

    def scan(self, target_obj):
        """
        target_obj: AuditTarget instance
        """
        raise NotImplementedError
