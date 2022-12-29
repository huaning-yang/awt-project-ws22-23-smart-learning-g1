class Skill:
  def __init__(self, concept_uri, description, title):
    self.concept_uri = concept_uri
    self.description = description
    self.title = title
  
  def print(self):
    print(f"   ------------------------")
    print(f"     - Skill title: {self.title}")
    print(f"     - Skill concept_uri: {self.concept_uri}")
    print(f"     - Skill description: {self.description}")
