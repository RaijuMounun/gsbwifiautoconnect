"""Data models for the GSB WiFi Auto Connect application."""

from dataclasses import dataclass


@dataclass
class SessionInfo:
    """Data class representing session information after login.
    
    Attributes:
        success: Whether the login was successful.
        message: Status message from the server or application.
        remaining_quota: Remaining data quota in MB.
        total_quota: Total data quota in MB.
        quota_renewal_date: Date when the quota will be renewed.
        last_login: Timestamp of the last successful login.
    """
    success: bool
    message: str
    remaining_quota: str = "---"
    total_quota: str = "---"
    quota_renewal_date: str = "---"
    last_login: str = "---"
    
    @property
    def quota_percent(self) -> float:
        """Calculate the percentage of quota used.
        
        Returns:
            Float between 0.0 and 1.0 representing usage.
            Returns 0.0 if parsing fails.
        """
        try:
            # Parse strings like "32764.83 MB" -> 32764.83
            rem_str = self.remaining_quota.split(" ")[0]
            tot_str = self.total_quota.split(" ")[0]
            
            remaining = float(rem_str)
            total = float(tot_str)
            
            if total <= 0:
                return 0.0
                
            return remaining / total
        except (ValueError, IndexError):
            return 0.0