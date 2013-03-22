import os

from hackathon_portal import logic, models, server_directory


class HackathonPhotoLoader(object):

    hackathon_directory_base_path = os.path.join(server_directory, 'data')

    def __init__(self, hackathon_number):
        self.hackathon = models.Hackathon.query.filter(
            models.Hackathon.number == hackathon_number
        ).one()

    def add_photo_files(self):
        hackathon_directory = os.path.join(
            self.hackathon_directory_base_path,
            str(self.hackathon.number)
        )
        for directory_path, directory_names, filenames in os.walk(hackathon_directory):
            for filename in filenames:
                with open(os.path.join(directory_path, filename), 'r') as file:
                    _, extension = filename.rsplit('.', 1)
                    photo_model = logic.save_photo(
                        file,
                        'Hackathon%d' % self.hackathon.number,
                        extension
                    )
                    logic.associate_photo_with_project(photo_model, self.hackathon)

if __name__ == '__main__':
    for i in range(7, 10):
        HackathonPhotoLoader(i).add_photo_files()