import numpy as np


def skew(w):
    return np.array([[0, -w[2], w[1]], [w[2], 0, -w[0]], [-w[1], w[0], 0]])


def expm(w_hat, theta):
    return (
        np.eye(3) + np.sin(theta) * w_hat + (1 - np.cos(theta)) * np.dot(w_hat, w_hat)
    )


def poe(w, q, theta):
    w_hat = skew(w)
    exp_w_theta = expm(w_hat, theta)
    v = np.cross(-np.array(w), q)
    p = np.dot(
        np.eye(3) * theta
        + (1 - np.cos(theta)) * skew(w)
        + (theta - np.sin(theta)) * np.dot(skew(w), skew(w)),
        v
    )
    return np.vstack(
        (np.hstack((exp_w_theta, p.reshape(3, 1))), np.array([0, 0, 0, 1]))
    )


def computeTransform(M, joints, thetas):
    for i in range(len(thetas)):
        thetas[i] = np.deg2rad(thetas[i])

    transforms = []
    for i in range(len(joints)):
        j = joints[i]
        T = poe(j.w, j.q, thetas[i])
        transforms.append(T)

    T_s_endEffector = transforms[0]
    for i in range(len(transforms) - 1):
        T_s_endEffector = np.dot(T_s_endEffector, transforms[i + 1])

    return np.dot(T_s_endEffector, M)
