from rest_framework.routers import Route, SimpleRouter


class ProfileRouter(SimpleRouter):
    """
    Router for account viewset.
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'post': 'create',
                'get': 'list',
            },
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'delete': 'destroy',
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
            },
            name='{basename}_detail',
            detail=False,
            initkwargs={'suffix': 'Me'}
        ),
    ]
