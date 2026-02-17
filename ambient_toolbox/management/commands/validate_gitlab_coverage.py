from django.core.management.base import BaseCommand

from ambient_toolbox.gitlab.coverage import CoverageService


class Command(BaseCommand):
    """
    Compares the test-coverage percentage of the current branch against the default branch
    using the GitLab API and fails when coverage has dropped.
    """

    help = "Validates that test coverage has not dropped relative to the default branch (GitLab only)."

    def handle(self, *args, **options):
        service = CoverageService()
        return service.process()
