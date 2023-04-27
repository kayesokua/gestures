import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def plot_principal_component_analysis(kd, joints):
    joint_data = []
    for joint in joints:
        joint_x, joint_y, joint_z = joint + "_x", joint + "_y", joint + "_z"
        np_joint = np.stack([kd[joint_x], kd[joint_y], kd[joint_z]], axis=1)
        joint_data.append(np_joint)

    np_joints = np.concatenate(joint_data, axis=1)
    scaler = StandardScaler()
    joints_std = scaler.fit_transform(np_joints)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(joints_std)

    fig, ax = plt.subplots(figsize=(24, 12))
    plt.scatter(principal_components[:, 0], principal_components[:, 1])
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.xlim(-15,15)
    plt.ylim(-15,15)
    plt.title('PCA Visualization of Dance Data')
    plt.grid(True)
    plt.show()