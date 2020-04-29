from unittest import mock


class TestStatiiView:
    @mock.patch("views.statii.ServiceRepository.find")
    def test_statii_view(self, mock_find, service, test_client):
        mock_find.return_value = [service]
        response = test_client.get("/statii")
        assert response.status_code == 200
        assert response.json == {
            "services": [
                {
                    "id": "5ea972aaed4990e6c653aa59",
                    "title": "API",
                    "checks": [{"description": "App Health", "id": None}],
                }
            ]
        }
