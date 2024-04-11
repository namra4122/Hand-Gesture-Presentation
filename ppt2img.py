import os
import threading
from spire.presentation.common import *
from spire.presentation import *

class PPTConverter:
    def __init__(self):
        self.presentation = Presentation()

    def set_ppt_path(self, ppt_path):
        self.ppt_path = ppt_path

    def convert_to_images(self, output_directory):
        try:
            self.presentation.LoadFromFile(self.ppt_path)

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            threads = []
            for i, slide in enumerate(self.presentation.Slides):
                thread = threading.Thread(target=self._save_slide_as_image, args=(slide, output_directory, i))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.presentation.Dispose()

    def _save_slide_as_image(self, slide, output_directory, index):
        try:
            fileName = f"{output_directory}{index}.png"
            image = slide.SaveAsImage()
            image.Save(fileName)
        except Exception as e:
            print(f"Error converting slide {index}: {e}")
        finally:
            if 'image' in locals():
                image.Dispose()

if __name__ == "__main__":
    PPTConverter()
    



# ppt to png_folder
from ppt2img import PPTConverter

ppt_path = "Dickinson_Sample_Slides.pptx"
output_folder = "ppt2pngOutput/"

# converter = PPTConverter()
# converter.set_ppt_path(ppt_path)
# converter.convert_to_images(output_folder)