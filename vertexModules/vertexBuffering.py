import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QAbstractOpenGLFunctions
from PySide6.QtGui import QSurfaceFormat
from OpenGL.GL import *


class VertexBuffer:
    def __init__(self, vertices = np.array([]), color = np.array([]), texels = np.array([]), indcies = np.array([])):
        self.vertices = np.copy(vertices)
        self.vertices_bytes = vertices.nbytes
        self.color = np.copy(color)
        self.color_bytes = color.nbytes
        self.texels = np.copy(texels)
        self.texels_bytes = texels.nbytes
        self.indcies = np.copy(indcies)
        self.indcies_bytes = indcies.nbytes
        #super().__init__(parent)
        self.vao = None
        

    def buff_vex_object(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

    def buff_vertices(self):
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW )
        #glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


    def buff_colors(self):
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.color.nbytes, self.color, GL_STATIC_DRAW )
        #glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def buff_texels(self):
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.texels.nbytes, self.texels, GL_STATIC_DRAW )
        #glEnableVertexAttribArray(0)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def buff_indcies(self):
        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indcies.nbytes, self.indcies, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def bind_vex_array(self):
        glBindVertexArray(self.vao)

    def unbind_vex_array(self):
        glBindVertexArray(0)


    def deleter_attrib_buffer(self):
        glDeleteVertexArrays(1, [self.vao])

    def delete_vertex_buffer(self):
        glDeleteBuffers(1, [self.vbo])

    def delete_index_buffer(self):
        glDeleteBuffers(1, [self.ebo])



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
            gl_widget = VertexBuffer(self)

            # Set up the main layout and add the OpenGL widget to it
            layout = QVBoxLayout()
            layout.addWidget(gl_widget)

            # Create a central widget to hold the layout and set it as the main window's central widget
            central_widget = QWidget(self)
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            self.setWindowTitle("OpenGL Widget Window")
            self.resize(800, 600)
            self.show()


    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())