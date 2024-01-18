import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QAbstractOpenGLFunctions
from PySide6.QtGui import QSurfaceFormat
from OpenGL.GL import *

class ShaderProgram:
    def __init__(self, file_path = None):
        self.file_path = file_path
        self.vertex_shader = ""
        self.fragment_shader = ""
        self.shaderProgram = None
        self.initilize_vertex_shader()
        self.initilize_fragment_shader()
        


    def initilize_vertex_shader(self):
        # Step 1: Open the text document for reading
        file_content = ""
        try:
            with open(self.file_path + "/vertex_shader.glsl", "r") as file :
                file_content = file.read()
                print(file_content)
        except FileNotFoundError:
            print("file was not found")
        except Exception:
            print("file was not found")
        self.vertex_shader = file_content


    def initilize_fragment_shader(self):
        file_content = ""
        try:
            with open(self.file_path + "/fragment_shader.glsl", "r") as file :
                file_content = file.read()
                print(file_content)
        except FileNotFoundError:
            print("file was not found")
        except Exception:
            print("file was not found")
        self.fragment_shader = file_content

    def makeShaderProgram(self):
        # compile vertex and fragment shader
        shader_program = glCreateProgram()
        compiled_vertex_shader = self.compile_shader(self.vertex_shader, GL_VERTEX_SHADER)
        compiled_fragment_shader = self.compile_shader(self.fragment_shader, GL_FRAGMENT_SHADER)
        # # attach your shaders
        glAttachShader(shader_program, compiled_vertex_shader)
        glAttachShader(shader_program, compiled_fragment_shader)
        glLinkProgram(shader_program)
        # delete shaders
        glDeleteShader(compiled_vertex_shader)
        glDeleteShader(compiled_fragment_shader)
        self.shaderProgram = shader_program
        print(shader_program)
        print("shader complete")


    def compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        # check compilation error
        success = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if not success:
            info_log = glGetShaderInfoLog(shader).decode('utf-8')
            print(f"Shader compilation failed:\n{info_log}")
            glDeleteShader(shader)
            return None
        return shader
    
    def set_texture_unit(self, unit):
        # gl bind texture unit
        glBindTextureUnit(unit, self.shaderProgram)
    
    def delete_shader_program(self):
        glDeleteProgram(self.shaderProgram)



if __name__ == "__main__":

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
            gl_widget = ShaderProgram("fragmentShading/shaderProgram/shaderOne")
            gl_widget.makeShaderProgram()

            # Set up the main layout and add the OpenGL widget to it
            # layout = QVBoxLayout()
            # layout.addWidget(gl_widget)

            # Create a central widget to hold the layout and set it as the main window's central widget
            central_widget = QWidget(self)
            # central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            self.setWindowTitle("OpenGL Widget Window")
            self.resize(800, 600)
            self.show()


    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    
    
