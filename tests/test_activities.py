"""Tests for activities endpoints"""

import pytest
from fastapi import HTTPException


def test_get_activities(client, reset_activities):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    

def test_get_activities_structure(client, reset_activities):
    """Test that activities have the correct structure"""
    response = client.get("/activities")
    activities = response.json()
    
    # Check first activity has required fields
    first_activity = list(activities.values())[0]
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity


def test_activities_has_participants(client, reset_activities):
    """Test that activities include participant information"""
    response = client.get("/activities")
    activities = response.json()
    
    chess_club = activities["Chess Club"]
    assert isinstance(chess_club["participants"], list)
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_get_all_activities_count(client, reset_activities):
    """Test that all expected activities are returned"""
    response = client.get("/activities")
    activities = response.json()
    
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Workshop",
        "Drama Club",
        "Math Olympiad",
        "Science Club"
    ]
    
    for activity in expected_activities:
        assert activity in activities
