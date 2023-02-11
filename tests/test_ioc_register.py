# todo: use imports:
# from commands.ioc_register import Register
# from scope import Scopes

from ioc.container import IoC
from ioc.container import Register


class TestIocRegisterCommand:
    """
    tests for scope command
    """

    def test_ioc_register(self, mocker, scopes_test):
        scopes = scopes_test()
        mocker.patch.object(IoC, 'scopes', scopes)
        scopes.current_scope = mocker.PropertyMock()
        Register(key='test.key', func=print).execute()
        assert scopes.current_scope.__getattribute__('test.key')
        assert scopes.current_scope.__getattribute__('test.key') is print

    def test_ioc_register_call(self):
        Register(key='test.key', func=lambda x: x ** 2).execute()
        assert IoC.scopes.current_scope.__getattribute__('test.key')
        assert IoC.scopes.current_scope.__getattribute__('test.key')(7) == 49  # 7 ** 2
