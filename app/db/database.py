from odmantic import AIOEngine

engine = AIOEngine()

def get_engine() -> AIOEngine:
    return engine