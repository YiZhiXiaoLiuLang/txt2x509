# txt2x509
txt转为x509（CA证书），用于在可以打开原生设置的学习机上看小说。

# 原理

ca证书中包含c，st，l，cn，o，ou。

原生安卓只显示CN,O,OU，其中CN最大64，而ou没有长度限制。

故我们可以自己定义颁发者，使用者生成证书来实现

<img width="1418" height="818" alt="屏幕截图 2025-07-24 132712" src="https://github.com/user-attachments/assets/b1354a4c-9057-489d-9974-f858b91e71ee" />
<img width="1421" height="780" alt="屏幕截图 2025-07-24 132702" src="https://github.com/user-attachments/assets/e0aed391-900e-48b4-bbee-ac4fb650a0c4" />
<img width="1424" height="799" alt="屏幕截图 2025-07-24 132648" src="https://github.com/user-attachments/assets/2fac19ab-e8ed-4d63-a049-f4e12592c4c0" />



# How To Use
## js版-在线使用（基于<a href="https://github.com/sometiny/x509js">x509js</a>）
示例：<a href="https://yzxll.icu/txt2x509/">https://yzxll.icu/txt2x509/</a>

或下载v1.html后打开

## python3版
```bash
pip3 install cryptography
python3 v1.py
```


