from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class NotificationAccountRouter(DefaultRouter):
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
        DynamicRoute(
            url=r'^{prefix}/{url_path}/{lookup}{trailing_slash}$',
            name='{basename}_{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
