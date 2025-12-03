"""Tests for unregister endpoints"""

import pytest


def test_unregister_from_activity(client, reset_activities):
    """Test unregistering from an activity"""
    email = "michael@mergington.edu"
    
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_unregister_removes_participant(client, reset_activities):
    """Test that unregister actually removes the participant"""
    email = "michael@mergington.edu"
    
    # Unregister
    client.delete(
        f"/activities/Chess Club/participants/{email}"
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregistering from non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent Activity/participants/test@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_not_participant(client, reset_activities):
    """Test unregistering non-participant from activity"""
    response = client.delete(
        "/activities/Chess Club/participants/notparticipant@mergington.edu"
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_response_format(client, reset_activities):
    """Test unregister response format"""
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_then_unregister(client, reset_activities):
    """Test full signup and unregister flow"""
    email = "temp@mergington.edu"
    
    # Sign up
    signup_response = client.post(
        "/activities/Math Olympiad/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Verify signup
    response = client.get("/activities")
    assert email in response.json()["Math Olympiad"]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/Math Olympiad/participants/{email}"
    )
    assert unregister_response.status_code == 200
    
    # Verify removal
    response = client.get("/activities")
    assert email not in response.json()["Math Olympiad"]["participants"]
