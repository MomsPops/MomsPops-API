from rest_framework.routers import Route, SimpleRouter, DynamicRoute


class AccountRouter(SimpleRouter):
    """
    Router for account viewset.
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'post': 'create',
            },
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/me{trailing_slash}$',
            mapping={
                'delete': 'destroy',
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
            },
            name='{basename}_me',
            detail=False,
            initkwargs={'suffix': 'Me'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}_{url_name}',
            detail=False,
            initkwargs={}
        ),
    ]


class BlackListRouter(SimpleRouter):
    """
    Router for blocking user viewset.
    """
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'post': 'create',
                'delete': 'destroy',
                'get': 'list',
            },
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
    ]
