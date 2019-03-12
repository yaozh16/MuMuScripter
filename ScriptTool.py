#coding=utf-8
import os
import numpy as np
import aircv as ac
import time
from PIL import Image,ImageDraw
import random
import win32gui
import win32ui
import win32con
import win32api
class ScriptTool:
    def __init__(self):
        def defaultErrorTest():
            pass
        self.errorTest=defaultErrorTest
        self._hwnd=0
        self._temRecordImage="screen.png"
        self._temRecordImage2="screen2.png"
        random.seed(time.time())
        self._offset=[0,36]


    def setUp(self,windowName):
        self._hwnd = win32gui.FindWindow(None, windowName)
        if(self._hwnd== 0):
            print("window not found!")
            return None

        self.printWindowStatus()
        win32api.SendMessage(self._hwnd,win32con.WM_ACTIVATE,None)
        return self._hwnd
    def printWindowStatus(self):
        if (self._hwnd == 0):
            print("window not found!")
            return None

            # 获取窗口位置
        left, top, right, bottom = win32gui.GetWindowRect(self._hwnd)
        # 获取某个句柄的类名和标题
        title = win32gui.GetWindowText(self._hwnd)
        clsname = win32gui.GetClassName(self._hwnd)
        print("[title]\033[1;32m%s\033[0m" % title)
        print("[class]\033[1;32m%s\033[0m" % clsname)
        print("[hwnd]\033[1;32m%d\033[0m" % self._hwnd)
        print("[position]\033[1;32m(%d,%d,%d,%d):[w]%d[h]%d\033[0m" % (
        left, top, right, bottom, right - left, bottom - top))
    def typeKey(self,KeyCode,timeWait=0.0,continuePrintKey=False):
        if(self._hwnd==0):
            return
        print("["+chr(KeyCode)+"]",end=' ')
        #win32gui.SetActiveWindow(self._hwnd)
        #win32api.SendMessage(self._hwnd,win32con.WM_ACTIVATE,None)
        win32api.SendMessage(self._hwnd, win32con.WM_KEYDOWN, KeyCode, 0)
        time.sleep(0.01)
        win32api.SendMessage(self._hwnd, win32con.WM_KEYUP, KeyCode, 0)
        while(timeWait>=1):
            if(continuePrintKey):
                win32api.SendMessage(self._hwnd, win32con.WM_KEYDOWN, KeyCode, 0)
                win32api.SendMessage(self._hwnd, win32con.WM_KEYUP, KeyCode, 0)
            print(timeWait,end=' ')
            time.sleep(1)
            timeWait-=1
        if(timeWait>0):
            time.sleep(timeWait)
        print(' ')
    def click(self,XY,timeWait=0.0,randRange=(3,2)):
        X,Y=XY[0]*0.01,XY[1]*0.01
        # 获取窗口位置
        left, top, right, bottom = win32gui.GetWindowRect(self._hwnd)
        #X=int(X*1280)
        X=int(X*(right-left+2))
        Y=int(Y*(bottom-top-35-35))
        X+=0
        Y+=30
        X+=random.randint(-randRange[0],randRange[0])
        Y+=random.randint(-randRange[1],randRange[1])

        pos = win32api.MAKELONG(X,Y)
        print("[click](%d,%d)"%(X, Y))

        win32gui.SendMessage(self._hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 1)
        time.sleep(0.001)
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONDOWN, win32con.VK_LBUTTON, pos)
        time.sleep(0.001)
        win32api.SendMessage(self._hwnd, win32con.WM_LBUTTONUP, None, pos)
        time.sleep(0.15)
        time.sleep(timeWait+random.randint(0,10)/1000.0)

    def log(self,msg,emergency=0):
        if(emergency==0):
            print("\033[1;30m%s\033[0m" % msg)
        elif(emergency==1):
            print("\033[1;31m%s\033[0m" % msg)
        elif(emergency>30):
            print("\033[1;%dm%s\033[0m" % (emergency,msg))
        else:
            print("%s" % msg)
    def screenRecord(self):
        def screenRecordToFile(hwnd,fileName):
            # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
            hwndDC = win32gui.GetWindowDC(hwnd)

            # 创建设备描述表
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)

            # 创建内存设备描述表
            saveDC = mfcDC.CreateCompatibleDC()

            # 创建位图对象
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, 1280, 720)
            saveDC.SelectObject(saveBitMap)

            # 截图至内存设备描述表
            img_dc = mfcDC
            mem_dc = saveDC
            #mem_dc.BitBlt((0, 0), (1280, 720), img_dc, (6, 46), win32con.SRCCOPY)
            mem_dc.BitBlt((0, 0), (1280, 720), img_dc, (0,36), win32con.SRCCOPY)

            # 将截图保存到文件中
            while(True):
                try:
                    saveBitMap.SaveBitmapFile(mem_dc, fileName)
                    break
                except Exception as e:
                    print(e)
                    pass

            # 内存释放
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
        def readImageFile(fileName):
            fp=open(fileName,"rb")
            img=Image.open(fp)
            img=img.crop((0,0,img.size[0],img.size[1]))
            fp.close()
            return img
        win32gui.SendMessage(self._hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, None)
        screenRecordToFile(self._hwnd, self._temRecordImage)
        img=readImageFile(self._temRecordImage)

        return img

    def loopWait(self, assFunc, assPara=None, loopMax=100, finishWait=0.0, failTypeKeyOrd=None, failClickPos=None, failWaitStep=0.2):
        def helperFunc():
            return True
        helperPara=None
        self.loopWaitRev(assFunc,assPara,helperFunc,helperPara,loopMax,finishWait,failTypeKeyOrd,failClickPos,failWaitStep)
    def loopWaitRev(self,assFunc,assPara=None,failFunc=None,failPara=None,loopMax=100, finishWait=0.0, failTypeKeyOrd=None, failClickPos=None, failWaitStep=0.2):

        def getRet(func, para):
            if (para != None):
                return func(para)
            else:
                return func()
        print("[wait]",end=" ")
        ret=getRet(assFunc,assPara)
        if (ret):
            pass
        else:
            def nowOK():
                time.sleep(failWaitStep)
                self.errorTest()
                ret=getRet(assFunc,assPara)
                if (ret):
                    return True
                else:
                    if (getRet(failFunc,failPara)):
                        if (failTypeKeyOrd != None):
                            self.typeKey(failTypeKeyOrd, failWaitStep)
                        if (failClickPos != None):
                            self.click(failClickPos, failWaitStep)
                    return False
            if(loopMax!=None):
                for i in range(loopMax):
                    ret=nowOK()
                    if(ret):
                        break
                    print(i,end=" ")
            else:
                #infinite loop
                i=0
                while(True):
                    ret = nowOK()
                    if (ret):
                        break
                    print(i, end=" ")
                    i+=1
        if (not ret):
            print("[fail]")
            for i in range(5):
                print("\a")
                time.sleep(0.5)
            exit(0)
        print("[finishWait]",end=" ")
        while(finishWait>failWaitStep):
            print("%.1f"%finishWait,end=" ")
            finishWait-=failWaitStep
            time.sleep(failWaitStep)
        if(finishWait>0):
            time.sleep(finishWait)
        print("[done]")

    def recordCrop(self,rect):
        self.assertCrop1(rect,self._temRecordImage,display=False)
    def recordCropChanged(self,rect):
        return not self.assertCrop2(rect,self._temRecordImage)
    def recordCropUnchanged(self,rect):
        self._temRecordImage="imgs\\Common\\tmp\\tmp.png"
        return self.assertCrop2(rect,self._temRecordImage)

    def identifyAndFindPos(self,expectImg,confidence=0.9):
        imobj = ac.imread(expectImg)
        self.assertCrop1((0, 0, 1, 1), self._temRecordImage2, display=False)
        imsrc = ac.imread(self._temRecordImage2)
        match_result = ac.find_template(imsrc, imobj, confidence)
        if (match_result != None):
            centerPoint = match_result["result"]
            clickPos = (centerPoint[0] * 100.0 / imsrc.shape[1], centerPoint[1] * 100.0 / imsrc.shape[0])
            return clickPos
        else:
            return None
    def identifyAndFindPosOriginal(self,imobjPath,imsrcPath,confidence=0.9):
        imobj = ac.imread(imobjPath)
        imsrc = ac.imread(imsrcPath)
        match_result = ac.find_template(imsrc, imobj, confidence)
        if (match_result != None):
            centerPoint = match_result["result"]
            clickPos = (centerPoint[0] * 100.0 / imsrc.shape[1], centerPoint[1] * 100.0 / imsrc.shape[0])
            return clickPos
        else:
            return None
    def identifyAndClick(self,expectImg,confidence=0.9):
        imobj = ac.imread(expectImg)
        self.screenRecord()
        imsrc = ac.imread(self._temRecordImage)
        match_result = ac.find_template(imsrc, imobj, confidence)

        if (match_result != None):
            centerPoint = match_result["result"]
            clickPos = (centerPoint[0] * 100.0 / imsrc.shape[1], centerPoint[1] * 100.0 / imsrc.shape[0])
            self.click(clickPos, 0.9)
            return True
        else:
            return False
    def bestFit(self,rect,files):
        screen = self.screenRecord()
        w, h = screen.size

        cropped = screen.crop((int(w * rect[0]), int(h * rect[1]), int(w * rect[2]), int(h * rect[3])))
        croppedList = np.array(cropped.histogram())
        best=None
        for each in files:
            fp = open(each, "rb")
            stdImage = Image.open(fp)
            cropped.resize((stdImage.size))
            stdList = np.array(stdImage.histogram())
            fp.close()
            diff = np.average(np.square(np.subtract(stdList, croppedList)))
            if(best==None or diff<best[0]):
                best=(diff,each)
        return best
    def bestFitByDir(self,rect,directory):
        screen = self.screenRecord()
        w, h = screen.size

        cropped = screen.crop((int(w * rect[0]), int(h * rect[1]), int(w * rect[2]), int(h * rect[3])))

        croppedList = np.array(cropped.histogram())
        best = None
        files=os.listdir(directory)
        for each in files:
            fp = open(os.path.join(directory,each), "rb")
            stdImage = Image.open(fp)
            cropped.resize((stdImage.size))
            stdList = np.array(stdImage.histogram())
            diff = np.average(np.square(np.subtract(stdList, croppedList)))
            if (best == None or diff < best[0]):
                best = (diff, each)
            fp.close()
        return best


    def assertCrop1(self, percentRect, expectImage, rgbThresh=(0, 0, 0), display=True):
        screen=self.screenRecord()
        w,h=screen.size
        if(rgbThresh!=(0, 0, 0)):
            pixels = screen.load()
            for y in range(h):
                for x in range(w):
                    r,g,b=pixels[x,y]
                    if(r<rgbThresh[0] or g<rgbThresh[1] or b<rgbThresh[2]):
                        pixels[x, y] = (0, 0, 0)
        cropped=screen.crop((int(w*percentRect[0]),int(h*percentRect[1]),int(w*percentRect[2]),int(h*percentRect[3])))
        fp=open(expectImage,"wb")
        cropped.save(fp)
        fp.close()
        if(display):
            drawObject = ImageDraw.Draw(screen)

            #drawObject.rectangle((int(w*percentRect[0]),int(h*percentRect[1]),int(w*percentRect[2]),int(h*percentRect[3])), fill="red", outline=1)
            for p in range(1, 51):
                xP = p / 50.0
                drawObject.line([w * xP, 0, w * xP, h], fill="pink", width=1)
            for p in range(1, 51):
                yP = p / 50.0
                drawObject.line([0, h * yP, w, h * yP], fill="pink", width=1)

            for p in range(1, 11):
                xP = p / 10.0
                drawObject.line([w * xP, 0, w * xP, h], fill="red", width=2)
            for p in range(1, 11):
                yP = p / 10.0
                drawObject.line([0, h * yP, w, h * yP], fill="red", width=2)
            #screen.show()
            x1, y1, x2, y2 = (
                int(w * percentRect[0]), int(h * percentRect[1]), int(w * percentRect[2]), int(h * percentRect[3]))
            drawObject.line((x1, y1, x2, y1), fill="green", width=3)
            drawObject.line((x2, y1, x2, y2), fill="green", width=3)
            drawObject.line((x1, y2, x2, y2), fill="green", width=3)
            drawObject.line((x1, y1, x1, y2), fill="green", width=3)
            screen.show()
    def assertCrop2(self, percentRect,expectImage, rgbThresh=(0, 0, 0)):
        screen=self.screenRecord()
        w,h=screen.size
        if (rgbThresh != (0, 0, 0)):
            pixels = screen.load()
            for y in range(h):
                for x in range(w):
                    r, g, b = pixels[x, y]
                    if (r < rgbThresh[0] or g < rgbThresh[1] or b < rgbThresh[2]):
                        pixels[x, y] = (0, 0, 0)
        cropped=screen.crop((int(w*percentRect[0]),int(h*percentRect[1]),int(w*percentRect[2]),int(h*percentRect[3])))

        fp=open(expectImage,"rb")
        stdImage=Image.open(fp)
        cropped.resize((stdImage.size))
        stdList=np.array(stdImage.histogram())
        croppedList=np.array(cropped.resize(stdImage.size).histogram())
        fp.close()
        diff=np.average(np.square(np.subtract(stdList,croppedList)))
        #print("(%f)"%diff,end=" ")
        return diff<1


    def gameTab(self,index):
        if(index==0):
            self.click((28,-1),0.2)
        elif(index==1):
            self.click((40,-1),0.2)
if __name__=="__main__":
    tool=ScriptTool()
    #tool.setUp(u'BlueStacks App Player')
    #tool.setUp(u'少女前线 - MuMu模拟器')
    tool.setUp(u'命运-冠位指定 - MuMu模拟器')

    img=tool.screenRecord()
    #tool.click((40,-1),0)
    tool.click((28,-1),0)
    tool.printWindowStatus()
    #tool.click((40,50),0.4)
    #tool.click((50,50),0.5)