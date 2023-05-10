# API

## Packing

```{eval-rst}
.. autofunction:: umsgpack.packb

Also available under the ``umsgpack.dumps()`` alias.
```

```{eval-rst}
.. autofunction:: umsgpack.pack

Also available under the ``umsgpack.dump()`` alias.
```

## Unpacking

```{eval-rst}
.. autofunction:: umsgpack.unpackb

Also available under the ``umsgpack.loads()`` alias.
```

```{eval-rst}
.. autofunction:: umsgpack.unpack

Also available under the ``umsgpack.load()`` alias.
```

## Packing Exceptions

```{eval-rst}
.. autoexception:: umsgpack.PackException
```

```{eval-rst}
.. autoexception:: umsgpack.UnsupportedTypeException
```

## Unpacking Exceptions

```{eval-rst}
.. autoexception:: umsgpack.UnpackException
```

```{eval-rst}
.. autoexception:: umsgpack.InsufficientDataException
```

```{eval-rst}
.. autoexception:: umsgpack.InvalidStringException
```

```{eval-rst}
.. autoexception:: umsgpack.UnsupportedTimestampException
```

```{eval-rst}
.. autoexception:: umsgpack.ReservedCodeException
```

```{eval-rst}
.. autoexception:: umsgpack.UnhashableKeyException
```

```{eval-rst}
.. autoexception:: umsgpack.DuplicateKeyException
```

## Ext Class

```{eval-rst}
.. autoclass:: umsgpack.Ext
   :member-order: bysource
   :special-members: __init__, __eq__, __ne__, __str__, __hash__
```

## Ext Serializable Decorator

```{eval-rst}
.. autodecorator:: umsgpack.ext_serializable
```

## Invalid String Class

```{eval-rst}
.. autoclass:: umsgpack.InvalidString
```

## Attributes

```{eval-rst}
.. autodata:: umsgpack.compatibility
```

## Constants

```{eval-rst}
.. autodata:: umsgpack.version
```

```{eval-rst}
.. autodata:: umsgpack.__version__
```
