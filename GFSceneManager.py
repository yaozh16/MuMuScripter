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
        self.countDown=0
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
    def SOP_115(self,loopCountAndUseSkill):
        loopCount,useSkillStyle=loopCountAndUseSkill
        tool=self.tool
        airPort = [(48,70), (48,82), (39.5, 82)]
        battlePos = [(48,58), (39.5, 58), (39.5, 70), (31, 70), (31, 82)]

        def phase1_deployStart():
            self.tool.log("[init]")
            tool.loopWait(tool.asBattle_Init, None, 10)
            self.tool.log("[init done]")

            for i in range(3):
                self.tool.log("deploy %d" % i)
                tool.clickOpenDeployPanel(airPort[i])
                tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init, None)
                self.tool.log("deploy done")
            tool.clickBattle_StartBattle(planMode=True)
        def phase2_s1_planExecute_1():
            #tool.clickSelectTeamAt(airPort[0])
            route1=[airPort[0]]
            route1.extend(battlePos[0:1])
            tool.clickExecutePlanMode(route1,6)
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
        def phase2_s1_planExecute_2():
            #tool.clickSelectTeamAt(battlePos[2])
            tool.clickTurnFairyAutoSkill(True)
            tool.scrollDown()
            tool.scrollDown()
            route2=battlePos[0:4]
            tool.clickExecutePlanMode(route2,5)
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
            tool.clickTurnFairyAutoSkill(False)
        def phase2_s1_planExecute_3():

            route3=battlePos[3:5]
            tool.clickExecutePlanMode(route3,2)
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
        def phase2_s2_planExecute_1():

            #tool.clickSelectTeamAt(airPort[0])
            route1=[airPort[0]]
            route1.extend(battlePos[0:3])
            tool.clickExecutePlanMode(route1,6)
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
        def phase2_s2_planExecute_2():
            #tool.clickSelectTeamAt(battlePos[2])
            tool.clickTurnFairyAutoSkill(True)
            route2=battlePos[2:4]
            tool.clickExecutePlanMode(route2,3)
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
            tool.clickTurnFairyAutoSkill(False)
        def phase2_s2_planExecute_3():

            route3=battlePos[3:5]
            tool.clickExecutePlanMode(route3,2)
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
        def phase2_s3_planExecute():
            # tool.clickSelectTeamAt(airPort[0])
            route1 = [airPort[0]]
            route1.extend(battlePos)
            tool.clickExecutePlanMode(route1, 6)
            while (not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
        def phase3_initSwapAndWithdraw():
            tool.loopWait(tool.asBattle_PlanMode, assPara=False, loopMax=None, finishWait=0, failWaitStep=1)
            tool.clickSelectTeamAt(battlePos[4])
            tool.clickSwapWith(airPort[2])
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
        def phase4_deployRefuelAndWithdraw():
            print("[deploy SOP2]")
            tool.clickOpenDeployPanel(airPort[2])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_PlanMode, False)

            print("[refuel SOP2]")
            tool.clickOpenOperatePanel(airPort[2])
            tool.clickBattle_TeamOperate_Refuel()

            print("[withdraw SOP2]")
            tool.clickOpenOperatePanel(airPort[2])
            tool.clickBattle_TeamOperate_Withdraw()
        def phase5_restartGame():
            tool.clickBattle_Restart()
        def scriptLoop():
            phase1_deployStart()
            if(useSkillStyle==3):
                phase2_s1_planExecute_1()
                phase2_s1_planExecute_2()
                phase2_s1_planExecute_3()
            elif(useSkillStyle==1):
                phase2_s2_planExecute_1()
                phase2_s2_planExecute_2()
                phase2_s2_planExecute_3()
            else:
                phase2_s3_planExecute()

            phase3_initSwapAndWithdraw()
            teamFormationAdopt(1)
            phase4_deployRefuelAndWithdraw()
            teamFormationAdopt(0)

            self.collectingPhase()
            phase5_restartGame()
            pass
        def initScript():
            '''phase1_deployStart()
            phase2_s1_planExecute_2()
            phase2_s1_planExecute_3()
            phase2_s2_planExecute_2()
            phase2_s2_planExecute_3()
            phase3_initSwapAndWithdraw()
            teamFormationAdopt(1)
            phase4_deployRefuelAndWithdraw()
            teamFormationAdopt(0)
            phase5_restartGame()
            '''
            pass

        self._timerStart(initScript=initScript,scriptLoop=scriptLoop,loopCount=loopCount)
    def Zas_81n(self,loopCount_UseSupport):
        loopCount,useSupport=loopCount_UseSupport
        tool=self.tool
        airPort = [(18.5, 17), (13.5, 89.5), (88.5, 28.5)]
        battlePos = [(25, 35), (11, 41), (12, 67), (25, 51), (23, 73)]
        ZasImgsT={"Free":"imgs\\GF\\TDoll\\Zas_Free.png","T3":"imgs\\GF\\TDoll\\Zas_T3.png"}
        battlePosN=(23,63)
        airPortN=(14,80)
        def phase1():
            #deploy and start
            self.tool.log("[phase1]")
            tool.skipDlg()
            tool.loopWait(tool.asBattle_Init)
            tool.scrollUp()
            tool.scrollUp()
            for i in range(3):
                 tool.click(airPort[i])
                 tool.loopWait( tool.asDeployPanel,failClickPos=airPort[i])
                 tool.clickBattle_Deploy_YesBtn( tool.asBattle_Init,None)
            tool.clickBattle_StartBattle()
        def phase2_refuelAndWithdraw():
            self.tool.log("[refuel]")
            tool.clickOpenOperatePanel(airPort[2])
            tool.clickBattle_TeamOperate_Refuel()
            self.tool.log('[withdraw]')
            tool.clickOpenOperatePanel(airPort[2])
            tool.clickBattle_TeamOperate_Withdraw()
            pass
        def phase2_planModeExecuting():
            tool.clickSelectTeamAt(airPort[0])
            tool.clickBattle_PlanMode()
            for i in range(5):
                tool.click(battlePos[i], 0.2)
                tool.loopWait(tool.asPlanStepLeft, assPara=6 - i, failClickPos=battlePos[i], failWaitStep=0.5)
            tool.clickBattle_PlanMode_Start()
        def phase3():
            def wait():
                time.sleep(75)
                tool.loopWait(assFunc=tool.asBattle_PlanMode,assPara=False,loopMax=None,failWaitStep=1)
            def withdrawOriginal():
                tool.clickSelectTeamAt(battlePosN)
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
            wait()
            withdrawOriginal()
            reformation()
        def phase4_1():
            def subphase1():
                tool.log("[deploy supportTeam]")
                tool.clickDeploySupportTeam(airPortN, tool.asBattle_PlanMode, False)
                tool.log("[swap with supportTeam]")
                #swap
                tool.clickSelectTeamAt(battlePosN)
                tool.click(airPortN, 0.5)
                tool.click((12, 76), 1.5, (1, 1))
            def subphase2():

                tool.clickSetSupportTeamStrategy(battlePosN,0)
                for i in range(2):
                    tool.log("[finish Turn]")
                    tool.clickFinishTurn(fastforward=True)
                    tool.log("[battle done]")
            def subphase3():
                tool.log("[battleClear]")
                entryImage = "imgs\\GF\\Common\\BattleEntry\\8-1N.png"
                normalStartImage = "imgs\\GF\\Common\\BattleEntry\\NormalStart.png"
                tool.battleResultClear(1)

                def succFunc():
                    if (None != tool.identifyAndFindPos(entryImage)):
                        return True
                    else:
                        return False

                tool.loopWait(succFunc, failWaitStep=0.5)
                pos0 = tool.identifyAndFindPos(entryImage)
                tool.click(pos0, 0.3)
                tool.loopWait(tool.asBattleNormalStart)
                pos1 = tool.identifyAndFindPos(normalStartImage)
                tool.click(pos1)
                tool.loopWaitRev(tool.asSkipable, None, tool.asBattleNormalStart, None)
            subphase1()
            subphase2()
            subphase3()
        def phase4_2():
            tool.clickBattle_Restart()
        def scriptLoop():
            phase1()
            phase2_refuelAndWithdraw()
            phase2_planModeExecuting()
            phase3()
            self.collectingPhase()
            if(useSupport):
                phase4_1()
            else:
                phase4_2()
            pass
        def initScript():
            '''phase1()
            phase2_refuelAndWithdraw()
            phase2_planModeExecuting()
            phase3()
            self.collectingPhase()
            if(useSupport):
                phase4_1()
            else:
                phase4_2()
            '''
            pass
        self._timerStart(initScript,scriptLoop,loopCount)
    def HS2000_14e(self,loopCount):
        tool = self.tool

        def phase1():
            #enterBattle
            tool.log("[phase1]")
            entryImage="imgs\\GF\\Common\\BattleEntry\\1-4e.png"
            normalStartImage="imgs\\GF\\Common\\BattleEntry\\NormalStart.png"
            tool.battleResultClear(1)
            tool.log("[battleResultCleared]")
            def succFunc():
                if(None!=tool.identifyAndFindPos(entryImage,0.8)):
                    return True
                else:
                    return False
            tool.loopWait(succFunc,failWaitStep=0.5)
            pos0=tool.identifyAndFindPos(entryImage,0.8)
            tool.click(pos0,0.3)
            tool.loopWait(tool.asBattleNormalStart)
            pos1=tool.identifyAndFindPos(normalStartImage)
            tool.click(pos1)
            tool.loopWaitRev(tool.asBattle_Init,None,tool.asBattleNormalStart,None)
            tool.log("[phase1 done]")
        def phase2():
            #deploy
            airPort=(22,44)
            tool.log("[phase2]")
            tool.loopWait(tool.asBattle_Init,loopMax=None)
            tool.clickOpenDeployPanel(airPort)
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init,None)
            tool.clickBattle_StartBattle()
            tool.log("[phase2 done]")
        def phase3_T1():
            pastPos=[(22,44),(39,46),(30,70)]
            tool.clickSelectTeamAt(pastPos[0])
            tool.clickOpenOperatePanel(pastPos[0])
            tool.clickBattle_TeamOperate_Refuel()
            tool.clickExecutePlanMode(pastPos,2)
            tool.clickFinishTurn(True)
        def phase3_T2():
            pastPos=[(30,50),(42,75),(63,51)]
            tool.clickSelectTeamAt(pastPos[0])
            tool.clickExecutePlanMode(pastPos, 2)
            tool.clickFinishTurn(True)
        def phase3_T3_1():
            route1=[(63,50),(42,74)]
            tool.clickOpenOperatePanel(route1[0])
            tool.clickBattle_TeamOperate_Refuel()
            tool.clickDirectBattle(route1[1])
        def phase3_T3_2():
            pastPos=[(63,27),(42,50),(47,25)]
            tool.clickOpenDeployPanel(pastPos[0])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_PlanMode,False)
            tool.clickSelectTeamAt(pastPos[1])
            tool.clickSwapWith(pastPos[0])
            tool.clickDirectBattle(pastPos[2])
            tool.clickFinishTurn(True)
        def phase3_T4():
            route1=[(47,50),(60,27),(73,38),(72,64),(63,82)]
            tool.clickExecutePlanMode(route1,4)
            tool.clickFinishTurn(True)
        def scriptLoop():
            phase1()
            phase2()
            phase3_T1()
            phase3_T2()
            phase3_T3_1()
            phase3_T3_2()
            self.collectingPhase()
            phase3_T4()
        def initScript():
            pass
        self._timerStart(initScript,scriptLoop,loopCount)
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
                for i in range(4):
                    tool.click(pastPos[i],0.5)
                tool.clickBattle_PlanMode_Start()
            tool.code3RecoverFunc=code3RecoverFunc
            tool.clickSelectTeamAt(pastPos[0])
            tool.clickBattle_PlanMode()
            for i in range(1,4):
                tool.click(pastPos[i],0.2)
                tool.loopWait(tool.asPlanStepLeft,4-i,failClickPos=pastPos[i])
            tool.clickBattle_PlanMode_Start()
            while(not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
            #tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None,failWaitStep=1)
            tool.code3RecoverFunc=None


            tool.clickSelectTeamAt(pastPos[3])
            tool.useFairySkill()
            while(tool.asBattle_PlanMode(False)):
                tool.click(pastPos[4],1)

            while (not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                tool.click((50,50),1)
            tool.log("[phase3 done]")
        def phase4():
            tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None,failWaitStep=1)
            tool.click((90,90),1)
            tool.battleResultClear()
        def scriptLoop():
            phase1()
            phase2()
            phase3()
            self.collectingPhase()
            phase4()
        def initScript():
            #phase4()
            pass
        self._timerStart(initScript,scriptLoop,loopCount)
    def M4_36(self,loopCount):
        tool = self.tool

        def phase1():
            # enterBattle
            tool.log("[phase1]")
            entryImage = "imgs\\GF\\Common\\BattleEntry\\3-6.png"
            normalStartImage = "imgs\\GF\\Common\\BattleEntry\\NormalStart.png"
            tool.battleResultClear(1)

            def succFunc():
                if (None != tool.identifyAndFindPos(entryImage)):
                    return True
                else:
                    tool.clickChooseDifficulty("N")
                    time.sleep(0.1)
                    tool.scrollDown()
                    time.sleep(0.5)
                    return False

            tool.scrollDown()
            tool.loopWait(succFunc, failWaitStep=0.5)
            pos0 = tool.identifyAndFindPos(entryImage)
            tool.click(pos0, 0.3)
            tool.loopWait(tool.asBattleNormalStart)
            pos1 = tool.identifyAndFindPos(normalStartImage)
            tool.click(pos1)
            tool.loopWaitRev(tool.asBattle_Init, None, tool.asBattleNormalStart, None)
            tool.log("[phase1 done]")

        def phase2():
            airPort = [(83, 32), (56,48)]
            tool.log("[phase2]")
            tool.loopWait(tool.asBattle_Init, loopMax=None)
            tool.clickOpenDeployPanel(airPort[0])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init, None)

            tool.clickOpenDeployPanel(airPort[1])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init, None)
            tool.clickBattle_StartBattle()
            tool.log("[phase2 done]")

        def phase3():
            pastPos = [(56,48), (44,50), (32,74), (30,98)]
            tool.log("[phase3]")
            tool.loopWait(tool.asBattle_PlanMode, False, loopMax=None)

            def code3RecoverFunc():
                for i in range(4):
                    tool.scrollUp()
                tool.clickBattle_PlanMode()
                for i in range(4):
                    tool.click(pastPos[i], 0.5)
                tool.clickBattle_PlanMode_Start()

            tool.code3RecoverFunc = code3RecoverFunc
            tool.clickSelectTeamAt(pastPos[0])
            tool.clickBattle_PlanMode()
            for i in range(1, 4):
                tool.click(pastPos[i], 0.2)
                tool.loopWait(tool.asPlanStepLeft, 5 - i, failClickPos=pastPos[i])
            tool.clickBattle_PlanMode_Start()
            while (not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
            # tool.loopWait(tool.asBattle_PlanMode,False,loopMax=None,failWaitStep=1)
            tool.code3RecoverFunc = None
            tool.log("[phase3 done]")
        def phase4():
            tool.log("[phase4]")
            pastPos=[(30,50),(41,62)]
            tool.clickSelectTeamAt(pastPos[0])
            tool.useFairySkill()
            tool.clickBattle_PlanMode()
            tool.click(pastPos[1],0.5)
            tool.loopWait(tool.asPlanStepLeft,1,failClickPos=pastPos[1])
            tool.clickBattle_PlanMode_Start()
            while (not tool.asBattle_PlanMode(False)):
                tool.identifyRescue()
                time.sleep(0.5)
            tool.log("[phase4 done]")
            pass
        def phase5():
            tool.loopWait(tool.asBattle_PlanMode, False, loopMax=None, failWaitStep=1)
            tool.click((90, 90), 1)
            tool.battleResultClear()

        def scriptLoop():
            phase1()
            phase2()
            phase3()
            phase4()
            phase5()

        def initScript():
            # phase4()
            pass

        self._timerStart(initScript, scriptLoop, loopCount)
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
                    tool.clickChooseDifficulty("N")
                    time.sleep(0.1)
                    tool.scrollDown()
                    time.sleep(0.5)
                    return False
            tool.scrollDown()
            tool.loopWait(assFunc=succFunc,failWaitStep=0.5)
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
            tool.clickSelectTeamAt(pastPos[0])
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
    def Any_46_fileCollecting(self,loopCount):
        tool=self.tool
        def phase_deploy():
            airPort = [(82, 66), (86, 22)]
            tool.log("[deploy]")
            tool.loopWait(tool.asBattle_Init, loopMax=None)
            tool.clickOpenDeployPanel(airPort[0])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init, None)

            for i in range(4):
                tool.scrollUp()
            tool.clickOpenDeployPanel(airPort[1])
            tool.clickBattle_Deploy_YesBtn(tool.asBattle_Init, None)
            tool.clickBattle_StartBattle(planMode=True)
            tool.log("[deploy done]")
        def phase_planMove():
            pastPos=[(86,22),(84.5,43),(77,64),(67,78),(78,83)]
            #tool.clickSelectTeamAt(pastPos[0])
            tool.clickExecutePlanMode(pastPos,4)
        def phase_planFinish():
            while(True):
                if(tool.asAmbushed()):
                    tool.log("[Ambushed]",31)
                    tool.click((50,50),0)
                    while not tool.asBattlePaused():
                        tool.log("[try pause]",32)
                        tool.click((50,2),0.1,randRange=(1,1))
                    tool.log("[try withdraw]",32)
                    tool.click((30,5),0.1,randRange=(1,1))
                    tool.loopWait(tool.asBattle_PlanMode,False,failClickPos=(30,5),failWaitStep=0.1)
                    break
                elif(tool.asBattle_PlanMode(False)):
                    tool.log("[succeed]",32)
                    break
                elif(tool.identifyAndFindPos("imgs\\GF\\Common\\Battle\\Event\\Tdoll.png")!=None):
                    time.sleep(0.5)
                    if (tool.identifyAndFindPos("imgs\\GF\\Common\\Battle\\Event\\Tdoll.png") != None):
                        time.sleep(0.5)
                        if (tool.identifyAndFindPos("imgs\\GF\\Common\\Battle\\Event\\Tdoll.png") != None):
                            time.sleep(0.5)
                            if (tool.identifyAndFindPos("imgs\\GF\\Common\\Battle\\Event\\Tdoll.png") != None):
                                time.sleep(0.5)
                                if (tool.identifyAndFindPos("imgs\\GF\\Common\\Battle\\Event\\Tdoll.png") != None):
                                    tool.click((50,50),0.5)
                                    tool.click((50,50),0.1)
            tool.log("[try restart]")
            tool.clickBattle_Restart()
        def scriptLoop():
            phase_deploy()
            phase_planMove()
            phase_planFinish()
        def initScript():
            #phase_planFinish()
            pass
        self._timerStart(initScript,scriptLoop,loopCount)
    def collectingPhase(self):
        tool=self.tool
        self.countDown+=1
        clock=2
        if(self.countDown%clock==(clock-1)):
            tool.log("[collecting...]",32)
            tool.quitToMainPanel()
            #self.enterFactoryToRetire(False)
            tool.returnToBattle()
            tool.log("[collect done]",32)
    def finishWaitRestart(self):
        tool=self.tool
        t=time.localtime()
        tool.log("%d:%d:%d"%(t.tm_hour,t.tm_min,t.tm_sec))
        tool.skipDlg()
        tool.quitToMainPanel()
        t=time.localtime()
        tool.log("%d:%d:%d"%(t.tm_hour,t.tm_min,t.tm_sec))
        while(True):
            time.sleep(300)
            t=time.localtime()
            tool.log("%d:%d:%d"%(t.tm_hour,t.tm_min,t.tm_sec))
            tool.mainPanelClear()



    def enterFactoryToStrengthen(self):
        pass
    def enterFactoryToRetire(self,retireAll=False):
        def switchToRetirePanel():
            self.tool.log("[switch to retire panel]")
            self.tool.enterFactory()
            self.tool.clickFactoryOption(3)
        def retire2StarAll():
            self.tool.loopWait(self.tool.asFactoryOption, assPara=3,finishWait=0.5)
            pos0=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png")
            self.tool.click(pos0,1.5)
            pos1 = self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png")
            self.tool.click(pos1,0.5)
            if (None != self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png")):
                self.tool.click((5, 5), 0.5)
            self.tool.loopWait(self.tool.asFactoryOption, assPara=3, failClickPos=pos1)
            while True:
                posTest=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png")
                self.tool.click(pos1)
                diff=((posTest[0]-pos0[0])**2+(posTest[1]-pos0[1])**2)
                if(diff<15):
                    break
                else:
                    print(diff)
        def retire2StarMG():
            self.tool.loopWait(self.tool.asFactoryOption,assPara=3,finishWait=0.5)
            self.tool.log("[enter selectPanel]")
            pos0 = self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png")
            self.tool.click(pos0, 1.5)
            while None==self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png"):
                pass
            self.tool.log("[at select panel]")
            pos1=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png")
            pos2=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\FilterBy_INIT.png")
            while pos2==None:
                pos2=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\FilterBy_INIT.png")

            self.tool.log("[select filter]")
            self.tool.click(pos2,0.5)
            self.tool.loopWait(self.tool.asFilterOpen,failClickPos=pos2,failWaitStep=0.5)
            self.tool.log("[filter MG]")
            pos3=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\Filter\\MG_1.png")
            self.tool.click(pos3,0.5)
            self.tool.loopWait(self.tool.asFilterState_MG,assPara=True,failClickPos=pos3)
            self.tool.identifyAndClick("imgs\\GF\\Common\\Factory\\3Retire\\FilterOPEN.png")
            self.tool.log("[auto select]")
            self.tool.click(pos1,0.5)
            if(None!=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png")):
                self.tool.click((5,5),0.5)
            self.tool.loopWait(self.tool.asFactoryOption,assPara=3,failClickPos=pos1)
            self.tool.log("[returned to factory option3]")
            while True:
                posTest=self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\selectTDoll.png")
                self.tool.click(pos1)
                diff=((posTest[0]-pos0[0])**2+(posTest[1]-pos0[1])**2)
                if(diff<15):
                    break
                else:
                    print(diff)
            self.tool.log("[retire done]")

            self.tool.identifyAndClick("imgs\\GF\\Common\\Factory\\selectTDoll.png")
            self.tool.click(pos3,0.5)
            self.tool.click(pos2,0.5)
            self.tool.identifyAndClick("imgs\\GF\\Common\\Factory\\3Retire\\FilterOPEN.png")
            self.tool.click((5,5),0.5)
            self.tool.loopWait(self.tool.asFactoryOption,assPara=3)
            pass
        def returnToMainPanel():
            while (None != self.tool.identifyAndFindPos("imgs\\GF\\Common\\Factory\\returnToBase.png")):
                self.tool.identifyAndClick("imgs\\GF\\Common\\Factory\\returnToBase.png")
            self.tool.mainPanelClear()
        switchToRetirePanel()
        if(retireAll):
            retire2StarAll()
        else:
            retire2StarMG()
        returnToMainPanel()


    def start(self,script,paraTuple):
        def startScript():
            for i in range(3):
                print("\a")
                time.sleep(0.5)
            script(self,paraTuple)
            self.tool.log("[All Finish]")
            time.sleep(2)
            for i in range(5):
                print("\a",end=" ")
                time.sleep(0.5)
        startScript()


if(__name__=="__main__"):
    mngr=GFSceneManager()
    #mngr.start(GFSceneManager.enterFactoryToRetire,False)
    #mngr.start(GFSceneManager.Zas_81n,(30,False))
    mngr.start(GFSceneManager.SOP_115,(40,0))
    #mngr.finishWaitRestart()+
    #mngr.start(GFSceneManager.Any_46_fileCollecting,300)