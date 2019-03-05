#coding=utf-8
import math




def speedTable():
    def c(s):
        t=math.ceil(30.0*50/s)
        return t

    f=None
    for i in range(20,121):
        if(c(i)!=f):
            if(f!=None):
                print("%d[%.2fs]"%(i-1,c(i-1)/30.0))
            f=c(i)
            print("[%d] %d -"%(f,i),end=" ")
    print("%d[%.2fs]" % (120, c(120) / 30.0))
if __name__=="__main__":
    speedTable()
