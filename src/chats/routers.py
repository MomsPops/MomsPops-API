from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class GroupRouter(DefaultRouter):
    """Router class for notification account viewset."""
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'patch': 'partial_update',
                "delete": "destroy"
            },
            name='{basename}_detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}/{lookup}{trailing_slash}$',
            name='{basename}_{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
