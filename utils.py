import numpy as np
import numpy.linalg as la
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtQml import QQmlListProperty
import math


def perspective_projection (fovy, aspect_ratio, near_z, far_z):
	m = np.zeros(shape = (4, 4))

	t = np.tan(np.radians(fovy) / 2.0)  # half width

	m[0][0] = 1.0 / (aspect_ratio * t)
	m[1][1] = 1.0 / t
	m[2][2] = -(far_z + near_z) / (far_z - near_z)
	m[2][3] = -1.0
	m[3][2] = -(2.0 * far_z * near_z) / (far_z - near_z)

	return m


def look_at (eye, center, up):
	f = normalize_vector(center - eye)
	u = normalize_vector(up)
	s = normalize_vector(np.cross(f, u))
	u = np.cross(s, f)

	m = np.identity(4)

	m[0, :] = np.array([s[0], s[1], s[2], -np.dot(s, eye)])
	m[1, :] = np.array([u[0], u[1], u[2], -np.dot(u, eye)])
	m[2, :] = np.array([-f[0], -f[1], -f[2], np.dot(f, eye)])

	return m


# assuming the volume is symmetric such that no need to specify l, r, t, b
# Tested against glm::ortho(l, r, b, t, near_z, far_z) with
# glm::mat4 p = glm::ortho(-320.0f, 320.0f, -240.0f, 240.0f, 0.001f, 100.0f);
# TODO should be farther tested
def orthographic_projection (w, h, near_z, far_z):
	m = np.zeros(shape = (4, 4))

	m[0][0] = 2.0 / w
	m[1][1] = 2.0 / h
	m[2][2] = -2.0 / (far_z - near_z)
	m[2][3] = -(far_z + near_z) / (far_z - near_z)
	m[3][3] = 1

	return m


def normalize_vector (v):
	return v / la.norm(v)


def rotate_x (angle):
	rad = np.radians(angle)
	m = np.identity(4)
	m[0][0] = 1.0
	m[1][1] = np.cos(rad)
	m[1][2] = -np.sin(rad)
	m[2][1] = np.sin(rad)
	m[2][2] = np.cos(rad)
	return m


def rotate_y (angle):
	rad = np.radians(angle)
	m = np.identity(4)
	m[0][0] = np.cos(rad)
	m[0][2] = np.sin(rad)
	m[1][1] = 1.0
	m[2][0] = -np.sin(rad)
	m[2][2] = np.cos(rad)
	return m


def rotate_z (angle):
	rad = np.radians(angle)
	m = np.identity(4)
	m[0][0] = np.cos(rad)
	m[0][1] = -np.sin(rad)
	m[1][0] = np.sin(rad)
	m[1][1] = np.cos(rad)
	m[2][2] = 1.0
	return m


def translate (trans):
	m = np.identity(4)
	m[0][3] = trans[0]
	m[1][3] = trans[1]
	m[2][3] = trans[2]
	return m


def scale (scale_vec):
	m = np.identity(4)
	m[0][0] = scale_vec[0]
	m[1][1] = scale_vec[1]
	m[2][2] = scale_vec[2]
	return m


def create_transformation_matrix (trans,
                                  rotation,
                                  scale_val):
	m = np.identity(4)
	m1 = translate(trans)
	m2 = rotate_x(rotation[0])
	m3 = rotate_y(rotation[1])
	m4 = rotate_z(rotation[2])
	m5 = scale(scale_val)

	m = m5 @ m4 @ m3 @ m2 @ m1 @ m

	return m
