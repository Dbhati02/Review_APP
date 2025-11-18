import time

class ConversationManager:
    def __init__(self):
        self.sessions = {}  # {phone: {...}}

    def get(self, number):
        session = self.sessions.get(number)
        if not session:
            return {"stage": "start", "timestamp": time.time()}
        return session

    def update(self, number, data):
        data["timestamp"] = time.time()
        self.sessions[number] = data

    def reset(self, number):
        if number in self.sessions:
            del self.sessions[number]

conv = ConversationManager()
