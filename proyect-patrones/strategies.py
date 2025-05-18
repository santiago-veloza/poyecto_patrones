# strategies.py
from flask import redirect, url_for

class RoleStrategy:
    def redirect_user(self, user):
        raise NotImplementedError()

class TrabajadorStrategy(RoleStrategy):
    def redirect_user(self, user):
        return redirect(url_for('trabajador_dashboard'))

class JefeStrategy(RoleStrategy):
    def redirect_user(self, user):
        return redirect(url_for('jefe_dashboard'))

class ClienteStrategy(RoleStrategy):
    def redirect_user(self, user):
        return redirect(url_for('cliente_dashboard'))

class RoleContext:
    def __init__(self, strategy: RoleStrategy):
        self.strategy = strategy

    def redirect_user(self, user):
        return self.strategy.redirect_user(user)
