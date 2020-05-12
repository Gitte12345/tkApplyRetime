# tkApplyRetime.py

import maya.cmds as cmds
import maya.mel as mel
from functools import partial 

ver = 0.1

colDarkGrey			= [0.1, 0.1, 0.1]
colSilverLight 		= [0.39, 0.46, 0.50]
colSilverDark 		= [0.08, 0.09, 0.10]
colSilverMid 		= [0.23, 0.28, 0.30]
colRed 				= [0.42, 0.30, 0.30]
colGreen 			= [0.35, 0.50, 0.32]
colBlue 			= [0.20, 0.25, 0.47]

windowStartHeight = 50
windowStartWidth = 450
bh1 = 18



def cShrinkWin(windowToClose, *args):
	cmds.window(windowToClose, e=1, h=20, w=300)


def cApplySceneTimeWarp(action, *args):
	if cmds.objExists('timewarp'):
		cmds.delete('timewarp')
		print 'deleted old timewarp'

	cmds.AddTimeWarp()



def cRetimeFile(action, *args):
	timewarp = 'timewarp'
	global tkFileList
	if action == 'read':
		cBrowseFiles()



	if action == 'list':
		f=open(tkFileList[0], "r")
		if f.mode == 'r':
			retimeValues = f.read()
			print retimeValues


	if action == 'apply':
		cmds.select(clear=1)
		numKeys = cmds.keyframe(timewarp, kc=1, q=1)
		timeLast = cmds.keyframe("timewarp", q=True)[-1]
		timeFirst = cmds.keyframe("timewarp", q=True)[0]
		cmds.cutKey('timewarp', time=(timeLast,timeLast))
		print 'timeFirst:'
		print timeFirst
		print 'timeLast:'
		print timeLast

		f=open(tkFileList[0], "r")
		if f.mode == 'r':
			retimeValues = f.read().split()
			for value in range (0, len(retimeValues), 2):
				if (value == len(retimeValues)):
					print 'delete'
					cmds.cutKey('timewarp', time=(timeFirst,timeFirst))


				time = float(retimeValues[value])
				value = float(retimeValues[(value +1)])
				print time
				print value
				cmds.setKeyframe(timewarp, t=time, v=value)

		cmds.select(timewarp, r=1)
		cmds.keyTangent(itt='linear', ott='linear')



def cBrowseFiles():
	global tkFileList
	ws = cmds.workspace(fn=1)
	ws = ws + '/data'
	tkFileList = cmds.fileDialog2(dir=ws, fm=4)
	return tkFileList






def tkApplyRetimeUI(*args):
	if (cmds.window('win_tkApplyRetime', exists=1)):
		cmds.deleteUI('win_tkApplyRetime')
	myWindow = cmds.window('win_tkApplyRetime', t='tkApplyRetime ' + str(ver), s=1)

	cmds.columnLayout(adj=1, bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]))
	cmds.frameLayout('flRetime', l='Retime', bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]), cll=1, cl=0, cc='cShrinkWin("win_tkApplyRetime")')

	cmds.columnLayout(adj=1, bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]))

	cmds.button(l='Apply General Scene Time Warp', c=partial(cApplySceneTimeWarp, 'apply'), bgc=(colSilverLight[0], colSilverLight[1], colSilverLight[2]))
	cmds.setParent('..')

	cmds.rowColumnLayout(bgc=(colSilverDark[0], colSilverDark[1], colSilverDark[1]), nc=2, cw=[(1,150), (2,150)])
	cmds.button(l='Select Retime Value file', c=partial(cRetimeFile, 'read'), bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]))
	cmds.button(l='List Values', c=partial(cRetimeFile, 'list'), bgc=(colSilverMid[0], colSilverMid[1], colSilverMid[2]))
	cmds.setParent('..')

	cmds.button(l='Apply Values To Timewarp', c=partial(cRetimeFile, 'apply'), bgc=(colSilverLight[0], colSilverLight[1], colSilverLight[2]))



	cmds.showWindow(myWindow)

tkApplyRetimeUI()
partial(cShrinkWin, 'win_tkApplyRetime')
