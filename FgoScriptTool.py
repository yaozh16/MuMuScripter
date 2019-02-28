#coding=utf-8
import time
from ScriptTool import ScriptTool
import aircv as ac
import os
from PIL import Image
class FgoScriptTool(ScriptTool):
    def __init__(self):
        super(FgoScriptTool,self).__init__()
        self._temRecordImage="imgs\\FGO\\Common\\tmp\\tmp.png"
        self._temRecordImage2="imgs\\FGO\\Common\\tmp\\tmp2.png"
    def waitReady(self,finishWait=0.5):
        self.loopWait(assFunc=self.asBattleReady, loopMax=None, finishWait=finishWait)
    def serventSkill(self, serventIndex, skillIndex,applyTo=None):
        self.waitReady()
        P=serventIndex*25+5+(skillIndex)*7.5
        p=P/100.0
        L1=0.02
        L2=0.03
        clickPos=(P,80)
        window=(p-L1, 0.8-L2, p+L1, 0.8+L2)
        self.recordCrop(window)
        self.click(clickPos,0.5)
        if(applyTo!=None):
            self.click((25+25*applyTo,60),0.5)

        self.loopWaitRev(assFunc=self.recordCropChanged,assPara=window,
                         failFunc=self.recordCropUnchanged,failPara=window,
                         loopMax=10,failClickPos=clickPos,failWaitStep=0.2)
        self.waitReady(0.8)
    def masterSkill(self, skillIndex, swapIndexs=None):
        self.waitReady()
        self.click((92,45),0.8)
        clickPos=(70+8*skillIndex,45)
        self.click(clickPos,0.5)
        if(swapIndexs!=None):
            #swap skill
            self.loopWait(self.asSwapPanel,assPara=False,loopMax=100,finishWait=0.1)
            self.click((swapIndexs[0]*15+12.5,50),0.2)
            self.click((swapIndexs[1]*15+12.5,50),0.2)
            self.loopWait(self.asSwapPanel,assPara=True,loopMax=100,finishWait=0.1)
            self.click((50,88),1)
        self.waitReady()
    def startAttack(self):
        window = (0.83,0.89,0.96,0.94)
        clickPos=(90,85)
        self.loopWait(self.asBattleReady,assPara=None,loopMax=100)
        self.recordCrop(window)
        self.click(clickPos, 0)
        self.loopWaitRev(assFunc=self.recordCropChanged, assPara=window,
                         failFunc=self.recordCropUnchanged, failPara=window,
                         loopMax=10, failClickPos=clickPos, failWaitStep=0.2)
        time.sleep(1.7)
    def clickActionCardByIndex(self, index):
        P = index * 20 +10
        p = P / 100.0
        L1 = 0.06
        L2 = 0.10
        window=(p-L1, 0.7-L2, p+L1, 0.7+L2)
        #self.rectTest(window)
        clickPos = (P, 70)
        self.click(clickPos,0.6)
    def clickCardByRank(self,rank,path):
        print("clickCard By rank...",end=" ")
        for each in rank:
            fileName=os.path.join(path,each+".png")
            if(self.identifyAndClick(fileName,0.8)):
                time.sleep(0.5)
                print("succeed ")
                return True
        print("fail ")
        return False
    def clickNPcard(self,index):
        P=index*17.5+32.5
        p = P / 100.0
        L1 = 0.06
        L2 = 0.10
        window = (p - L1, 0.3 - L2, p + L1, 0.3 + L2)
        #self.rectTest(window)
        self.click((index*20+30,30),0.8)
        pass
    def eatApple(self,type="G"):
        imgPath="imgs\\FGO\\Common\\Apple_"
        self.loopWait(self.asAPRecoverPanel,assPara=None,loopMax=None)
        if(type=="G"):
            self.identifyAndClick(imgPath+"G.png")
            self.loopWait(self.asAPRecoverConfirmPanel,assPara=None,loopMax=None,failWaitStep=1)
            self.click((65,80),0.5)
            self.loopWait(self.asSupportPanel,assPara=None,loopMax=None,failClickPos=(65,80),failWaitStep=1)
            pass
        elif(type=="S"):
            self.identifyAndClick(imgPath + "S.png")
            self.loopWait(self.asAPRecoverConfirmPanel, assPara=None, loopMax=None, failClickPos=(50, 45),
                          failWaitStep=1)
            self.click((65, 80), 0.5)
            self.loopWait(self.asSupportPanel, assPara=None, loopMax=None, failWaitStep=1)
            pass
        else:
            self.click((79,75),0.5)
            self.identifyAndClick(imgPath + "B.png")
            self.loopWait(self.asAPRecoverConfirmPanel, assPara=None, loopMax=None, failClickPos=(50, 45),
                          failWaitStep=1)
            self.click((65, 80), 0.5)
            self.loopWait(self.asSupportPanel, assPara=None, loopMax=None, failWaitStep=1)
            pass
    def selectGoodSupporter(self, expectImg, confidence=0.9):
        self.loopWait(self.asSupportPanel,assPara=None,loopMax=20)
        supportPage=0
        while(True):
            time.sleep(0.5)
            if(self.asPreparePanel()):
                break
            elif(not self.identifyAndClick(expectImg,confidence)):
                supportPage=self.switchSupporters(supportPage)
    def switchSupporters(self,count=0):
        if(count==7):
            self.click((65,18),1)
            self.click((60,78),1)
        else:
            self.click((97,30+12*count),0.5)
        return (count+1)%8
    def currentBattle(self, TurnImagePath):
        self.waitReady(finishWait=0)
        L=os.listdir(TurnImagePath)
        result= self.bestFit((0.675,0.02,0.690,0.06),[os.path.join(TurnImagePath,each) for each in L])
        return int([each.strip(".png") for each in L if os.path.join(TurnImagePath,each)==result[1]][0])
    def switchEnemy(self,index):
        self.waitReady()
        clickPos=(2+20*index,5)
        self.click(clickPos,0.5)
        self.waitReady()

    def asMainPanel(self):
        return self.assertCrop2((0.88,0.02,0.97,0.09),expectImage="imgs\\FGO\\Common\\MainPanel.png")
    def asSupportPanel(self):
        #助战
        return self.assertCrop2((0.62, 0.15, 0.68, 0.21), "imgs\\FGO\\Common\\SupportPanel.png")
    def asSupportUpdatePanel(self):
        #助战
        return self.assertCrop2((0.30, 0.30, 0.70, 0.60), "imgs\\FGO\\Common\\SupportUpdatePanel.png")
    def asPreparePanel(self):
        return self.assertCrop2((0.87,0.90,0.99,0.99),"imgs\\FGO\\Common\\PreparePanel.png")
    def asBattleReady(self):
        #可以行动
        return None!=self.identifyAndFindPos("imgs\\FGO\\Common\\BattleReady.png")
    def asSwapPanel(self,selected):
        if(not selected):
            return None!=self.identifyAndFindPos("imgs\\FGO\\Common\\SwapPanel_unselected.png")
        else:
            return None!=self.identifyAndFindPos("imgs\\FGO\\Common\\SwapPanel_selected.png")
    def asBattleResultPanel(self):
        #战役胜利界面
        return None!=self.identifyAndFindPos("imgs\\FGO\\Common\\BattleResult.png")
        #return self.assertCrop1((0.40,0.40,0.6,0.6),"imgs\\FGO\\Common\\BattleResult.png")
    def asAPRecoverPanel(self):
        return None!=self.identifyAndFindPos("imgs\\FGO\\Common\\Apple_S.png")
    def asAPRecoverConfirmPanel(self):
        return None!=self.identifyAndFindPos("imgs\\FGO\\Common\\APRecoverConfirmPanel.png")
    def asPoolEmpty(self):
        return self.assertCrop2((0.63,0.32,0.68,0.36),"imgs\\FGO\\Common\\PoolEmpty.png")

    def asStrengthenPanel(self):
        return self.assertCrop2((0.40, 0.88, 0.53, 0.99), "imgs\\FGO\\Common\\StrengthenPanel.png")
    def asStrengthenConfirmPanel(self):
        return self.assertCrop2((0.20, 0.78, 0.80, 0.90), "imgs\\FGO\\Common\\StrengthenConfirmPanel.png")
    def rectTest(self,rect):
        self.assertCrop1(rect,"test.png")


if __name__ == "__main__":
    tool=FgoScriptTool()
    tool.setUp(u'命运-冠位指定 - MuMu模拟器')
    #print(tool.click((95,95),0))
    #print(tool.asAPRecoverConfirmPanel())
    #tool.click((10, 90), 0.1)
    #tool.rectTest((0.48,0.48,0.52,0.52))
    #print(tool.asBattleResultPanel())

