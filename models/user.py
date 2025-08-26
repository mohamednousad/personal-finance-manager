from datetime import datetime

class User:
    def __init__(self, email, name, user_id=None, created_at=None):
        self.id = user_id
        self.email = email
        self.name = name
        if created_at:
            if isinstance(created_at, str):
                try:
                    self.created_at = datetime.fromisoformat(created_at)
                except ValueError:
                    self.created_at = datetime.now()
            else:
                self.created_at = created_at
        else:
            self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            email=data.get("email"),
            name=data.get("name"),
            user_id=data.get("id"),
            created_at=data.get("created_at")
        )