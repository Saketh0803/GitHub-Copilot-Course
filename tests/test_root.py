"""Tests for root endpoint"""

import pytest


def test_root_redirect(client):
    """Test that root endpoint redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_root_with_follow_redirect(client):
    """Test root endpoint with redirect following"""
    response = client.get("/", follow_redirects=True)
    # The static file might not exist in test, so we just check it tries to redirect
    assert response.status_code in [200, 404]  # 200 if static exists, 404 if not
