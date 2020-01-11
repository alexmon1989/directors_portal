from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.exceptions import SuspiciousFileOperation


class ForgivingManifestStaticFilesStorage(ManifestStaticFilesStorage):

    def hashed_name(self, name, content=None, filename=None):
        try:
            result = super().hashed_name(name, content, filename)
        except (ValueError, SuspiciousFileOperation):
            # When the file is missing, let's forgive and ignore that.
            result = name
        return result
