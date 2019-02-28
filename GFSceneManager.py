#coding=utf-8
import win32con
from GFScriptTool import GFScriptTool
import time
from PIL import Image,ImageDraw
import pytesseract
import numpy as np
import cv2
import os
import scipy.signal as signal
import random
class GFSceneManager:
    def __init__(self):
        self.tool=GFScriptTool()
        pass
    def _timerStart(self,initScript,scriptLoop,loopCount):
        tool=self.tool
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
        print("[Time Average]:%.1f" % ((time.time() - T0) / loopCount))
    def SOP_115(self,loopCount):
        tool=self.tool
        airPort = [(48,70), (48,82), (39.5, 82)]
        battlePos = [(48,58), (39.5, 58), (39.5, 70), (31, 70), (31, 82)]

        def phase1():
            self.tool.log("[init]")
            tool.loopWait(tool.asBattle_Init, None, 10)
            self.tool.log("[init done]")

            for i in range(3):
                self.tool.log("deploy %d" % i)
                tool.clickOpenDeployPanel(airPort[i])
                tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init, None)
                self.tool.log("deploy done")
            tool.clickBattle_StartBattle()
        def phase2():

            tool.loopWait(tool.asBattle_PlanMode, assPara=False, loopMax=10, finishWait=1)
            tool.selectTeamAt(airPort[0])
            tool.clickBattle_PlanMode()
            for i in range(5):
                tool.click(battlePos[i], 0.5)
                tool.loopWait(tool.asPlanStepLeft, assPara=5 - i, failClickPos=battlePos[i])

            def code3RecoverFunc():
                # 假如中途code3出错的恢复
                tool.log("code3 recover...")
                tool.loopWait(tool.asBattle_PlanMode, False, loopMax=None)
                tool.scrollDown()

                tool.click((88, 86), 1)
                if (tool.asBattle_PlanMode(True)):
                    tool.click(airPort[0], 0.5)
                    for i in range(5):
                        tool.click(battlePos[i], 0.5)
                    tool.clickBattle_PlanMode_Start()

            tool.code3RecoverFunc = code3RecoverFunc
            tool.clickBattle_PlanMode_Start()
            tool.loopWait(tool.asBattle_PlanMode, assPara=False, loopMax=None, finishWait=0.0, failWaitStep=5)
            tool.code3RecoverFunc = None
        def phase3():
            def initSwapAndWithdraw():
                tool.loopWait(tool.asBattle_PlanMode, assPara=False, loopMax=100, finishWait=0, failWaitStep=1)
                tool.selectTeamAt(battlePos[4])
                tool.swapWith(airPort[2])
                tool.clickOpenOperatePanel(airPort[2])
                tool.clickBattle_TeamOperate_Withdraw()

            def teamFormationAdopt(index):
                tool.loopWait(tool.asBattle_PlanMode, assPara=False)
                tool.clickOpenDeployPanel(airPort[2])
                print("[enter formation]")
                tool.loopWaitRev(tool.asDeployPanel, assPara=None, failFunc=tool.asBattle_PlanMode, failPara=False,
                                 loopMax=20, failClickPos=airPort[2], failWaitStep=1)
                tool.clickBattle_Deploy_Formation()
                tool.clickEchelonFormation_Preset()
                print("[adopt option]")
                tool.clickEchelonFormation_Preset_Options_N(index)
                print("[adopt done]")
                tool.clickEchelonFormation_Preset_Finish()
                print("[finish formation]")
                tool.clickEchelonFormation_Finish()

            def deployRefuelAndWithdraw():
                print("[deploy SOP2]")
                tool.clickOpenDeployPanel(airPort[2])
                tool.clickBattle_Deploy_YesBtn(tool.asBattle_PlanMode, False)

                print("[refuel SOP2]")
                tool.clickOpenOperatePanel(airPort[2])
                tool.clickBattle_TeamOperate_Refuel()

                print("[withdraw SOP2]")
                tool.clickOpenOperatePanel(airPort[2])
                tool.clickBattle_TeamOperate_Withdraw()

            def restartGame():
                tool.clickBattle_Restart()

            print("[initSwapAndWithdraw]")
            initSwapAndWithdraw()
            print("[teamFormationAdopt(1)]")
            teamFormationAdopt(1)
            print("[deployRefuelAndWithdraw]")
            deployRefuelAndWithdraw()
            print("[teamFormationAdopt(0)]")
            teamFormationAdopt(0)
            print("[restartGame]")
            restartGame()
        def scriptLoop():

            phase1()
            phase2()
            phase3()
            pass
        def initScript():
            #phase3()
            pass
        print("start!")
        initScript()
        T0=time.time()
        for c in range(loopCount):
            print("\a")
            print("_________________________________________________________")
            print("\033[1;32m[Loop %d]\033[0m"%(c+1))
            print("_________________________________________________________")
            T1=time.time()
            scriptLoop()
            print("[Time]:%.1f"%(time.time()-T1))
        print("[Time Average]:%.1f" % ((time.time() - T0)/loopCount))
    def Zas_81n(self,loopCount):
        tool=self.tool
        airPort = [(18.5, 17), (13.5, 89.5), (88.5, 28.5)]
        battlePos = [(25, 35), (11, 41), (12, 67), (25, 51), (23, 73)]
        ZasImgsT={"Free":"imgs\\GF\\TDoll\\Zas_Free.png","T3":"imgs\\GF\\TDoll\\Zas_T3.png"}
        battlePosN=(23,63)
        airPortN=(14,80)
        def phase1():
            self.tool.log("[phase1]")
            tool.skipDlg()
            tool.loopWait(tool.asBattle_Init)
            tool.scrollUp()
            for i in range(3):
                 tool.click(airPort[i])
                 tool.loopWait( tool.asDeployPanel,failClickPos=airPort[i])
                 tool.clickBattle_Deploy_YesBtn( tool.asBattle_Init,None)
            tool.clickBattle_StartBattle()
        def phase2():
            self.tool.log("[phase2]")
            def refuelAndWithdraw():
                self.tool.log("[refuel]")
                tool.clickOpenOperatePanel(airPort[2])
                tool.clickBattle_TeamOperate_Refuel()
                self.tool.log('[withdraw]')
                tool.clickOpenOperatePanel(airPort[2])
                tool.clickBattle_TeamOperate_Withdraw()
            def planModePlannig():
                tool.selectTeamAt(airPort[0])
                tool.clickBattle_PlanMode()
                for i in range(5):
                    tool.click(battlePos[i],0.2)
                    tool.loopWait( tool.asPlanStepLeft,assPara=6-i,failClickPos=battlePos[i],failWaitStep=0.5)
            def planModeExecuting():
                tool.clickBattle_PlanMode_Start()
            refuelAndWithdraw()
            planModePlannig()
            planModeExecuting()
        def phase3():
            def wait():
                time.sleep(75)
                tool.loopWait(assFunc=tool.asBattle_PlanMode,assPara=False,loopMax=None,failWaitStep=1)
            def withdrawOriginal():
                tool.selectTeamAt(battlePosN)
                tool.click(airPortN,0.5)
                tool.click((12,76),1.5,(1,1))
                tool.clickOpenOperatePanel(airPortN)
                tool.clickBattle_TeamOperate_Withdraw()
            def reformation():
                global ZasUsed
                tool.clickOpenDeployPanel(airPortN)
                tool.clickBattle_Deploy_Formation()
                tool.click((75,50),0.5)
                pos0=tool.identifyAndFindPos("imgs\\GF\\Common\\EchelonFormation\\OrderBy.png")
                tool.click(pos0,0.5)
                pos1=tool.identifyAndFindPos("imgs\\GF\\Common\\EchelonFormation\\OrderBy_Damage.png",0.8)
                while(pos1==None):
                    tool.click(pos0,0.5)
                    pos1=tool.identifyAndFindPos("imgs\\GF\\Common\\EchelonFormation\\OrderBy_Damage.png",0.8)
                tool.click(pos1,0.2)
                pos2=tool.identifyAndFindPos(ZasImgsT["T3"])
                while(pos2==None):
                    pos2=tool.identifyAndFindPos(ZasImgsT["T3"])
                tool.click(pos2,0.5)
                tool.loopWait(tool.asEchelonFormationPanel,failClickPos=pos2,failWaitStep=0.5)



                tool.identifyAndClick("imgs\\GF\\Common\\EchelonFormation\\Echelon3.png")
                tool.click((18,50),0.5)
                pos3=tool.identifyAndFindPos(ZasImgsT["Free"])
                while (pos3 == None):
                    pos3 = tool.identifyAndFindPos(ZasImgsT["Free"])
                tool.click(pos3,0.5)
                tool.loopWait(tool.asEchelonFormationPanel,failClickPos=pos3,failWaitStep=0.5)


                tool.clickEchelonFormation_Finish()
            def restartGame():
                tool.clickBattle_Restart()
            wait()
            withdrawOriginal()
            reformation()
            restartGame()
        def scriptLoop():
            phase1()
            phase2()
            phase3()
            pass

        print("start!")
        T0 = time.time()
        for c in range(loopCount):
            print("\a")
            print("_________________________________________________________")
            print("\033[1;32m[Loop %d]\033[0m" % (c + 1))
            print("_________________________________________________________")
            T1 = time.time()
            scriptLoop()
            print("[Time]:%.1f" % (time.time() - T1))
        print("[Time Average]:%.1f" % ((time.time() - T0) / loopCount))
    def M4_44e(self,loopCount):
        tool = self.tool

        def phase1():
            #enterBattle
            tool.log("[phase1]")
            entryImage="imgs\\GF\\Common\\BattleEntry\\4-4e.png"
            normalStartImage="imgs\\GF\\Common\\BattleEntry\\NormalStart.png"
            tool.battleResultClear(1)
            def succFunc():
                if(None!=tool.identifyAndFindPos(entryImage)):
                    return True
                else:
                    return False
            tool.loopWait(succFunc,failWaitStep=0.5)
            pos0=tool.identifyAndFindPos(entryImage)
            tool.click(pos0,0.3)
            tool.loopWait(tool.asBattleNormalStart)
            pos1=tool.identifyAndFindPos(normalStartImage)
            tool.click(pos1)
            tool.loopWaitRev(tool.asBattle_Init,None,tool.asBattleNormalStart,None)
            tool.log("[phase1 done]")
        def phase2():
            airPort=[(82,66),(86,22)]
            tool.log("[phase2]")
            tool.loopWait(tool.asBattle_Init,loopMax=None)
            tool.clickOpenDeployPanel(airPort[0])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init,None)

            for i in range(4):
                tool.scrollUp()
            tool.clickOpenDeployPanel(airPort[1])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init,None)
            tool.clickBattle_StartBattle()
            tool.log("[phase2 done]")
        def phase3():
            pastPos=[(86,22),(67,22),(54,22),(37,24),(16.5,24)]
            tool.log("[phase3]")
            tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None)
            def code3RecoverFunc():
                for i in range(4):
                    tool.scrollUp()
                tool.clickBattle_PlanMode()
                for i in range(5):
                    tool.click(pastPos[i],0.5)
                tool.clickBattle_PlanMode_Start()
            tool.code3RecoverFunc=code3RecoverFunc
            tool.selectTeamAt(pastPos[0])
            tool.clickBattle_PlanMode()
            for i in range(1,5):
                tool.click(pastPos[i],0.2)
                tool.loopWait(tool.asPlanStepLeft,4-i,failClickPos=pastPos[i])
            tool.clickBattle_PlanMode_Start()
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
            #tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None,failWaitStep=1)
            tool.code3RecoverFunc=None
            tool.log("[phase3 done]")
        def phase4():
            tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None,failWaitStep=1)
            tool.click((90,90),1)
            tool.battleResultClear()
        def scriptLoop():
            phase1()
            phase2()
            phase3()
            phase4()
        def initScript():
            #phase4()
            pass
        self._timerStart(initScript,scriptLoop,loopCount)
    def M4_56(self,loopCount):
        tool = self.tool

        def phase1():
            #enterBattle
            tool.log("[phase1]")
            entryImage="imgs\\GF\\Common\\BattleEntry\\5-6.png"
            normalStartImage="imgs\\GF\\Common\\BattleEntry\\NormalStart.png"
            tool.battleResultClear(1)
            def succFunc():
                if(None!=tool.identifyAndFindPos(entryImage)):
                    return True
                else:
                    tool.scrollDown()
                    time.sleep(0.5)
                    return False
            tool.scrollDown()
            tool.loopWait(succFunc,failWaitStep=0.5)
            pos0=tool.identifyAndFindPos(entryImage)
            tool.click(pos0,0.3)
            tool.loopWait(tool.asBattleNormalStart)
            pos1=tool.identifyAndFindPos(normalStartImage)
            tool.click(pos1)
            tool.loopWaitRev(tool.asBattle_Init,None,tool.asBattleNormalStart,None)
            tool.log("[phase1 done]")
        def phase2():
            airPort=[(82,75),(84,25)]
            tool.log("[phase2]")
            tool.loopWait(tool.asBattle_Init,loopMax=None)
            tool.clickOpenDeployPanel(airPort[0])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init,None)

            for i in range(4):
                tool.scrollUp()
            tool.clickOpenDeployPanel(airPort[1])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init,None)
            tool.clickBattle_StartBattle()
            tool.log("[phase2 done]")
        def phase3():
            pastPos=[(84,25),(67,23),(53,30),(37,25),(20,30)]
            tool.log("[phase3]")
            tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None)
            def code3RecoverFunc():
                for i in range(4):
                    tool.scrollUp()
                tool.clickBattle_PlanMode()
                for i in range(5):
                    tool.click(pastPos[i],0.5)
                tool.clickBattle_PlanMode_Start()
            tool.code3RecoverFunc=code3RecoverFunc
            tool.selectTeamAt(pastPos[0])
            tool.clickBattle_PlanMode()
            for i in range(1,5):
                tool.click(pastPos[i],0.2)
                tool.loopWait(tool.asPlanStepLeft,4-i,failClickPos=pastPos[i])
            tool.clickBattle_PlanMode_Start()
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
            #tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None,failWaitStep=1)
            tool.code3RecoverFunc=None
            tool.log("[phase3 done]")
        def phase4():
            tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None,failWaitStep=1)
            tool.click((90,90),1)
            tool.battleResultClear()
        def scriptLoop():
            phase1()
            phase2()
            phase3()
            phase4()
        def initScript():
            #phase4()
            pass
        self._timerStart(initScript,scriptLoop,loopCount)

    def enterFactoryToRetire(self):
        def switchToRetirePanel():
            self.tool.log("[switch to retire panel]")
            if(self.tool.asMainPanel()):
                self.tool.log("[at main panel]")
                self.tool.identifyAndClick("imgs\\GF\\Common\\MainPanel\\factory.png")
            self.tool.loopWait(self.tool.asFactory)
            pos=(7,16+12.8*3+6.4)
            self.tool.click(pos,0.2)
            self.tool.loopWait(self.tool.asFactoryOption,assPara=3,failClickPos=pos)
        def retire2StarAll():
            self.tool.loopWait(self.tool.asFactoryOption, assPara=3)
            pos0=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png")
            self.tool.click(pos0,1.5)
            pos1 = self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png")
            self.tool.click(pos1)
            self.tool.loopWait(self.tool.asFactoryOption, assPara=3, failClickPos=pos1)
            while self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png")!=pos0:
                self.tool.click(pos1)
        def retire2StarMG():
            self.tool.loopWait(self.tool.asFactoryOption,assPara=3)
            self.tool.log("[enter selectPanel]")
            pos0 = self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png")
            self.tool.click(pos0, 1.5)
            while None==self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png"):
                pass
            self.tool.log("[at select panel]")
            pos1=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png")
            pos2=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\FilterBy_INIT.png")
            self.tool.log("[select filter]")
            self.tool.click(pos2,0.5)
            self.tool.loopWait(self.tool.asFilterOpen,failClickPos=pos2,failWaitStep=0.5)
            self.tool.log("[filter MG]")
            pos3=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\Filter\\MG_1.png")
            #self.tool.click(pos3,0.5)
            #self.tool.loopWait(self.tool.asFilterState_MG,assPara=True,failClickPos=pos3)

            self.tool.log("[auto select]")
            self.tool.click(pos1)
            self.tool.loopWait(self.tool.asFactoryOption,assPara=3,failClickPos=pos1)
            self.tool.log("[returned to factory option3]")
            while self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png")!=pos0:
                self.tool.log(pos0+","+self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png"))
                self.tool.click(pos1)
            self.tool.log("[retire done]")

            self.tool.identifyAndClick("imgs\\GF\\Common\\Factory\\selectTDoll.png")
            self.tool.click(pos3,0.5)
            self.tool.click(pos2,0.5)
            self.tool.click((5,5),0.5)
            self.tool.loopWait(self.tool.asFactoryOption,assPara=3)
            pass
        switchToRetirePanel()
        retire2StarMG()
    def start(self,script,count):
        def startScript():
            for i in range(3):
                print("\a")
                time.sleep(0.5)
            script(self,count)
            self.tool.log("[All Finish]")
            time.sleep(2)
            for i in range(50):
                print("\a",end=" ")
                time.sleep(0.5)
        startScript()
if(__name__=="__main__"):
    mngr=GFSceneManager()
    mngr.start(GFSceneManager.M4_44e,30)