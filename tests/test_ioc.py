import pytest

from errors.errors import IocResolveException
from ioc.container import IoC


class TestIoC:
    """ tests for IoC class"""

    def test_ioc(self):
        class TestClass:
            ...

        assert hasattr(IoC, 'resolve')
        IoC.resolve('IoC.Register', 'A', TestClass).execute()
        assert isinstance(IoC.resolve('A'), TestClass)

    def test_ioc_unresolved_dependency(self):
        with pytest.raises(IocResolveException):
            IoC.resolve('Unresolved.Dependency', 'args').execute()

    # def test_ioc_register(self):
    #     IoC._register('A', lambda x: 'A' * x)
    #     assert IoC.resolve('A', 3) == 'AAA'
