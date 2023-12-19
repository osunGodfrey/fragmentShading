from OpenGL.GL import *
from PIL import Image


class TextureGen:
    def __init__(self, file_path="", image_data = None):
        self.image_path = file_path
        self.image_data = image_data
        self.image_load = False
        self.texture_id = None

    def load_image_file(self):
        try:
            self.image = Image.open(self.image_path)
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
            self.image_data = self.image.tobytes()
            self.image_load = True
            return True
        except Exception as e:
            print(f"Failed to load texture {e}")
            return False

    def texture_wrap(self):
        self.texture_id = glGenTextures(1)

        # gl bind texture id
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        # set texture warps and filters
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # unbind texture
        glBindTexture(GL_TEXTURE_2D, 0)

    def load_texture(self):
        # gl bind texture id
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        if self.image_load == True:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image.width,
                         self.image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.image_data)
            glGenerateMipmap(GL_TEXTURE_2D)
            # unbind texture
        glBindTexture(GL_TEXTURE_2D, 0)

    

