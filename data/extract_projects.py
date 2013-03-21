import os
import sys


class HackathonProject(object):
    def __init__(self, description="", people=None):
        self.description = description
        self.people = people or []


class HackathonMunger(object):
    @staticmethod
    def extract_projects(html_doc=""):
        raise NotImplementedError("Project data munger not implemented")


class Hackathon1Munger(HackathonMunger):
    pass


class Hackathon2Munger(HackathonMunger):
    pass


class Hackathon3Munger(HackathonMunger):
    pass


class Hackathon4Munger(HackathonMunger):
    pass


class Hackathon5Munger(HackathonMunger):
    pass


class Hackathon6Munger(HackathonMunger):
    pass


class Hackathon7Munger(HackathonMunger):
    pass


class Hackathon8Munger(HackathonMunger):
    pass


class Hackathon9Munger(HackathonMunger):
    pass


class Hackathon10Munger(HackathonMunger):
    pass


if __name__ == "__main__":
    data_html_dir = "/html"

    mungers = [
        Hackathon1Munger, Hackathon2Munger, Hackathon3Munger,
        Hackathon4Munger, Hackathon5Munger, Hackathon6Munger,
        Hackathon7Munger, Hackathon8Munger, Hackathon9Munger,
        Hackathon10Munger
    ]

    for hackathon_num, munger in enumerate(mungers):
        try:
            html_dump_dir = os.path.dirname(os.path.abspath(__file__))
            html_dump_file = os.path.join(html_dump_dir,
                os.path.join(data_html_dir, "%02d.html" % (hackathon_num+1)))
            with open(html_dump_file, 'r') as html_dump_fh:
                html_dump = html_dump_file.read()
            munger.extract_projects()
        except NotImplementedError as e:
            print e
