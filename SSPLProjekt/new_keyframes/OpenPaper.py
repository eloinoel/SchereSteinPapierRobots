def OpenPaper():
	names = list()
	times = list()
	keys = list() 

	names.append('HeadYaw')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('HeadPitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LShoulderPitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[1.49, [0, 1, 2], [0, 1, 2]], [0.99, [0, 1, 2], [0, 1, 2]], [0.5, [0, 1, 2], [0, 1, 2]], [0.18, [0, 1, 2], [0, 1, 2]], [0.18, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [1.49, [0, 1, 2], [0, 1, 2]]])

	names.append('LShoulderRoll')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.51, [0, 1, 2], [0, 1, 2]], [0.73, [0, 1, 2], [0, 1, 2]], [0.96, [0, 1, 2], [0, 1, 2]], [0.96, [0, 1, 2], [0, 1, 2]], [1.5, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LElbowYaw')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[-1.15, [0, 1, 2], [0, 1, 2]], [-1.15, [0, 1, 2], [0, 1, 2]], [-1.15, [0, 1, 2], [0, 1, 2]], [-1.44, [0, 1, 2], [0, 1, 2]], [-1.44, [0, 1, 2], [0, 1, 2]], [-1.44, [0, 1, 2], [0, 1, 2]], [-1.15, [0, 1, 2], [0, 1, 2]]])

	names.append('LElbowRoll')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [-0.51, [0, 1, 2], [0, 1, 2]], [-1.04, [0, 1, 2], [0, 1, 2]], [-1.5, [0, 1, 2], [0, 1, 2]], [-1.5, [0, 1, 2], [0, 1, 2]], [-1.5, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LHipYawPitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LHipRoll')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LHipPitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LKneePitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LAnklePitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LAnkleRoll')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RShoulderPitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[1.49, [0, 1, 2], [0, 1, 2]], [0.99, [0, 1, 2], [0, 1, 2]], [0.5, [0, 1, 2], [0, 1, 2]], [0.18, [0, 1, 2], [0, 1, 2]], [0.18, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [1.49, [0, 1, 2], [0, 1, 2]]])

	names.append('RShoulderRoll')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [-0.53, [0, 1, 2], [0, 1, 2]], [-0.75, [0, 1, 2], [0, 1, 2]], [-1.07, [0, 1, 2], [0, 1, 2]], [-1.07, [0, 1, 2], [0, 1, 2]], [-1.5, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RElbowYaw')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[1.07, [0, 1, 2], [0, 1, 2]], [1.07, [0, 1, 2], [0, 1, 2]], [1.14, [0, 1, 2], [0, 1, 2]], [1.46, [0, 1, 2], [0, 1, 2]], [1.46, [0, 1, 2], [0, 1, 2]], [1.46, [0, 1, 2], [0, 1, 2]], [1.07, [0, 1, 2], [0, 1, 2]]])

	names.append('RElbowRoll')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.5, [0, 1, 2], [0, 1, 2]], [0.98, [0, 1, 2], [0, 1, 2]], [1.49, [0, 1, 2], [0, 1, 2]], [1.49, [0, 1, 2], [0, 1, 2]], [1.49, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RHipYawPitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RHipRoll')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RHipPitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RKneePitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RAnklePitch')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RAnkleRoll')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LWristYaw')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('LHand')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RWristYaw')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])

	names.append('RHand')
	times.append([0.0, 0.25, 0.5, 1.0, 1.5, 4.0, 5.0])
	keys.append([[0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0, [0, 1, 2], [0, 1, 2]], [0.0, [0, 1, 2], [0, 1, 2]]])
	return names, times, keys