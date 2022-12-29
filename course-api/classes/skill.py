class Skill:
    def __init__(self, concept_uri, description, preferred_label):
        self.concept_uri = concept_uri
        self.description = description
        self.preferred_label = preferred_label

    def print(self):
        print(f"   ------------------------")
        print(f"     - Skill preferred_label: {self.preferred_label}")
        print(f"     - Skill concept_uri: {self.concept_uri}")
        print(f"     - Skill description: {self.description}")
