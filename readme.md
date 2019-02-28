# MuMuScripter

>针对MuMu模拟器的脚本产生器

## 说明：

* ScriptTool:基础类，封装点击、按键和识别等基本功能

* FGOScriptTool\GFScriptTool:继承ScriptTool，针对特定游戏的特定操作添加了一些操作，比如FGOScriptTool里面根据截图选满破助战（如果没有找到会自动刷新助战继续查找）

	* 目前只针对FGO和GF写了几个脚本辅助函数
	
	* asXXX一般表示assertAtXXX，一般和loopWait和loopWaitRev合用达到状态同步
	
* SceneManager:利用FGOScriptTool\GFScriptTool，写了各种针对特定战斗场景脚本，例如FGO无限池终本，GF刷核心\炸狗等

* __重要__:如果需要使用identifyAndFindPos和identifyAndClick等识图函数，需要自己控制截图和MuMu模拟器的分辨率相同！目前已经有一部分截图，如果不想重新截图，MuMu请调整到1280x720的分辨率并不要修改窗口大小
