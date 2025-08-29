## **VL822 Info Update Tool**

一个用于修改VL822固件中部分Descriptor内容的工具，以达到设备自定义名称的目的。

<img width="400" height="439" alt="2c08074980ca5b3a7a11e470ba9103cf" src="https://github.com/user-attachments/assets/a7f49d16-8b75-4f99-96f4-e21b5b54d575" />

> [!CAUTION]
> 1. 仅测试VL822固件可用，Via Lab的其他HUB固件未测试，请勿使用。刷砖作者一概不负责。
> 2. 不同IC（Q5、Q7、Q8）之间不可也不能混刷。

## **工作原理：**
查找固件中的自定义值并替换。

## **使用方法：**

自定义固件重新生成后，点开根目录下的`VL822_firmware_upgrade_tool`：

<img width="242" height="99" alt="image" src="https://github.com/user-attachments/assets/f6a9197a-e59c-4131-aa97-c67f248fcec4" />

将新自定义固件拷贝到`VL822_firmware_upgrade_tool\Binfile`中：

<img width="239" height="116" alt="image" src="https://github.com/user-attachments/assets/70833b7b-5b9b-4db5-86cb-7d83a18df41f" />

`VL822_firmware_upgrade_tool`里面有一个文件`Setting.ini`，双击点开：

<img width="185" height="91" alt="image" src="https://github.com/user-attachments/assets/2ceceddf-e53d-40da-9cf2-f2280939f9d1" />

修改`[HUBModule]`下`NO.1HUBWantUpdateBinFile`的值为自定义固件名：

<img width="616" height="152" alt="image" src="https://github.com/user-attachments/assets/595377c2-48de-4dbd-bc54-2735cef2aad4" />

保存退出后回到`VL822_firmware_upgrade_tool`，双击`start.bat`执行自定义更新。

***

更新前：

<img width="742" height="583" alt="image" src="https://github.com/user-attachments/assets/92667c21-8c31-47da-b7d8-0cb9fb64610e" />

更新后：

<img width="740" height="589" alt="a3bf40c1c30293602dca5996b66d82ba" src="https://github.com/user-attachments/assets/cf2c8833-f43c-4a1c-88b0-921af4361988" />

**更新后最好拔插一下HUB，不然有概率会出现无法识别的USB设备，拔插一下即可解决。**
