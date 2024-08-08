[![Actions Status](https://github.com/bytewax/bytewax-interval-operator/workflows/CI/badge.svg)](https://github.com/bytewax/bytewax-interval-operator/actions)
[![PyPI](https://img.shields.io/pypi/v/bytewax.svg?style=flat-square)](https://pypi.org/project/bytewax-interval-operator/)
[![Bytewax User Guide](https://img.shields.io/badge/user-guide-brightgreen?style=flat-square)](https://docs.bytewax.io/stable/guide/index.html)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/6073079/195393689-7334098b-a8cd-4aaa-8791-e4556c25713e.png" width="350">
  <source media="(prefers-color-scheme: light)" srcset="https://user-images.githubusercontent.com/6073079/194626697-425ade3d-3d72-4b4c-928e-47bad174a376.png" width="350">
  <img alt="Bytewax">
</picture>

## Bytewax Interval Operator

This operator allows opening "windows" whenever an item occurs on the left
side, and then pairs it with items in the right side that are
within the specified timestamp gap.

Values are always applied to the logic in timestamp (not arrival) order.

## License

bytewax-interval is commercially licensed with publicly available source code.
Please see the full details in [LICENSE](./LICENSE.md).
