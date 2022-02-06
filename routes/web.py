"""Web Routes."""

from masonite.routes import Get, Post, Delete, Put, RouteGroup

ROUTES = [
    ## These authentication routes were taken from the following imports
    ## `from masonite.auth import Auth`
    ## `ROUTES += Auth.routes()`
    Get("/login", "auth.LoginController@show").name("login"),
    Get("/logout", "auth.LoginController@logout").name("logout"),
    Post("/login", "auth.LoginController@store"),
    ## The following routes are commented out because I do not want to have them enabled in production. Maybe in the future.
    # Get("/register", "auth.RegisterController@show").name("register"),
    # Post("/register", "auth.RegisterController@store"),
    # Get("/email/verify", "auth.ConfirmController@verify_show").name("verify"),
    # Get("/email/verify/send", "auth.ConfirmController@send_verify_email"),
    # Get("/email/verify/@id:signed", "auth.ConfirmController@confirm_email"),
    # Get("/password", "auth.PasswordController@forget").name("forgot.password"),
    # Post("/password", "auth.PasswordController@send"),
    # Get("/password/@token/reset", "auth.PasswordController@reset").name("password.reset"),
# Post("/password/@token/reset", "auth.PasswordController@update"),

    RouteGroup([
        Get("/", "HomeController@index"),

        Get("/workspaces", "WorkspacesController@index"),

        Get("/workspaces/@workpace_key/papers/", "PapersController@index"),
        Get("/workspaces/@workpace_key/papers/@key", "PapersController@show"),

        Get("/workspaces/@workpace_key/authors/", "AuthorsController@index"),
        Get("/workspaces/@workpace_key/authors/graph", "AuthorsController@graph"),
        Get("/workspaces/@workpace_key/authors/@creator_id", "AuthorsController@show"),

        Get("/workspaces/@workpace_key/publications/", "PublicationsController@index"),

        Get("/workspaces/@workpace_key/tags/", "TagsController@index"),
        Get("/workspaces/@workpace_key/tags/@tag", "TagsController@show"),

        Get("/workspaces/@workpace_key/screenshots", "ScreenshotsController@index"),
        Get("/workspaces/@workpace_key/notes", "NotesController@index"),
        Get("/workspaces/@workpace_key/search", "FullTextSearchController@index"),
    ], middleware=['auth']),

    RouteGroup([
        Get("/api/info", "ApiController@api_info"),

        Get("/api/workspaces", "WorkspacesController@api_index"),
        Post("/api/workspaces", "WorkspacesController@create"),
        Delete("/api/workspaces/@workpace_key", "WorkspacesController@delete"),

        Get("/api/workspaces/@workpace_key/papers/", "PapersController@api_index"),
        Get("/api/workspaces/@workpace_key/papers/@key", "PapersController@api_show"),

        Get("/api/workspaces/@workpace_key/authors/", "AuthorsController@api_index"),
        Get("/api/workspaces/@workpace_key/authors/graph", "AuthorsController@api_graph"),
        Get("/api/workspaces/@workpace_key/authors/@creator_id", "AuthorsController@api_show"),

        Get("/api/workspaces/@workpace_key/publications/", "PublicationsController@api_index"),

        Get("/api/workspaces/@workpace_key/tags", "TagsController@api_index"),
        Get("/api/workspaces/@workpace_key/tags/@tag_id", "TagsController@api_show"),
        Post("/api/tags", "TagsController@create"),
        Put("/api/tags/update", "TagsController@update"),
        Delete("/api/tags/@id", "TagsController@delete"),

        Get("/api/workspaces/@workpace_key/screenshots", "ScreenshotsController@api_index"),
        Post("/api/screenshots", "ScreenshotsController@create"),
        Delete("/api/screenshots/@id", "ScreenshotsController@delete"),

        Get("/api/workspaces/@workpace_key/notes", "NotesController@api_index"),
        Post("/api/notes", "NotesController@create"),
        Delete("/api/notes/@id", "NotesController@delete"),

        Get("/api/workspaces/@workpace_key/search", "FullTextSearchController@api_index"),
        Get("/api/workspaces/@workpace_key/search/alternatives", "FullTextSearchController@api_alternatives"),

        Get("/api/workspaces/@workpace_key/papers/@paper_key/bibtex", "BibtexController@api_get"),
        Put("/api/workspaces/@workpace_key/papers/@paper_key/bibtex", "BibtexController@api_set"),
        Get("/api/workspaces/@workpace_key/papers/@paper_key/bibtex/generate", "BibtexController@api_generate"),
    ], middleware=['auth']),
]
