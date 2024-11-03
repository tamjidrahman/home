from unittest.mock import patch

import pytest

from homeassistant.speaker import Speaker, SpeakerCommand


@pytest.fixture
def mock_client():
    with patch("homeassistant.speaker.client") as mock:
        yield mock


def test_get_status(mock_client):
    mock_client.get_entity_status.return_value = {
        "state": "playing",
        "attributes": {
            "media_title": "Test Song",
            "media_artist": "Test Artist",
            "media_album_name": "Test Album",
            "media_playlist": "Test Playlist",
        },
    }

    speaker = Speaker.LivingRoom
    status = speaker.get_status()

    assert status["status"] == "playing"
    assert status["media_title"] == "Test Song"
    assert status["media_artist"] == "Test Artist"
    assert status["media_album_name"] == "Test Album"
    assert status["media_playlist"] == "Test Playlist"


def test_run_status(mock_client, capsys):
    mock_client.get_entity_status.return_value = {
        "state": "paused",
        "attributes": {},
    }

    speaker = Speaker.Kitchen
    speaker.run(SpeakerCommand.STATUS)

    captured = capsys.readouterr()
    assert (
        "{'status': 'paused', 'media_title': None, 'media_artist': None, 'media_album_name': None, 'media_playlist': None}"
        in captured.out
    )


def test_run_play(mock_client):
    speaker = Speaker.Office
    speaker.run(SpeakerCommand.PLAY)
    mock_client.command_service.assert_called_with(
        "media_player", "media_play", {"entity_id": "media_player.office"}
    )


def test_run_pause(mock_client):
    speaker = Speaker.DiningRoom
    speaker.run(SpeakerCommand.PAUSE)
    mock_client.command_service.assert_called_with(
        "media_player", "media_pause", {"entity_id": "media_player.dining_room"}
    )


def test_entity_id():
    assert Speaker.LivingRoom.entity_id == "media_player.living_room"
    assert Speaker.Kitchen.entity_id == "media_player.kitchen"


def test_homeassistant_commandstr():
    assert SpeakerCommand.PLAY.homeassistant_commandstr == "media_play"
    assert SpeakerCommand.PAUSE.homeassistant_commandstr == "media_pause"
