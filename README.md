# Smart Routing

同一套规则，分别生成 Clash Verge / Mihomo 和 iOS 小火箭配置。AI 使用专线；Cloudflare 相关域名直连；普通网站按社区规则分流。仓库不保存节点、密码或机场订阅。

## 更新地址

- 小火箭配置：https://raw.githubusercontent.com/zzz7491/smart-routing/main/shadowrocket.conf
- Clash 配置模板：https://raw.githubusercontent.com/zzz7491/smart-routing/main/clash.template.yaml
- AI 规则：https://raw.githubusercontent.com/zzz7491/smart-routing/main/rules/ai.yaml
- Cloudflare 规则：https://raw.githubusercontent.com/zzz7491/smart-routing/main/rules/cloudflare.yaml

## Clash Verge

公开模板不含节点，AI / Normal 初始为 REJECT，不能直接当作节点订阅。首次把模板中的 rule-providers 和 rules 接入自己的本地配置，并将 AI / Normal 关联本地节点。AI 只关联已验证可用的专线，不加入 DIRECT 或普通组。Unmatched 默认走 Normal，可自行切 DIRECT。

已有私有本地完整配置的用户使用本地远程规则版本，节点保留本地。三个自定义规则集每 86400 秒更新，也可以在客户端手动刷新。修改策略组或规则顺序需更新配置；更新节点订阅不等于更新规则。

## 小火箭

先保留已导入节点，确保存在准确命名为 DMIT-HY2 的可用节点；从上述 conf 地址添加远程配置并启用，AI 组选 DMIT-HY2，Normal 使用当前 PROXY 节点。全局路由选择“配置”。修改规则后刷新远程规则集，配置结构有变化则更新远程配置。不要把 Clash YAML 当作小火箭配置导入。

## 维护

编辑 policy.json，再执行：

```sh
python3 build.py https://raw.githubusercontent.com/zzz7491/smart-routing/main
```

提交生成后的配置和 rules。两端刷新即可获取规则变化。无定时工作流；普通网站列表由客户端直接更新上游。

## 分流顺序

AI 专属域名 → Cloudflare 相关域名直连 → 显式直连 → 国内域名直连 → 普通代理列表 → 中国 IP 直连 → Unmatched。

未知网站默认走常规代理，延续原文件语义。Cloudflare IP 段为共享 CDN，不设全段直连。workers.dev / pages.dev 当前直连，具体托管网站若不可达需按域名添加例外。通用 auth0、支付、统计和共享 ASN 不归入 AI；域名规则无法区分同一个共享域名来自哪个页面。

## 登录排查与验证限制

旧配置已经将 cloudflare.com 设为 DIRECT，故主站实际走代理需要检查实际配置、全局模式或覆写。旧版缺少部分关联域名，登录子请求可能命中代理兜底。关闭代理后登录正常只是线索，具体原因仍需失败请求的域名、命中规则和最终出口。

本地 Clash 完整配置经本机 Mihomo 离线解析检查；12 个域名优先级与边界样例通过。检查没有验证远程下载、节点出口、DNS、Cloudflare 登录或小火箭实机运行。AI 节点延迟正常不代表服务接受其出口。

## 参考

- https://github.com/blackmatrix7/ios_rule_script （普通 Proxy / ChinaMax 规则）
- https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Clash/Cloudflare/Cloudflare.list
- https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/OpenAI/OpenAI.list
- https://wiki.metacubex.one/config/rules/
- https://wiki.metacubex.one/en/config/rule-providers/
