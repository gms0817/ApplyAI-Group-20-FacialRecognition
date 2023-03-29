import os
import random
from skimage import io
from skimage.transform import rotate
from skimage import exposure
from numpy import fliplr, flipud


class FacialRecognition:
    def __init__(self):
        self.dataset_path = './test_dataset'
        self.photo_cap = 100
        self.num_of_pics = 0  # Track pics across single directory
        self.total_pics = 0  # Track total pics across all directories

    def load_dataset(self):
        print('Reached process_images()')
        print('Starting Image Pre-Processing...')

        # Load images recursively from directory
        for subdir, dirs, files in os.walk(self.dataset_path):
            self.num_of_pics = len(files)  # get initial number of files

            # Increment total num of pics
            self.total_pics = self.total_pics + self.num_of_pics

            for file in files:
                filetype = file[-4:]
                if filetype == '.jpg':

                    # Read the image from the file as grayscale
                    im = io.imread(os.path.join(subdir, file), as_gray=True)

                    # augment pics as needed
                    aug_count = 0
                    while self.num_of_pics < self.photo_cap:
                        aug_count = aug_count + 1  # Increment augmentation count

                        # Augment the image
                        self.augment_image(im, subdir, file, aug_count)
            print(f'Number of Pics in {subdir}: {self.num_of_pics}')

        # Print final total number of pics
        print(f'New Dataset Size: {self.total_pics}')
        print('Finished Image Pre-Processing.')

    def augment_image(self, im, subdir, file, aug_count):
        print('Reached augment_images()')

        # Randomly rotate image
        random_angle = random.randint(-90, 90)
        if self.num_of_pics < self.photo_cap:
            im_rotated = rotate(im, angle=random_angle, resize=False)

            # Configure new filepath
            filepath = os.path.join(subdir, file[:4] + f'-rotated_-{random_angle}-degrees-{aug_count}.jpg')
            if not os.path.exists(filepath):
                io.imsave(filepath, im_rotated)  # Save the image
                self.num_of_pics = self.num_of_pics + 1
                self.total_pics = self.total_pics + 1

            print(f'Number of Pictures: {self.num_of_pics} - {os.path.join(subdir, filepath)}')

        # Adjust brightness based on random gamma value
        if self.num_of_pics < self.photo_cap:
            gamma_val = random.uniform(0.5, 1.5, )
            ex_im = exposure.adjust_gamma(im_rotated, gamma=gamma_val, gain=1)

            # Configure new filepath
            ex_filepath = os.path.join(subdir, file[:4] + f'-exposure-{gamma_val}.jpg')

            # Check for existing file
            if not os.path.exists(ex_filepath):
                io.imsave(ex_filepath, ex_im)  # Save the vertically flipped im
                self.num_of_pics = self.num_of_pics + 1
                self.total_pics = self.total_pics + 1

            print(f'Number of Pictures: {self.num_of_pics} - {os.path.join(subdir, ex_filepath)}')

        # Flip image horizontally
        if self.num_of_pics < self.photo_cap:
            hor_im = fliplr(im_rotated)  # Flip horizontally

            # Configure new filepath
            hor_filepath = os.path.join(subdir, file[:4] + f'-horizontal-flip-{aug_count}.jpg')

            # Check for existing file
            if not os.path.exists(hor_filepath):
                io.imsave(hor_filepath, hor_im)  # Save the horizontally flipped im
                self.num_of_pics = self.num_of_pics + 1
                self.total_pics = self.total_pics + 1

            print(f'Number of Pictures: {self.num_of_pics} - {os.path.join(subdir, hor_filepath)}')

        # Flip image vertically
        if self.num_of_pics < self.photo_cap:
            ver_im = flipud(im_rotated)  # Flip vertically

            # Configure new filepath
            ver_filepath = os.path.join(subdir, file[:4] + f'-vertical-flip-{aug_count}.jpg')

            # Check for existing file
            if not os.path.exists(ver_filepath):
                io.imsave(ver_filepath, ver_im)  # Save the vertically flipped im
                self.num_of_pics = self.num_of_pics + 1
                self.total_pics = self.total_pics + 1

            print(f'Number of Pictures: {self.num_of_pics} - {os.path.join(subdir, ver_filepath)}')


def main():
    print('Reached main()')


if __name__ == '__main__':
    print('Launching program.')
    app = FacialRecognition()

    # Load dataset
    app.load_dataset()
