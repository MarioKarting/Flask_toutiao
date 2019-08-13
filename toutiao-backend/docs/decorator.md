# 关于装饰器

## 1. decorators

放在`decorators`列表中的装饰器，是由Flask原生类视图支持的，

装饰作用是发生在`as_view`方法中，装饰在view函数上

```python
    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        """Converts the class into an actual view function that can be used
        with the routing system.  Internally this generates a function on the
        fly which will instantiate the :class:`View` on each request and call
        the :meth:`dispatch_request` method on it.

        The arguments passed to :meth:`as_view` are forwarded to the
        constructor of the class.
        """
        def view(*args, **kwargs):
            self = view.view_class(*class_args, **class_kwargs)
            return self.dispatch_request(*args, **kwargs)

        if cls.decorators:
            view.__name__ = name
            view.__module__ = cls.__module__
            for decorator in cls.decorators:
                view = decorator(view)
```

## 2. method_decorators

放在`method_decorators`中的装饰器，是由Flask-restful扩展支持的，

装饰作用是发生在`view->dispatch_request`中的，装饰在http请求方法上

```python
class Resource(MethodView):
    """
    Represents an abstract RESTful resource. Concrete resources should
    extend from this class and expose methods for each supported HTTP
    method. If a resource is invoked with an unsupported HTTP method,
    the API will return a response with status 405 Method Not Allowed.
    Otherwise the appropriate method is called and passed all arguments
    from the url rule used when adding the resource to an Api instance. See
    :meth:`~flask_restful.Api.add_resource` for details.
    """
    representations = None
    method_decorators = []

    def dispatch_request(self, *args, **kwargs):

        # Taken from flask
        #noinspection PyUnresolvedReferences
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        if isinstance(self.method_decorators, Mapping):
            decorators = self.method_decorators.get(request.method.lower(), [])
        else:
            decorators = self.method_decorators

        for decorator in decorators:
            meth = decorator(meth)

        resp = meth(*args, **kwargs)
```

