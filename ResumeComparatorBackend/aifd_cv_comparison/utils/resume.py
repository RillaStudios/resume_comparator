from aifd_cv_comparison.utils.resume_contact import ResumeContact


class Resume:
    raw_text: str
    contact: ResumeContact
    summary: str
    skills: str
    education: str
    experience: str
    projects: str
    certifications: str
    awards: str
    hobbies: str
    references: str
    unknown: str
    bad_format: bool
    passing_list: list[str]
    failing_list: list[str]

    def __init__(self,
                 raw_text: str = "",
                 contact: ResumeContact = None,
                 summary: str = "",
                 skills: str = None,
                 education: str = None,
                 experience: str = None,
                 projects: str = None,
                 certifications: str = None,
                 awards: str = None,
                 hobbies: str = None,
                 references: str = None,
                 unknown: str = None,
                 bad_format: bool = False,
                 passing_list: list[str] = None,
                 failing_list: list[str] = None
                 ):
        self.raw_text = raw_text
        self.contact = ResumeContact() if contact is None else contact
        self.summary = summary
        self.skills = skills
        self.education = education
        self.experience = experience
        self.projects = projects
        self.certifications = certifications
        self.awards = awards
        self.hobbies = hobbies
        self.references = references
        self.unknown = unknown
        self.bad_format = bad_format
        self.passing_list = passing_list or []
        self.failing_list = failing_list or []