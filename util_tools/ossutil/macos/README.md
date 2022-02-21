1. 下载并安装ossutil

```shell
curl -o ossutilmac64 https://gosspublic.alicdn.com/ossutil/1.7.9/ossutilmac64
sudo mv ossutilmac64 /usr/local/bin
sudo chown ${USER}:admin /usr/local/bin/ossutilmac64
sudo chmod 755 /usr/local/bin/ossutilmac64
```

2. 生成默认配置文件

```shell
ossutilmac64 config
```
