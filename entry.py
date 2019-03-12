#coding=utf-8

from GFSceneManager import GFSceneManager
from FgoSceneManager import FgoSceneManager


if __name__=="__main__":
    mngr1=GFSceneManager()
    mngr1.tool.gameTab(1)
    mngr2=FgoSceneManager()
    def testFunc():
        mngr1.tool.gameTab(0)
        mngr1.tool.mainPanelClear()
        mngr1.tool.gameTab(1)
    mngr2.Sarum_0((30,testFunc))
    mngr1.tool.gameTab(0)