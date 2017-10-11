# mzphp2_decrypt

近期在研究某源码时碰到文件经过mzphp加密，于是自己写了个解密脚本，要解密的拿去。

接受issue和request，但现在我正在找工作，可能没有太多时间处理BUG或者增加功能，欢迎添砖加瓦。

### 使用方法：

`python3 mzphp_decrypt.py mzphp_encrypted.php` 

结果将直接输出到控制台，或

`python3 mzphp_decrypt.py mzphp_encrypted.php mzphp_decrypted.php` 

结果将输出到文件 `mzphp_decrypted.php` 中。



### 解码前后效果对比：

![image](https://user-images.githubusercontent.com/15062548/31435093-05b3012a-aeb1-11e7-84e0-f0a75db0de00.png)

![image](https://user-images.githubusercontent.com/15062548/31444674-744842b2-aecf-11e7-816b-13c87afac4e6.png)



云路花十块钱解码出来的结果：

![image](https://user-images.githubusercontent.com/15062548/31435103-16f23e92-aeb1-11e7-88f4-524ef23d9907.png)

可见，解密结果除了大括号换行问题之外其他基本一致。




​:copyleft: Copyleft(Ɔ) 2017-2099