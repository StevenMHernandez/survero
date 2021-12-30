"""Web Routes."""

from masonite.routes import Route


ROUTES = [
    ## These authentication routes were taken from the following imports
    ## `from masonite.authentication import Auth`
    ## `ROUTES += Auth.routes()`

    Route.get("/login", "auth.LoginController@show").name("login"),
    Route.get("/register", "auth.RegisterController@show").name("register"),
    Route.post("/register", "auth.RegisterController@store").name(
        "register.store"
    ),
    Route.get("/password_reset", "auth.PasswordResetController@show").name(
        "password_reset"
    ),
    Route.post("/password_reset", "auth.PasswordResetController@store").name(
        "password_reset.store"
    ),
    Route.get(
        "/change_password/@token",
        "auth.PasswordResetController@change_password",
    ).name("change_password"),
    Route.post(
        "/change_password/@token",
        "auth.PasswordResetController@store_changed_password",
    ).name("change_password.store"),
    Route.post("/login", "auth.LoginController@store").name("login.store"),

    Route.group([
        
        Route.get("/", "HomeController@index"),

        Route.get("/workspaces", "WorkspacesController@index"),

        Route.get("/workspaces/@workpace_key/papers", "PapersController@index"),
        Route.get("/workspaces/@workpace_key/papers/@key", "PapersController@show"),

        Route.get("/workspaces/@workpace_key/authors", "AuthorsController@index"),
        Route.get("/workspaces/@workpace_key/authors/graph", "AuthorsController@graph"),
        Route.get("/workspaces/@workpace_key/authors/@creator_id", "AuthorsController@show"),

        Route.get("/workspaces/@workpace_key/publications", "PublicationsController@index"),

        Route.get("/workspaces/@workpace_key/tags", "TagsController@index"),
        Route.get("/workspaces/@workpace_key/tags/@tag", "TagsController@show"),

        Route.get("/workspaces/@workpace_key/screenshots", "ScreenshotsController@index"),
        Route.get("/workspaces/@workpace_key/notes", "NotesController@index"),
        Route.get("/workspaces/@workpace_key/search", "FullTextSearchController@index"),
    ], middleware=['auth']),

    Route.group([
        Route.get("/api/workspaces", "WorkspacesController@api_index"),
        Route.post("/api/workspaces", "WorkspacesController@create"),
        Route.delete("/api/workspaces/@workpace_key", "WorkspacesController@delete"),

        Route.get("/api/workspaces/@workpace_key/papers", "PapersController@api_index"),
        Route.get("/api/workspaces/@workpace_key/papers/@key", "PapersController@api_show"),

        Route.get("/api/workspaces/@workpace_key/authors", "AuthorsController@api_index"),
        Route.get("/api/workspaces/@workpace_key/authors/graph", "AuthorsController@api_graph"),
        Route.get("/api/workspaces/@workpace_key/authors/@creator_id", "AuthorsController@api_show"),

        Route.get("/api/workspaces/@workpace_key/publications", "PublicationsController@api_index"),

        Route.get("/api/workspaces/@workpace_key/tags", "TagsController@api_index"),
        Route.get("/api/workspaces/@workpace_key/tags/@tag_id", "TagsController@api_show"),
        Route.post("/api/tags", "TagsController@create"),
        Route.put("/api/tags/update", "TagsController@update"),
        Route.delete("/api/tags/@id", "TagsController@delete"),

        Route.get("/api/workspaces/@workpace_key/screenshots", "ScreenshotsController@api_index"),
        Route.post("/api/screenshots", "ScreenshotsController@create"),
        Route.delete("/api/screenshots/@id", "ScreenshotsController@delete"),

        Route.get("/api/workspaces/@workpace_key/notes", "NotesController@api_index"),
        Route.post("/api/notes", "NotesController@create"),
        Route.delete("/api/notes/@id", "NotesController@delete"),

        Route.get("/api/workspaces/@workpace_key/search", "FullTextSearchController@api_index"),
        Route.get("/api/workspaces/@workpace_key/search/alternatives", "FullTextSearchController@api_alternatives"),
    ], middleware=['auth']),
]
