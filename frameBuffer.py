import sys
import numpy as np
from PIL import ImageDraw
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QSurfaceFormat
from OpenGL.GL import *


from shaderModules.ShaderCompilation import ShaderProgram
from textureModules.textureGen import TextureGen
from vertexModules.vertexBuffering import VertexBuffer


class MyOpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fragmentShader = None
        self.screenShader = None
        self.screen_vao = None
        self.frame_texel = None
        self.image_texel = None
        self.frame_buffer = None
        self.render_buffer = None

        # qt timer
        self.gl_timer = QTimer()
        self.gl_timer.timeout.connect(self.update)
        self.gl_timer_interval = 128
        self.gl_timer.start(self.gl_timer_interval)
        self.gl_time_laps = 0
       

    def version_status(self):
        version = glGetString(GL_VERSION)
        print(f"OpenGL version: {version.decode('utf-8')}")
        version = glGetString(GL_SHADING_LANGUAGE_VERSION)
        print(f"OpenGL shader language: {version.decode('utf-8')}")

    def create_frame(self):
        # load current texture
        #######
        # optomize the image
        # use PLI
        texel = TextureGen(file_path="images/default.png")
        if texel.load_image_file():
            texel.texture_wrap()
            texel.load_texture()
            self.frame_texel = texel

        # create fragment shader
        frameBuffer = glGenFramebuffers(1)
        self.frame_buffer = frameBuffer
        glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.frame_texel.texture_id, 0)

        # create and attach a depth render buffer
        renderBuffer = glGenRenderbuffers(1)
        self.render_buffer = renderBuffer
        glBindRenderbuffer(GL_RENDERBUFFER, renderBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, 600, 600)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, renderBuffer)

        # Check if the framebuffer is complete
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            print(status)
            raise Exception("Framebuffer is not complete!")

        # unbind frame buffer and render buffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # glBindRenderbuffer(GL_RENDERBUFFER, 0)

    
    def create_screen(self):
        vertex = np.array([(-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (1.0, -1.0, 0.0)], np.float32)
        color = np.array([(1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0)], np.float32)
        tex_coord = np.array([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)], np.float32)
        self.screen_vao = VertexBuffer(vertices= vertex, color=color, texels= tex_coord)
        self.screen_vao.buff_vex_object()
        self.screen_vao.buff_vertices()
        self.screen_vao.buff_colors()
        self.screen_vao.buff_texels()
        self.screen_vao.unbind_vex_array()

    def create_frame_plane(self):
        vertex = np.array([(-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (1.0, -1.0, 0.0)], np.float32)
        color = np.array([(1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 1.0)], np.float32)
        tex_coord = np.array([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)], np.float32)
        self.frame_vao = VertexBuffer(vertices= vertex, color=color, texels= tex_coord)
        self.frame_vao.buff_vex_object()
        self.frame_vao.buff_vertices()
        self.frame_vao.buff_colors()
        self.frame_vao.buff_texels()
        self.frame_vao.unbind_vex_array()

        




    def initializeGL(self):
        # Add any OpenGL initialization code here
        glClearColor(0, 1, 0, 0)
        self.version_status()

        # compile fragment shader program
        Shader_program = ShaderProgram("shaderProgram/shaderOne")
        Shader_program.makeShaderProgram()
        self.fragmentShader = Shader_program

        # compile screen shader program
        screen_shader = ShaderProgram("shaderProgram/screenShader")
        screen_shader.makeShaderProgram()
        self.screenShader = screen_shader

        # set screen vertices
        self.create_screen()

        # create frame buffer
        self.create_frame()

        # set frame vao
        self.create_frame_plane()

        

    def resizeGL(self, width, height):
        # Handle resizing of the OpenGL widget here
        glViewport(0, 0, width, height)



    def paintGL(self):
        # gl time laps
        self.gl_time_laps += .3
        # print(self.gl_time_laps)

        # Add your OpenGL rendering code here
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 0)

        # bind frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.frame_buffer)
        # glEnable(GL_DEPTH_TEST)
        self.frame_vao.bind_vex_array()
        glUseProgram(self.fragmentShader.shaderProgram)

        # enable attributes of frame_vao
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        # unifrom variable of frame_vao
        location = glGetUniformLocation(self.fragmentShader.shaderProgram, "time_laps")
        glUniform1f(location, self.gl_time_laps)
       

        glDrawArrays(GL_TRIANGLES, 0, self.frame_vao.vertices_bytes)
        glBindFramebuffer(GL_FRAMEBUFFER, 2)
        # print(self.frame_texel.image.width, self.frame_texel.image.width)


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 0)


        # enable the screen vao
        self.screen_vao.bind_vex_array()

        # use screen shader program
        glUseProgram(self.screenShader.shaderProgram)

        # Enable attributes
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        # unifrom texture sample
        glBindTexture(GL_TEXTURE_2D, self.frame_texel.texture_id)
        location = glGetUniformLocation(self.screenShader.shaderProgram, "textureSample")
        glUniform1i(location, 0)

        glDrawArrays(GL_TRIANGLES, 0, self.screen_vao.vertices_bytes)
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        sformat = QSurfaceFormat()
        sformat.setMajorVersion(4)
        sformat.setProfile(QSurfaceFormat.CoreProfile)
        sformat.setDefaultFormat(sformat)
        self.initUI()

    def initUI(self):
        # Create an instance of your custom OpenGL widget
        gl_widget = MyOpenGLWidget(self)

        # Set up the main layout and add the OpenGL widget to it
        layout = QVBoxLayout()
        layout.addWidget(gl_widget)

        # Create a central widget to hold the layout and set it as the main window's central widget
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("OpenGL Widget Window")
        self.resize(830, 625)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
