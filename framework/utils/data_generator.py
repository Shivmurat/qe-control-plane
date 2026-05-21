import uuid

class DataGenerator:

    @staticmethod
    def generate_user_payload() -> dict:

        unique_id = str(uuid.uuid4())[:8]

        return {
            "name": f"user_{unique_id}",
            "job": "SDET Architect"
        }
