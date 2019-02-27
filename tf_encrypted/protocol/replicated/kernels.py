import tensorflow as tf

from .types import Dtypes
from .replicated import AddPrivatePrivate, SubPrivatePrivate, \
    MulPrivatePrivate, CastFixed10, CastFixed16, \
    CastReplicated3

kernels = {}

fixed10_replicated3 = (Dtypes.REPLICATED3, Dtypes.FIXED10)
fixed16_replicated3 = (Dtypes.REPLICATED3, Dtypes.FIXED16)
integer_replicated3 = (Dtypes.REPLICATED3, Dtypes.INTEGER)


def register(kernel, dtype_tuple):
    op = kernel.op
    if len(dtype_tuple) != op.num_inputs:
        raise TypeError("Kernel type sig must match number of inputs of op")

    try:
        kernels[op.name][dtype_tuple] = kernel
    except KeyError:
        kernels[op.name] = {}
        kernels[op.name][dtype_tuple] = kernel


def dispatch(context, name, *args, **kwargs):
    dtype_list = []
    for arg in args:
        try:
            dtype_list.append(arg.dtype)
        except AttributeError:
            dtype_list.append(arg)

    dtype_tuple = tuple(dtype_list)
    kernel = kernels[name][dtype_tuple]
    op = kernel.op

    if len(op.attrs) > 0:
        return kernel(context, *args, **kwargs)
    else:
        return kernel(context, *args)


def register_all():
    register(AddPrivatePrivate(), (fixed10_replicated3, fixed10_replicated3))
    register(SubPrivatePrivate(), (fixed10_replicated3, fixed10_replicated3))
    register(MulPrivatePrivate(), (fixed10_replicated3, fixed10_replicated3))

    register(AddPrivatePrivate(), (fixed16_replicated3, fixed16_replicated3))
    register(SubPrivatePrivate(), (fixed16_replicated3, fixed16_replicated3))
    register(MulPrivatePrivate(), (fixed16_replicated3, fixed16_replicated3))

    register(AddPrivatePrivate(), (integer_replicated3, integer_replicated3))
    register(SubPrivatePrivate(), (integer_replicated3, integer_replicated3))
    register(MulPrivatePrivate(), (integer_replicated3, integer_replicated3))

    register(CastFixed10(), (tf.float32, Dtypes.FIXED10))
    register(CastFixed16(), (tf.float32, Dtypes.FIXED16))

    register(CastReplicated3(), (Dtypes.FIXED10, Dtypes.REPLICATED3))
    register(CastReplicated3(), (tf.int32, Dtypes.REPLICATED3))
    # TODO float right to replicated3
