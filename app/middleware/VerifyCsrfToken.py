"""CSRF Middleware."""

from masonite.middleware import VerifyCsrfToken as Middleware


class VerifyCsrfToken(Middleware):
    """Verify CSRF Token Middleware."""

    """Which routes should be exempt from CSRF protection."""
    exempt = [
        '/api/screenshots',
        '/api/tags',
        '/api/notes',
        '/api/notes/@id',
        '/api/tags/update',
        '/api/tags/@id',
    ]

    # """Whether or not the CSRF token should be changed on every request."""
    # every_request = False
    #
    # """The length of the token to generate."""
    # token_length = 30
