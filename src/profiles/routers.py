from rest_framework.routers import Route, DefaultRouter, DynamicRoute


class ProfileRouter(DefaultRouter):
    """
    Router for profile viewset.
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
                'patch': 'partial_update',
            },
            name='{basename}_detail',
            detail=False,
            initkwargs={'suffix': 'Me'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}_{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]


class PostRouter(DefaultRouter):
    """
    Router for post viewset.
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
                'patch': 'partial_update',
            },
            name='{basename}_detail',
            detail=False,
            initkwargs={'suffix': 'Me'}
        ),
    ]
