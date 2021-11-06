class Pitch:
    def __init__(self,pCategory,context,uploadedBy):
        self.pCategory = pCategory
        self.context = context
        self.uploadedBy = uploadedBy

    def save_pitch(self):
        Pitch.all_pitches.append(self)

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()