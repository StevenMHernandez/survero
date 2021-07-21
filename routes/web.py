"""Web Routes."""

from masonite.routes import Get, Post, Delete, Put

ROUTES = [
    Get("/", "HomeController@index"),

    Get("/papers/", "PapersController@index"),
    Get("/papers/@key", "PapersController@show"),

    Get("/authors/", "AuthorsController@index"),
    Get("/authors/graph", "AuthorsController@graph"),
    Get("/authors/@creator_id", "AuthorsController@show"),

    Get("/tags/", "TagsController@index"),
    Get("/tags/@tag", "TagsController@show"),

    Get("/api/papers/", "PapersController@api_index"),
    Get("/api/papers/@key", "PapersController@api_show"),

    Get("/api/authors/", "AuthorsController@api_index"),
    Get("/api/authors/graph", "AuthorsController@api_graph"),
    Get("/api/authors/@creator_id", "AuthorsController@api_show"),

    Get("/api/tags", "TagsController@api_index"),
    Get("/api/tags/@tag_id", "TagsController@api_show"),
    Post("/api/tags", "TagsController@create"),
    Put("/api/tags/update", "TagsController@update"),
    Delete("/api/tags/@id", "TagsController@delete"),

    Get("/screenshots", "ScreenshotsController@index"),
    Get("/api/screenshots", "ScreenshotsController@api_index"),
    Post("/api/screenshots", "ScreenshotsController@create"),

    Get("/notes", "NotesController@index"),
    Get("/api/notes", "NotesController@api_index"),
    Post("/api/notes", "NotesController@create"),

    Get("/search", "FullTextSearchController@index"),
    Get("/api/search", "FullTextSearchController@api_index"),
    Get("/api/search/alternatives", "FullTextSearchController@api_alternatives"),
]
