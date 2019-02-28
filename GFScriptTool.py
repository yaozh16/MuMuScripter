#coding=utf-8
from ScriptTool import ScriptTool
import time
import os
import win32api
import random
class GFScriptTool(ScriptTool):
    def __init__(self):
        super(GFScriptTool,self).__init__()
        self.code3RecoverFunc=None
        self._temRecordImage="imgs\\GF\\Common\\tmp\\tmp.png"
        self._temRecordImage2="imgs\\GF\\Common\\tmp\\tmp2.png"
        if(None==self.setUp(u'少女前线 - MuMu模拟器')):
            self.recoverApp()
    def asEchelonFormationPanel(self):
        return None!=self.identifyAndFindPos(
            "imgs\\GF\\Common\\EchelonFormation\\EchelonFormationPanel_PresetBtn.png")
    def asEchelonFormationPresetPanel(self):
        return None != self.identifyAndFindPos("imgs\\GF\\Common\\EchelonFormation\\EchelonFormationPanel_PresetOptionBtn.png")
    def asEchelonFormationPresetOptions(self,selected=False):
        img1="imgs\\GF\\Common\\EchelonFormation\\EchelonFormationPresetOptions_SELECTED.png"
        img2="imgs\\GF\\Common\\EchelonFormation\\EchelonFormationPresetOptions_INIT.png"
        best=self.bestFit((0.78,0.80,0.98,0.96),[img1,img2])
        if(selected):
            return None!=self.identifyAndFindPos(img1) and \
                   img1==best[1]
        else:
            return None!=self.identifyAndFindPos(img2) and \
                   img2==best[1]
    def asBattle_Init(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\INIT.png")
    def asDeployPanel(self):
        return None != self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\deployFormationBtn.png")
    def asBattle_PlanMode(self,selected=False):
        if(selected):
            return None != self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\planMode_SELECTED.png")
        else:
            return None != self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\planMode_INIT.png")
    def asTeamSelected(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\fairyInstructionCancel.png") \
               or None!=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\fairyInstructionRelease1.png") \
               or None!=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\fairyInstructionRelease2.png")
    def asTeamOperatePanel(self):
        #已经部署的梯队的界面
        return (None != self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\withdrawBtn.png")) \
               and(None != self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\refuelBtn.png"))
    def asWithdrawPanel(self):
        #梯队撤退确认的界面
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\withdrawPanel.png",0.8)
    def asRestartPanel(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\restartBtn.png",0.8)
    def asSwapable(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\swapBtn.png")
    def asPlanStepLeft(self,stepLeft):
        imgPath="imgs\\GF\\Common\\Battle\\PlanStepLeft\\%02d.png"%(stepLeft)
        return None!=self.identifyAndFindPos(imgPath,0.95)
    def asBattleInfo(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\battleInfo.png")
    def asBattleResult(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\BattleEntry\\BattleResult.png")

    def asMainPanel(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\MainPanel\\battle.png")
    def asBattleEntryPanel(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\BattleEntry\\CombatMission.png")
    def asBattleNormalStart(self):
        return self.identifyAndFindPos("imgs\\GF\\Common\\BattleEntry\\NormalStart.png")
    def asFactory(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Factory\\factoryMarker.png")
    def asFactoryOption(self,index):
        path="imgs\\GF\\Common\\Factory\\Options\\"
        def saveTest():
            return self.assertCrop1((0,0.16,0.14,0.80),path+"%d.png"%(index))
        def loadTest():
            best=self.bestFitByDir((0,0.16,0.14,0.80),path)
            if(best==None):
                return False
            else:
                result=int(best[1].strip(".png"))
                return result==index

        #return saveTest()
        return loadTest()
    def asFilterOpen(self):
        return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\FilterOPEN.png")
    def asFilterState_MG(self,selected=False):
        if(selected):
            return None!=self.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\Filter\\MG_2.png")
        else:
            return None != self.identifyAndFindPos("imgs\\GF\\Common\\Factory\\3Retire\\Filter\\MG_1.png")


    def asRetireSelected(self,selected=True):
        if(not selected):
            return self.assertCrop1((0.86,0.84,0.98,0.96),"imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectBtn.png")
        else:
            return self.assertCrop1((0.86,0.84,0.98,0.96),"imgs\\GF\\Common\\Factory\\3Retire\\AutoSelectConfirmBtn.png")

    def scrollDown(self):
        scrollKeys=[ord(each) for each in "SDFGHJKL"]
        self.typeKey(scrollKeys[random.randint(0,len(scrollKeys)-1)],1)
    def scrollUp(self):
        scrollKeys=[ord(each) for each in "XCVBNM"]
        self.typeKey(scrollKeys[random.randint(0,len(scrollKeys)-1)],1)
    def recoverApp(self):
        self.log("Try Recover App...", 1)
        if (None == self.setUp(u'MuMu模拟器')):
            self.log("Try Open Simulator", 1)
            self.log("Fail", 1)
            exit(1)
        self.identifyAndClick("imgs\\GF\\Common\\icon.png")
        for i in range(100):
            if (None != self.identifyAndFindPos("imgs\\GF\\Common\\Error\\welcomeImage_1.png")):
                break
    def skipDlg(self):
        if self.identifyAndClick("imgs\\GF\\Common\\battle\\skipBtn.png"):
            time.sleep(0.5)
    def clickEchelonFormation_Finish(self):
        #编队结束
        self.loopWait(self.asEchelonFormationPanel,None,failWaitStep=0.4)
        self.click((5,5), 0)
        self.loopWait(self.asBattle_PlanMode,False ,finishWait=0.2,failClickPos=(5,5),failWaitStep=0.5)
    def clickEchelonFormation_Preset(self):
        #进入阵型预设
        self.loopWait(self.asEchelonFormationPanel)
        self.identifyAndClick("imgs\\GF\\Common\\EchelonFormation\\EchelonFormationPanel_PresetBtn.png")
        self.loopWait(self.asEchelonFormationPresetPanel)
    def clickEchelonFormation_Preset_Finish(self):
        #预设确定
        self.click((88, 86), 0)
        self.loopWaitRev(assFunc=self.asEchelonFormationPanel,assPara=None,
                         failFunc=self.asEchelonFormationPresetPanel,failPara=None,
                         finishWait=0,failWaitStep=1,failClickPos=(88,86))
    def clickEchelonFormation_Preset_Options_N(self,number):
        #选项界面
        self.click((98,40), 0)
        self.loopWait(self.asEchelonFormationPresetOptions,False,None,0)
        #选项N
        if(number==0):
            self.click((80,15),0)
        elif(number==1):
            self.click((80,30),0)
        self.loopWait(self.asEchelonFormationPresetOptions,True,None,0)
        self.click((90,89),0.5)
        #可能的强制替换
        '''选中强制替换'''
        self.click((44,58),0.5)
        '''确定'''
        self.click((64,69.5),0.5)
        self.loopWait(self.asEchelonFormationPresetPanel,None,None,0)

    def clickBattle_StartBattle(self):
        #开始
        self.click((88,86), 0)
        self.loopWait(self.asBattle_PlanMode,assPara=False ,finishWait=0,failWaitStep=1)
        pos0=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\battleInfo.png")
        pos1=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\planMode_INIT.png")
        self.log("started")
        while(pos0!=None):
            self.click((16,19),0.2)
            pos0=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\battleInfo.png")
        self.click(pos1,0)
        self.loopWait(self.asBattle_PlanMode,assPara=True,failClickPos=pos1)
        self.click(pos1,0)
        self.loopWait(self.asBattle_PlanMode,assPara=False,failClickPos=pos1)
        print("[Battle Started]free to operate")
    def clickBattle_PlanMode(self):
        #计划模式
        print("[planMode]")
        self.identifyAndClick("imgs\\GF\\Common\\Battle\\planMode_INIT.png")
        self.loopWaitRev(assFunc=self.asBattle_PlanMode, assPara=True,
                         failFunc=self.asBattle_PlanMode, failPara=False,
                         loopMax=100, finishWait=0, failClickPos=(10,79),failWaitStep=0.5)
        print("[planMode]entered")
    def clickBattle_PlanMode_Start(self):
        #计划模式
        self.loopWait(self.asBattle_PlanMode,assPara=True)
        self.click((88,86), 0)
        for i in range(40):
            if(self.asBattle_PlanMode(True)):
                self.click((88.86),0)
            else:
                break
        print("[planMode]executing")
    def clickBattle_TeamOperate_Refuel(self):
        self.loopWait(self.asTeamOperatePanel)
        self.identifyAndClick("imgs\\GF\\Common\\Battle\\refuelBtn.png")
        time.sleep(0.5)
        self.loopWait(self.asBattle_PlanMode,None)
    def clickBattle_TeamOperate_Withdraw(self):
        self.loopWait(self.asTeamOperatePanel)
        self.identifyAndClick("imgs\\GF\\Common\\Battle\\withdrawBtn.png")
        self.loopWait(self.asWithdrawPanel)
        self.identifyAndClick("imgs\\GF\\Common\\Battle\\withdrawConfirmBtn.png")
        time.sleep(0.5)
        self.loopWait(self.asBattle_PlanMode,None)

    def clickBattle_Deploy_YesBtn(self,assFunc,assPara):
        #部署
        self.click((92,90), 0)
        self.loopWait(assFunc,assPara)
    def clickBattle_Deploy_Formation(self):
        #队伍编成
        self.loopWait(self.asDeployPanel)
        self.click((19,86))
        self.loopWaitRev(assFunc=self.asEchelonFormationPanel,assPara=None,
                         failFunc=self.asDeployPanel,failPara=None,
                         failClickPos=(19,86))
        return

    def clickBattle_Restart(self):
        #重新开始
        self.identifyAndClick("imgs\\GF\\Common\\Battle\\stopBtn.png")
        self.loopWait(self.asRestartPanel,None,10,failClickPos=(25,6))
        self.identifyAndClick("imgs\\GF\\Common\\Battle\\restartBtn.png")
        for i in range(30):
            if(self.asRestartPanel()):
                self.click((38,68),0)
            elif(self.asBattle_Init()):
                break
            self.skipDlg()
            time.sleep(1)

        pass

    def swapWith(self, Pos):
        self.loopWait(self.asTeamSelected)
        self.loopWait(self.asSwapable,failClickPos=Pos,failWaitStep=0.5,finishWait=0.2)
        swapBtnPos=self.identifyAndFindPos("imgs\\GF\\Common\\Battle\\swapBtn.png")
        self.click(swapBtnPos,1.5)
    def selectTeamAt(self,pos):
        self.log("selectTeam",-1)
        self.click(pos,0.5)
        for i in range(10):
            if(self.asTeamSelected()):
                return
            elif(self.asDeployPanel()):
                self.click((93,90),0.5)
            else:
                self.click(pos,0.5)
        print("[error]")
        exit(1)
    def clickOpenOperatePanel(self,pos):
        self.click(pos,0.5)
        while(not self.asTeamOperatePanel()):
            if(self.asTeamSelected()):
                self.click(pos,0.5)
            time.sleep(0.4)
    def clickOpenDeployPanel(self,pos):
        self.click(pos, 0.5)
        while (not self.asDeployPanel()):
            self.click(pos, 0.5)

    def identifyRescue(self):
        commonPath="imgs\\GF\\Common\\"
        entryPath=commonPath+"BattleEntry\\"
        rescuePath=commonPath+"Battle\\Rescue\\"
        rect=(0.8,0.2,0.9,0.6)
        if(None!=self.identifyAndFindPos(entryPath + "Share.png")):
            self.log("identifying")
            ret=self.bestFitByDir(rect,rescuePath)
            if((None!=ret) and (None!=self.identifyAndFindPos(rescuePath+ret[1],0.95))):
                if(ret[1].startswith("2")):
                    self.log("General(2)",32)
                    time.sleep(0.5)
                elif (ret[1].startswith("3")):
                    self.log("Rare(3)",34)
                    time.sleep(0.5)
                elif (ret[1].startswith("4")):
                    self.log("SR(4)",32)
                    time.sleep(0.5)
                elif (ret[1].startswith("5")):
                    self.log("Legendary(5)",33)
                    self.click((50,50),0.5)
                    time.sleep(0.5)
            else:
                self.assertCrop1(rect,rescuePath+"UNKNOWN%d.png"%random.randint(0,100),display=False)

    def enterBattlePanel(self):
        commonPath="imgs\\GF\\Common\\"
        path=commonPath+"Error\\"
        while(True):
            if(self.asBattleEntryPanel()):
                time.sleep(0.2)
                if (self.asBattleEntryPanel()):
                    time.sleep(0.2)
                    if (self.asBattleEntryPanel()):
                        break
            elif (self.identifyAndFindPos(path + "supportFinish.png")):
                self.identifyAndClick(path + "supportFinish.png")
            elif (self.identifyAndFindPos(path + "supportRestart.png")):
                self.identifyAndClick(path + "yesBtn.png")
            elif (self.asMainPanel()):
                self.identifyAndClick("imgs\\GF\\Common\\MainPanel\\battle.png")
        pass
    def battleResultClear(self,stableSecond=2):
        commonPath="imgs\\GF\\Common\\"
        errPath=commonPath+"Error\\"
        entryPath=commonPath+"BattleEntry\\"
        while(True):
            if(self.asBattleResult()):
                self.click((50,50),0.5)
            elif (None!=self.identifyAndFindPos(entryPath + "Share.png")):
                self.identifyRescue()
                self.click((50,50),0.5)
            elif (None!=self.identifyAndFindPos(errPath + "supportFinish.png")):
                self.identifyAndClick(errPath + "supportFinish.png")
            elif (None!=self.identifyAndFindPos(errPath + "supportRestart.png")):
                self.identifyAndClick(errPath + "yesBtn.png")
            elif(self.asBattleEntryPanel()):
                time.sleep(stableSecond/3.0)
                if (self.asBattleEntryPanel()):
                    time.sleep(stableSecond/3.0)
                    if (self.asBattleEntryPanel()):
                        break
    def mainPanelClear(self):
        commonPath="imgs\\GF\\Common\\"
        path=commonPath+"Error\\"
        while (True):
            if (self.identifyAndFindPos(path + "accidentalLeft.png")):
                self.identifyAndClick(path + "closeBtn.png")
            elif (self.identifyAndFindPos(path + "supportFinish.png")):
                self.identifyAndClick(path + "supportFinish.png")
            elif (self.identifyAndFindPos(path + "supportRestart.png")):
                self.identifyAndClick(path + "yesBtn.png")
            elif (self.asMainPanel()):
                time.sleep(4)
                if (self.asMainPanel()):
                    break
    def errorTest(self):
        commonPath="imgs\\GF\\Common\\"
        path=commonPath+"Error\\"
        def phase1():
            if (None!=self.identifyAndFindPos(path + "illegalOperation.png")):
                self.log("[found illegalOperation]",1)
                #errorProcess
                self.identifyAndClick(path+"closeBtn.png")
                while(None==self.identifyAndFindPos(path+"welcomeImage_1.png")):
                    pass
            elif(None!=self.identifyAndFindPos(path+"code3Error.png")):
                self.log("[found code3 error]", 1)
                # errorProcess
                self.identifyAndClick(path + "closeBtn.png")
                while (None == self.identifyAndFindPos(path + "welcomeImage_1.png")):
                    pass
            elif(None!=self.identifyAndFindPos(path+"welcomeImage_1.png")):
                self.log("[found welcomePage]",1)
            else:
                return False
            #touch welcome panel
            while (self.identifyAndClick(path + "welcomeImage_1.png")):
                pass
            #login and return to main panel
            self.mainPanelClear()
            self.loopWait(self.asMainPanel)
            while(None==self.identifyAndFindPos(commonPath+"MainPanel\\petHouse.png")):
                self.click((1,50),0.5)
            self.identifyAndClick(commonPath+"MainPanel\\fighting.png")
            if(None!=self.code3RecoverFunc):
                self.code3RecoverFunc()
            else:
                print("\033[1;35mUNABLE to PROCESS\033[0m\n")
                time.sleep(1)
                exit(2)
        return phase1()







    def rectTest(self,rect):
        self.assertCrop1(rect,"test.png")
if(__name__=="__main__"):
    tool=GFScriptTool()
    def test1():
        im=tool.screenRecord()
        im=im.crop((0,0,10,10))
        fp=open("test.png","wb")
        im.save(fp)
        fp.close()

    def test3():
        tool.rectTest((0,0,1,1))
    def test4():
        print(tool.click((99,86),0.5))
    def test5():
        import random
        for i in range(10):
            print(random.randint(-2,2))
    def test6():
        pass
        for i in range(3):
            print(tool.scrollUp())
    def test7():
        battlePos = [(25, 35), (11, 41), (12, 67), (25, 51), (23, 73),(23,63),(10,76)]
        tool.click(battlePos[6],randRange=(1,1))
    def test8():
        commonPath="imgs\\GF\\Common\\"
        errPath=commonPath+"Error\\"
        entryPath=commonPath+"BattleEntry\\"
        print(tool.battleResultClear())
    def test9():
        tool.click((90,90))
        #tool.mainPanelClear()
        #tool.enterBattlePanel()
    test9()
    #test8()
    #test3()