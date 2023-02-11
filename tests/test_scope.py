import pytest

from commands.scope import ScopeNew, ScopeSetCurrent
from ioc.container import Scopes  # todo: using from module scope.Scopes


class TestScopesCommand:
    """
    tests for scope command
    """

    def test_scope_new(self, mocker, scopes_test):
        scopes = scopes_test()
        mocker.patch.object(scopes, 'new_scope')
        ScopeNew(scopes=scopes, parent=10).execute()
        scopes.new_scope.assert_called()
        scopes.new_scope.assert_called_once()
        scopes.new_scope.assert_called_once_with(parent=10)

    def test_scope_set_current(self, mocker, scopes_test):
        scopes = scopes_test()
        mocker.patch.object(scopes, 'current_scope')
        ScopeSetCurrent(scopes=scopes, scope=10).execute()
        assert scopes.current_scope == 10


class TestScopes:
    """tests for scope class"""

    def test_scopes(self):
        # new SCOPES (thread local)
        scopes = Scopes()

        # auto create root scope
        assert scopes.current_scope.id == 0
        assert len(scopes.value) == 1

        # auto regitration for root scope
        assert scopes.current_scope.__getattribute__('IoC.Register')
        assert scopes.current_scope.__getattribute__('Scope.New')
        assert scopes.current_scope.__getattribute__('Scope.SetCurrent')
        with pytest.raises(AttributeError):
            assert scopes.current_scope.__getattribute__('Unregistered.dependency')

        # create new scope and set it as current
        scopes.new_scope(parent=scopes.current_scope.id)
        assert scopes.current_scope.id == 1
        assert len(scopes.value) == 2
        with pytest.raises(AttributeError):
            assert scopes.current_scope.__getattribute__('IoC.Register')
            assert scopes.current_scope.__getattribute__('Scope.New')
            assert scopes.current_scope.__getattribute__('Scope.SetCurrent')

        # set current root scope (index=0)
        scopes.current_scope = 0
        assert scopes.current_scope.id == 0
        assert len(scopes.value) == 2
        assert scopes.current_scope.__getattribute__('IoC.Register')
        assert scopes.current_scope.__getattribute__('Scope.New')
        assert scopes.current_scope.__getattribute__('Scope.SetCurrent')
        with pytest.raises(AttributeError):
            assert scopes.current_scope.__getattribute__('Unregistered.dependency')
