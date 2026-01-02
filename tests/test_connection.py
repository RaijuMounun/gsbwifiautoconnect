"""Unit tests for the connection module's HTML parsing logic.

Run with: pytest tests/test_connection.py -v
"""

import pytest
from connection import _parse_dashboard


# Sample HTML snippet from GSB portal (based on real captured HTML)
SAMPLE_DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head><title>GSB - Main Page</title></head>
<body>
    <label class="myinfo">Last Login: 02.01.2026 23:34</label>
    
    <table>
        <tr>
            <td><label>Total Remaining Quota (MB):</label></td>
            <td><label>32764.83</label></td>
        </tr>
        <tr>
            <td><label>Total Quota (MB):</label></td>
            <td><label>32768.0</label></td>
        </tr>
        <tr>
            <td><label>Next Refresh Date:</label></td>
            <td><label>01/02/2026 00:00:00</label></td>
        </tr>
    </table>
</body>
</html>
"""

EMPTY_HTML = "<html><body></body></html>"


class TestParseDashboard:
    """Test suite for the _parse_dashboard function."""

    def test_parse_remaining_quota(self):
        """Should correctly extract remaining quota value."""
        result = _parse_dashboard(SAMPLE_DASHBOARD_HTML)
        assert result["quota"] == "32764.83 MB"

    def test_parse_total_quota(self):
        """Should correctly extract total quota value (New feature)."""
        result = _parse_dashboard(SAMPLE_DASHBOARD_HTML)
        assert result["total_quota"] == "32768.0 MB"

    def test_parse_next_refresh_date(self):
        """Should correctly extract and format the refresh date."""
        result = _parse_dashboard(SAMPLE_DASHBOARD_HTML)
        assert result["date"] == "01/02/2026"

    def test_parse_last_login(self):
        """Should correctly extract last login timestamp."""
        result = _parse_dashboard(SAMPLE_DASHBOARD_HTML)
        assert result["last_login"] == "02.01.2026 23:34"

    def test_empty_html_returns_defaults(self):
        """Should return 'Not Found' for all fields when HTML is empty."""
        result = _parse_dashboard(EMPTY_HTML)
        assert result["quota"] == "Not Found"
        assert result["total_quota"] == "Not Found"
        assert result["date"] == "Not Found"
        assert result["last_login"] == "Not Found"

    def test_malformed_html_does_not_crash(self):
        """Should handle malformed HTML gracefully without raising exceptions."""
        malformed = "<html><body><label>Total Remaining Quota (MB):</label>"
        result = _parse_dashboard(malformed)
        # Should not crash, may return partial or default values
        assert isinstance(result, dict)
        assert "quota" in result
