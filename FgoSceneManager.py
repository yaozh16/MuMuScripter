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
    def finalPlay(self,loopCount):
        #终本
        tool=self._tool
        rootPath="imgs\\FGO\\FinalPlay\\"
        turnPath="imgs\\FGO\\FinalPlay\\battle\\"
        actionPath = "imgs\\FGO\\FinalPlay\\actionCard\\"
        rankingBusterFirstWithNP = ["4NP", "1NP", "1B", "4B", "2B", "2NP", "1A", "4A", "2A" , "1Q", "4Q", "2Q"]
        rankingBusterOnlyWithoutNP = ["1B", "4B", "2B"]
        rankingBusterFirstWithoutNP = ["1B", "4B", "2B", "1A", "4A", "2A" , "1Q", "4Q", "2Q"]
        rankingPersonFirstWithNP = ["4NP", "1NP","2NP","1B", "1A", "1Q", "2B", "2A", "2Q" , "4B", "4A", "4Q"]

        def phase0():
            print("************** phase0 ************")
            tool.loopWait(tool.asMainPanel,assPara=None,loopMax=None)
            tool.identifyAndClick(os.path.join(rootPath, "enter.png"))
            while not tool.asSupportPanel():
                print("--eatApple")
                time.sleep(1)
                if(tool.asAPRecoverPanel()):
                    tool.eatApple()
                elif(tool.asMainPanel()):
                    tool.identifyAndClick(os.path.join(rootPath, "enter.png"))




            print("--selectSupporter")
            tool.selectGoodSupporter(os.path.join(rootPath,"goodSupporter.png"))
            print("--prepare")
            tool.identifyAndClick("imgs\\FGO\\Common\\PreparePanel.png")
            print("************** phase0 done ************")
        def phase1():
            print("************** phase1 ************")
            tool.loopWait(assFunc=tool.asBattleReady,assPara=None,failWaitStep=1,loopMax=None)
            print("\033[1;32m[battle]\033[0m%d\n" % (tool.currentBattle(turnPath)))
            if(tool.currentBattle(turnPath)>1):
                return
            tool.serventSkill(2, 2)
            tool.startAttack()
            tool.clickNPcard(2)
            tool.clickActionCardByIndex(0)
            tool.clickActionCardByIndex(1)
            tool.waitReady()
            print("************** phase1 done ************")
        def phase2():
            print("************** phase2 ************")
            tool.waitReady()
            print("\033[1;32m[battle]\033[0m%d\n" % (tool.currentBattle(turnPath)))
            if (tool.currentBattle(turnPath) > 2):
                return
            tool.serventSkill(2, 0, 1)
            tool.serventSkill(2, 1)
            tool.serventSkill(2, 2)
            tool.masterSkill(2,[2,3])

            tool.serventSkill(0, 0)
            tool.serventSkill(0, 1)
            tool.serventSkill(0, 2)

            tool.serventSkill(1, 0)
            tool.serventSkill(1, 1)
            tool.serventSkill(1, 2)

            tool.serventSkill(2, 2)

            tool.startAttack()

            tool.clickCardByRank(rankingBusterOnlyWithoutNP,actionPath)
            tool.clickNPcard(1)
            while tool.clickCardByRank(rankingBusterFirstWithoutNP,actionPath):
                pass

            tool.waitReady()
            def continueGameP2():
                tool.waitReady()
                if(tool.currentBattle(turnPath)==3):
                    return True
                else:
                    print("\033[1;32m[battle]\033[0m%d\n" % (tool.currentBattle(turnPath)))
                    tool.startAttack()
                    while tool.clickCardByRank(rankingBusterFirstWithoutNP,actionPath):
                        pass
                    tool.waitReady()
                    return False
            tool.loopWait(continueGameP2,assPara=None,loopMax=None,finishWait=1)
            print("************** phase2 done ************")
        def phase3():
            print("************** phase3 ************")
            tool.waitReady()
            print("\033[1;32m[battle]\033[0m%d\n" % (tool.currentBattle(turnPath)))
            tool.waitReady()
            tool.serventSkill(2, 0)
            tool.waitReady()
            tool.masterSkill(0)
            tool.switchEnemy(1)
            tool.masterSkill(1)#眩晕
            tool.startAttack()
            while tool.clickCardByRank(rankingPersonFirstWithNP, actionPath):
                pass
            def contineGameP3():
                if(None!=tool.identifyAndFindPos("imgs\\FGO\\FinalPlay\\finish_1.png")):
                    return True
                elif(tool.asBattleReady()):
                    print("\033[1;32m[battle]\033[0m%d\n" % (tool.currentBattle(turnPath)))
                    #需要补刀
                    tool.startAttack()
                    while tool.clickCardByRank(rankingBusterFirstWithNP, actionPath):
                        pass
                    for i in range(5):
                        tool.clickActionCardByIndex(i)
                    return False
                return False
            tool.loopWait(assFunc=contineGameP3,assPara=None,loopMax=1000,failWaitStep=0.5)
            print("************** phase3 done ************")
        def phase4():
            print("************** phase4 ************")
            tool.loopWait(assFunc=tool.asBattleResultPanel,assPara=None,loopMax=1000,failClickPos=(50,10),failWaitStep=1)
            tool.click((95,95),0.5)
            print("************** phase4 done ************")

        def initScript():
            phase0()
            phase1()
            phase2()
            phase3()
            phase4()
        def scriptLoop():
            phase0()
            phase1()
            phase2()
            phase3()
            phase4()
        #initScript()
        T0=time.time()
        for i in range(loopCount):
            T1=time.time()
            scriptLoop()
            print("\033[1;33m[Loop %d]%.1fs\033[0m\n"%(i,time.time()-T1))
        T0=time.time()-T0
        print("\033[1;33m[Total]%.1f (%.1fs per game)\033[0m\n" % (T0,T0/loopCount))
        pass


if __name__ == "__main__":
    mngr=FgoSceneManager()
    #mngr.getBonus(2)
    mngr.strengthen(5)
    #mngr.finalPlay(100)
    #mngr.finalPlay(500)