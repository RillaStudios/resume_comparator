class Resume:
    raw_text: str
    contact: list[str] | str
    summary: str
    skills: list[str] | str
    education: list[str] | str
    experience: list[str] | str
    projects: list[str] | str
    certifications: list[str] | str
    awards: list[str] | str
    hobbies: list[str] | str
    references: list[str] | str
    unknown: list[str] | str
    bad_format: bool
    passing_list: list[str]
    failing_list: list[str]

    def __init__(self,
                 raw_text: str = "",
                 contact: list[str] | str = "",
                 summary: str = "",
                 skills: list[str] | str = None,
                 education: list[str] | str = None,
                 experience: list[str] | str = None,
                 projects: list[str] | str = None,
                 certifications: list[str] | str = None,
                 awards: list[str] | str = None,
                 hobbies: list[str] | str = None,
                 references: list[str] | str = None,
                 unknown: list[str] | str = None,
                 bad_format: bool = False,
                 passing_list: list[str] = None,
                 failing_list: list[str] = None
                 ):
        self.raw_text = raw_text
        self.contact = contact
        self.summary = summary
        self.skills = skills or []
        self.education = education or []
        self.experience = experience or []
        self.projects = projects or []
        self.certifications = certifications or []
        self.awards = awards or []
        self.hobbies = hobbies or []
        self.references = references or []
        self.unknown = unknown or []
        self.bad_format = bad_format
        self.passing_list = passing_list or []
        self.failing_list = failing_list or []