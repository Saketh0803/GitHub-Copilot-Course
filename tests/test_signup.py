"""Tests for signup endpoints"""

import pytest


def test_signup_for_activity(client, reset_activities):
    """Test signing up for an activity"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newemail@mergington.edu"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newemail@mergington.edu for Chess Club"


def test_signup_adds_participant(client, reset_activities):
    """Test that signup actually adds the participant"""
    email = "newemail@mergington.edu"
    
    # Sign up
    client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signing up for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "newemail@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email(client, reset_activities):
    """Test that duplicate signups are rejected"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_activities(client, reset_activities):
    """Test signing up for multiple different activities"""
    email = "newstudent@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify in both activities
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]


def test_signup_response_format(client, reset_activities):
    """Test signup response format"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "test@mergington.edu"}
    )
    
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
