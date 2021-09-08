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
        Get("/papers/", "PapersController@index"),
        Get("/papers/@key", "PapersController@show"),

        Get("/authors/", "AuthorsController@index"),
        Get("/authors/graph", "AuthorsController@graph"),
        Get("/authors/@creator_id", "AuthorsController@show"),

        Get("/publications/", "PublicationsController@index"),

        Get("/tags/", "TagsController@index"),
        Get("/tags/@tag", "TagsController@show"),

        Get("/screenshots", "ScreenshotsController@index"),
        Get("/notes", "NotesController@index"),
        Get("/search", "FullTextSearchController@index"),
    ], middleware=['auth']),

    RouteGroup([
        Get("/api/papers/", "PapersController@api_index"),
        Get("/api/papers/@key", "PapersController@api_show"),

        Get("/api/authors/", "AuthorsController@api_index"),
        Get("/api/authors/graph", "AuthorsController@api_graph"),
        Get("/api/authors/@creator_id", "AuthorsController@api_show"),

        Get("/api/publications/", "PublicationsController@api_index"),

        Get("/api/tags", "TagsController@api_index"),
        Get("/api/tags/@tag_id", "TagsController@api_show"),
        Post("/api/tags", "TagsController@create"),
        Put("/api/tags/update", "TagsController@update"),
        Delete("/api/tags/@id", "TagsController@delete"),

        Get("/api/screenshots", "ScreenshotsController@api_index"),
        Post("/api/screenshots", "ScreenshotsController@create"),

        Get("/api/notes", "NotesController@api_index"),
        Post("/api/notes", "NotesController@create"),

        Get("/api/search", "FullTextSearchController@api_index"),
        Get("/api/search/alternatives", "FullTextSearchController@api_alternatives"),
    ], middleware=['auth']),
]




