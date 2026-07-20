"""
Unit tests for AuthService functionality
"""
import pytest
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, LoginRequest
from tests.factories.user_factory import UserFactory


@pytest.mark.asyncio
async def test_register_user(db_session):
    """Test standard registration pipeline saves user properly."""
    service = AuthService(db_session)
    req = RegisterRequest(
        email="test_reg@example.com",
        password="SecurePassword123!",
        full_name="Tester",
    )
    user = await service.register(req)
    assert user.email == "test_reg@example.com"
    assert user.full_name == "Tester"


@pytest.mark.asyncio
async def test_login_user(db_session):
    """Test user login authentication."""
    service = AuthService(db_session)
    # Register first
    req = RegisterRequest(
        email="test_login@example.com",
        password="SecurePassword123!",
        full_name="Tester",
    )
    await service.register(req)
    await db_session.commit()

    # Login
    login_req = LoginRequest(email="test_login@example.com", password="SecurePassword123!")
    res = await service.login(login_req)
    assert res.access_token is not None
    assert res.user.email == "test_login@example.com"
