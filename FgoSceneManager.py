#coding=utf-8


import time
from FgoScriptTool import FgoScriptTool
import os
class FgoSceneManager:
    def __init__(self):
        self._tool=FgoScriptTool()
    def getBonus(self,pool):
        for i in range(pool):
            self._tool.loopWait(self._tool.asPoolEmpty,assPara=None,loopMax=1000,failClickPos=(25,65),failWaitStep=0)
            self._tool.resetBonus()
            time.sleep(0.5)
    def strengthen(self,loopCount):
        for i in range(loopCount):
            self._tool.loopWait(self._tool.asStrengthenPanel,assPara=None)
            self._tool.click((50,40),0.5)
            for y in range(3):
                for x in range(5):
                    X=50+15*(x-3)+6
                    Y=40+y*25
                    self._tool.click((X,Y),0)
            self._tool.loopWait(self._tool.asStrengthenConfirmPanel,assPara=None,loopMax=None,failClickPos=(90,96),failWaitStep=0.1)
            self._tool.loopWait(self._tool.asStrengthenPanel,assPara=None,loopMax=None,failClickPos=(65,82),failWaitStep=0.1)
    def Sarum_0(self,loopCountAndtestFunc):
        # 丘陵刷钉子
        loopCount,testFunc=loopCountAndtestFunc
        tool = self._tool
        entryImage = u"imgs\\FGO\\Entry\\Sarum_0.png"
        supporterImage = u"imgs\\FGO\\Servent\\KongMing.png"

        def phase0():
            tool.enterBattle(entryImage,supporterImage)

        def phase1():
            print("************** phase1 ************")
            tool.waitReady(0.5)
            tool.serventSkill(0, 2)
            tool.startAttack()
            tool.clickNPcard(0)
            tool.clickActionCardByIndex(0)
            tool.clickActionCardByIndex(1)
            tool.waitReady()
            print("************** phase1 done ************")

        def phase2():
            print("************** phase2 ************")
            tool.waitReady()
            tool.serventSkill(1, 0)
            tool.serventSkill(2, 0, 0)
            tool.serventSkill(2, 1)
            tool.serventSkill(2, 2)
            tool.startAttack()
            tool.clickNPcard(1)
            tool.clickActionCardByIndex(0)
            tool.clickActionCardByIndex(1)
            tool.waitReady()
            print("************** phase2 done ************")

        def phase3():
            print("************** phase3 ************")
            tool.waitReady()
            tool.masterSkill(0)
            tool.serventSkill(0, 1)
            tool.serventSkill(1, 1)
            tool.startAttack()
            tool.clickNPcard(1)
            tool.clickNPcard(0)
            tool.clickActionCardByIndex(0)
            print("************** phase3 done ************")

        def phase4():
            print("************** phase4 ************")
            tool.loopWait(assFunc=tool.asBattleResultPanel, assPara=None, loopMax=1000, failClickPos=(50, 10),
                          failWaitStep=1)
            tool.click((95, 95), 0.5)
            tool.click((95, 95), 0.5)
            print("************** phase4 done ************")

        def initScript():
            try:
                testFunc()
            except Exception as e:
                pass
            pass

        def scriptLoop():
            phase0()
            phase1()
            phase2()
            phase3()
            phase4()
            try:
                testFunc()
            except Exception as e:
                pass

        self._timerStart(initScript, scriptLoop, loopCount)
    def _timerStart(self,initScript,scriptLoop,loopCount):
        tool=self._tool
        tool.log("[initScript]")
        initScript()
        tool.log("start!")
        T0 = time.time()
        for c in range(loopCount):
            print("\a")
            print("_________________________________________________________")
            tool.log("[Loop %d]" % (c + 1),1)
            print("_________________________________________________________")
            T1 = time.time()
            scriptLoop()
            print("[Time]:%.1f" % (time.time() - T1))
        if(loopCount>0):
            print("[Time Average]:%.1f" % ((time.time() - T0) / loopCount))

if __name__ == "__main__":
    mngr=FgoSceneManager()
    #mngr.getBonus(2)
    #mngr.valPlay(40)
    mngr.Sarum_0((1,None))
    #mngr.finalPlay(100)
    #mngr.finalPlay(500)
