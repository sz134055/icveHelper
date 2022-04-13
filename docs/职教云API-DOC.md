# 职教云 

## 登陆

### Request

##### **API**

`https://zjyapp.icve.com.cn/newMobileAPI/MobileLogin/newSignIn`

##### Method

POST

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | \*/*                                                         |
| **emit**        | 1623135043000                                                |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |
| Content-Type    | application/x-www-form-urlencoded; charset=utf-8             |
| Content-Length  | 192                                                          |
| Referer         | https://file.icve.com.cn/                                    |
| Connection      | keep-alive                                                   |
| **User-Agent**  | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.5.0) Alamofire/4.7.3 |
| **device**      | 2420027c58efd5cd40a523564f2049bb                             |
| **Cookie**      |                                                              |

其中比较重要的是：

- emit：时间戳，以Python为例：

  ```python
  >>> import time
  >>> time.time()
  1623856807.311572
  >>> print(str(int(time.time()))+'000')
  1623857059000
  ```

  可以发现Python中`time.time()`函数可以生成整数位10位的时间戳，而Header中的emit参数据观察便知是 10位时间戳+000组成，因此可以使用上述例子的方法生成实时的emit

- User-Agent：针对Android和 iOS设备，有以下两种Agent：

  - Android：`okhttp/4.5.0`
  - iOS：`yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.5.0) `
    - iOS版本需要与后form表单中保持一致
    - yktIcve/2.8.43指出了职教云的版本，后面com.xx...（包名）和build可能随着版本的变更而变动

- device：该参数值是动态的，使用md5加密（**32位小写结果**），涉及到设备名，设备系统版本号，职教云版本号，emit。加密过程为，加密第一个值，将结果与后一个值相加（字符串拼接）作为新的值，随后重复前面步骤，直到最后一个值被相加后再次加密得出device值，过程类似如下：

  ```
  A , B , C
  md5(A)+B = 1
  md5(1)+C = 2
  device = md5(2)
  ```

- cookie：无需任何值，直接留空传递，登陆成功后会返回 Set-Cookie

##### Params

None

##### Form

| Key                     | Value                            |
| ----------------------- | -------------------------------- |
| **appVersion**          | 2.8.43                           |
| **clientId**            | 71c35ecb7baf4e16aea5eaca06312d3f |
| **equipmentApiVersion** | 14.6                             |
| **equipmentAppVersion** | 2.8.43                           |
| **equipmentModel**      | iPhone 11                        |
| sourceType              | 3                                |
| **userName**            | 12345678                         |
| **userPwd**             | 12345678                         |

说明：

- appVersion：即职教云App的版本号
- clientId：暂时未知该参数的含义，其用来指定设备的唯一，实测使用md5（32位小写）加密随机生成的UUID后可以登陆
  - 2021-8-16：测试任意字符串仍可以登陆成功
- equipmentApiVersion：即设备的系统版本号
- equipmentAppVersion：即职教云的版本号
- equipmentModel：即设备名称
- userName：职教云账号（明文）
- userPwd：职教云密码（明文）

### Response

#### 成功

##### Code

200

##### Header

| Key            | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Cache-Control  | no-cache                                                     |
| Content-Type   | text/html; charset=utf-8                                     |
| Date           | Tue, 08 Jun 2021 06:51:09 GMT                                |
| Expires        | -1                                                           |
| Pragma         | no-cache                                                     |
| **Set-Cookie** | acw_tc=2f624a3116211150441331459e111b934f7f8f7ee82880d4a0632f42ac145c;path=/;HttpOnly;Max-Age=1800 |
| **Set-Cookie** | auth=0102AACA4FCC492AD908FEAADAFB9D9D2AD908101639006D101C006C006101650079006D006B006F0078006600340071007000660072006500390069007200770000012F00FF73BE02DB8803994F3D8F8A43EDE328DAFDF5BE07; domain=.icve.com.cn; expires=Tue, 08-Jun-2021 16:51:09 GMT; path=/; HttpOnly; SameSite=Lax |
| X-Powered-By   | TXTEK                                                        |
| X-Upstream     | 0-3                                                          |
| Content-Length | 473                                                          |
| Connection     | keep-alive                                                   |

说明；

- Set-Cookie（第一个）：其中`Max-Age=1800`似乎指明该Cookie的有效时长只有半小时，后续将会有API提供更换过期Cookie

- Set-Cookie（第二个）：后续操作的每一次请求都需包含当中的`auth`值，即`Cookie = auth=0102XXXX...XXE07;`形式，第一个Set-Cookie将会被再次返回

##### Json

```json
{
	"code": 1,
	"userType": 1,
	"token": "9mllaeymxoxf4qpxox9irw",
	"userName": "2020123456",
	"secondUserName": "",
	"userId": "9mllaeymxoxf4qpxox9irw",
	"newToken": "@04bf86c94de9404c8001c592712a3e2b",
	"displayName": "XX",
	"employeeNumber": "2020123456",
	"url": "https://zjy2.icve.com.cn/common/images/default_avatar.jpg",
	"schoolName": "安徽XX学院",
	"schoolId": "abcdef-n7jlmggzr0-kxxx",
	"isValid": 1,
	"isNeedMergeUserName": 0,
	"isZjyUser": 1,
	"isGameUser": 0,
	"isNeedUpdatePwd": 0,
	"pwdMsg": ""
}
```

说明：

- token：似乎已经被废弃，其值等于下面的`userId`
- userId：个人的ID，唯一
- newToken：重要的值，后续请求的表单中需要包含，有时效性，过期后通过特定API更换
- displayName：个人的姓名
- employeeNumber：个人的学工号
- url：个人头像地址
- schoolName：学校名称
- schoolId：学校ID

其它值作用暂时未知，欢迎补充

#### 失败

##### Code

200

##### Header

| Key            | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Cache-Control  | no-cache                                                     |
| Content-Type   | text/html; charset=utf-8                                     |
| Date           | Tue, 08 Jun 2021 06:50:44 GMT                                |
| Expires        | -1                                                           |
| Pragma         | no-cache                                                     |
| **Set-Cookie** | acw_tc=2f624a3116211150441331459e111b934f7f8f7ee82880d4a0632f42ac145c;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                                        |
| X-Upstream     | 0-168                                                        |
| Content-Length | 41                                                           |
| Connection     | keep-alive                                                   |

说明：

- Set-Cookie：参展成功的Header说明

##### Json

```json
{
	"code": -1,
	"msg": "用户密码错误！"
}
```

- 经过测试，登陆超时（emit和生成device的emit不一致或间隔太大导致）时，`code`值依然为`-1`，因此基本可以断定登陆失败时，返回json信息中`code`的值为`-1`

  

**几乎后续的操作，失败时都如此返回，`code`为`-1`，后面将不再赘述**



## 保存登陆记录

### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/MobileLogin/saveUserLog`

##### Method

POST

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Content-Type    | application/x-www-form-urlencoded; charset=utf-8             |
| Content-Length  | 318                                                          |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=010...[中间省略]...E07;                                 |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.5.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

None

##### Form

| Key                 | Value                                        |
| ------------------- | -------------------------------------------- |
| api_version         | 14.5                                         |
| **appVersion**      | 2.8.43-71c35ecb7baf4e16aea5eaca06312d3f-14.5 |
| app_version         | 2.8.43                                       |
| clientId            | 71c35ecb7baf4e16aea5eaca06312d3f             |
| equipmentApiVersion | 14.5                                         |
| equipmentAppVersion | 2.8.43                                       |
| equipmentModel      | iPhone 11                                    |
| model               | iPhone 11                                    |
| **newToken**        | @04bf86c94de9404c8001c592712a3e2b            |
| sourceType          | 3                                            |
| **userId**          | 9mllaeymxoxf4qpxox9irw                       |

说明：

- appVersion：观察该值很容易得知，其形式为：`[app版本号]-[clientId]-[系统版本号]`

- newToken：登陆后拿到的`newToken`值
- userId：个人ID

### Response

#### 成功

##### Code

200

##### Header

| Cache-Control  | no-cache                                                |
| -------------- | ------------------------------------------------------- |
| Content-Type   | text/html; charset=utf-8                                |
| Date           | Tue, 08 Jun 2021 06:51:09 GMT                           |
| Expires        | -1                                                      |
| Pragma         | no-cache                                                |
| **Set-Cookie** | acw_tc=2f...[中间省略]..ae;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                                   |
| X-Upstream     | 0-13                                                    |
| Content-Length | 34                                                      |
| Connection     | keep-alive                                              |

##### Json

```json
{
	"code": 1,
	"msg": "保存成功！"
}
```

## 更换过期的Token

### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/MobileLogin/getNewSignInToken`

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Accept          | /                                                            |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Connection      | Keep-alive                                                   |
| Cookie          |                                                              |
| Host            | zjyapp.icve.com.cn                                           |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 15.0.0) Alamofire/4.7.3 |
| **device**      | 4a52babe00cb02887c93418341251510                             |
| **emit**        | 1646405017000                                                |

##### Params

| Key                 | Value                            | 说明   |
| ------------------- | -------------------------------- | ------ |
| clientId            | 71c35ecb7baf4e16aea5eaca06312d3f |        |
| equipmentApiVersion | 15.0                             |        |
| equipmentAppVersion | 2.8.43                           |        |
| equipmentModel      | iPhone 11                        |        |
| sourceType          | 3                                |        |
| userId              | 9mllae\*\*\*\*\*\*e9irw          | 账号ID |
| userName            | 2020123456                       | 账号   |
| userPwd             | ABC123456                        | 密码   |

### Response

##### Header

| Key            | Value                                                        |
| -------------- | ------------------------------------------------------------ |
| Cache-Control  | no-cache                                                     |
| Content-Length | 124                                                          |
| Content-Type   | text/html; charset=utf-8                                     |
| Date           | Fri, 04 Mar 2022 14:43:37 GMT                                |
| Expires        | -1                                                           |
| Pragma         | no-cache                                                     |
| Set-Cookie     | acw_tc=707c9fcb1646\*\*\*\*\*30f0afee7;path=/;HttpOnly;Max-Age=1800; auth=0102FBB9BF5\*\*\*\*\*D90801163900066000FFA9F3F0D780202DB31702182D12ABDC29524EBD04; domain=.icve.com.cn; expires=Sat, 05-Mar-2022 00:43:37 GMT; path=/; HttpOnly; SameSite=Lax |
| X-Powered-By   | TXTEK                                                        |
| X-Upstream     | 0-7                                                          |

##### JSON

```json
{
  "code": 1,
  "msg": "获取成功！",
  "userType": 1,
  "newToken": "@a860c423745456789f56b57e7e2e4399",
  "employeeNumber": "2020123456"
}
```



## 获取版本更新情况

### Request

##### API

iOS：`https://zjyapp.icve.com.cn/newMobileAPI/appversion/getIOSAppVersion`

Android：待补充

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=01...[中间省略]...07;                                   |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.5.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                     | Value     |
| ----------------------- | --------- |
| **equipmentApiVersion** | 14.5      |
| **equipmentAppVersion** | 2.8.43    |
| **equipmentModel**      | iPhone 11 |
| sourceType              | 3         |
| **versionCode**         | 2.8.43    |

##### Form

None

### Response

#### 有新版本时

*请求时一定要构建好参数，以下便是无参数直接访问API时获得的结果（macOS，Safari浏览器），获取到的是上一版本更新，并非最新版本*

##### Code

200

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 |
| Cookie          | acw_tc=2f624a3b16238603508947800e144e2eb7b8fccc49737d8023cee7a3a33d8e |
| User-Agent      | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15 |
| Accept-Language | zh-cn                                                        |
| Accept-Encoding | gzip, deflate, br                                            |
| Connection      | keep-alive                                                   |

##### Json

```json
{
	"code": 1,
	"msg": "获得最新版本成功！",
	"data": {
		"appVersionInfo": {
			"versionCode": "2.8.42",
			"isForce": true,
			"patchMessage": "1、教师新增年终报告;2、修复了一些不可爱的bug"
		}
	}
}
```

#### 无新版本时

##### Code

200

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=01...[中间省略]...E07;                                  |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.5.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Json

```json
{
	"code": -1,
	"msg": "暂无最新版本！",
	"data": {}
}
```

## 消息

*请求头与响应头忽略*

### 获取消息

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/News/getUserNewsList`

##### Method

GET

##### Params

实际测试仅需以下参数

| Key      | Value                     | 备注                                           |
| -------- | ------------------------- | ---------------------------------------------- |
| newToken | @d1df\*\*\*\*\*e52f94aaee | Token                                          |
| pageNum  | 1                         | 页数，用来获取更多的消息                       |
| userId   | 9mlla\*\*\*\*\*9irw       | 用户ID                                         |
| userType | 1                         | 用户类别，可能用于指示用户是否为学生还是老师等 |

#### Response

##### Code

200

##### Json

```json
{
	"code": 1,
	"newList": [{
		"Id": "gbcfaests5bbkgwf5akopq",
		"courseOpenId": "kvueaowsytpztlgxscx8q",
		"openClassId": "zfpzaoasfrfdcsyg5hxneq",
		"HwOrExamId": "3taeaestmijjrwna3ijw",
		"HwOrExamTermTimeId": "c7cfaest4j5lww8lsffsqa",
		"Content": "在班级:XX2021中，您有一个新的作业，时间为2021-06-11 09:40:00——2021-06-16 08:00:00",
		"Datecreated": "2021-06-11 09:41:24",
		"IsRead": 1,
		"NewsType": 1,
		"UserType": "1",
		"HwOrExamTitle": "p129  XXXX",
		"HwOrExamZtway": 3
	}, 
  #省略
  {
		"Id": "b8dxaksmldhsatwbbr4g",
		"courseOpenId": "jn9iay2rfllmpvvypwldmg",
		"openClassId": "9qcjavsrk1iv3aqa4ii6a",
		"HwOrExamId": "4ixakspj5ni8svktvdbq",
		"HwOrExamTermTimeId": "rxaksekjijlodwn1n7w",
		"Content": "在班级:XX2021中，您有一个新的考试，时间为2021-01-14 09:00:00——2021-01-14 11:00:00",
		"Datecreated": "2021-01-13 13:05:31",
		"IsRead": 1,
		"NewsType": 2,
		"UserType": "1",
		"HwOrExamTitle": "XXXX20-21-1",
		"HwOrExamZtway": 2
	}],
	"allowPage": 4
}
```

说明：

- Id：消息的ID
- courseOpenId：消息所属课程ID
- openClassId：课程开课班级ID
- HwOrExamId：消息对应的作业/考试ID
- HwOrExamTermTimeId：未知
- Content：消息内容
- Datecreated：创建日期？
- IsRead：是否已经阅读，`0`为未读，`1`为已读
- NewsType：消息类别，暂时未知类别对应码
- UserType：用户类别
- HwOrExamTitle：消息对应的作业/考试标题
- HwOrExamZtway：消息对应的作业/考试方式，如题库，暂未知晓不同方式说对应的值
- allowPage：消息列表的最大页数，对应请求参数中的`pageNum`值。但即使`pageNum`大于`allowPage`服务器仍然会正常响应，并返回空的列表

### 设置消息状态为已读

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/News/setNewsIsReadById`

##### Method

POST

##### Params

实测仅需以下参数

| Key        | Value                            | 备注   |
| ---------- | -------------------------------- | ------ |
| Id         | hrm7adqtjl5gazeecrw0na           | 消息ID |
| newToken   | @d1dfa26d1\*\*\*\*\*\*e52f94aaee | Token  |
| sourceType | 3                                | 默认   |

#### Response

##### Code

200

##### Json

```json
{
	"code": 1,
	"msg": "设置成功！"
}
```

### 设置所有信息为已读

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/News/setAllNewsIsRead`

##### Method

POST

##### Form

实测仅需以下参数

| Key        | Value                         | 备注   |
| ---------- | ----------------------------- | ------ |
| newToken   | @d1dfa26d\*\*\*\*\*\*2f94aaee | Token  |
| sourceType | 3                             | 默认   |
| userId     | hrm7a\*\*\*\*\*\*0na          | 用户ID |

#### Response

##### Code

200

##### Json

```json
{
	"code": 1,
	"msg": "设置成功！"
}
```

### 删除指定消息

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/News/deletedNewsByIds`

##### Method

POST

##### Form

| Key        | Value                        | 备注                                 |
| ---------- | ---------------------------- | ------------------------------------ |
| newToken   | @d1dfa26\*\*\*\*\*\*2f94aaee | Token                                |
| sourceType | 3                            | 默认                                 |
| Ids[]      | hrm7adqtjl5gazeecrw0na       | 指定删除的消息ID，可以存在多个，如下 |
| Ids[]      | stmdarmtobjekbiqxcj9zq       |                                      |

#### Response

##### Code

200

##### Json

```json
{
	"code": 1,
	"msg": "删除成功！"
}
```



## 我的学习

### 获取用户所有在修课程（Course）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/AppVersion/getProjectList`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=01......07;                                             |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.5.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                     | Value     |
| ----------------------- | --------- |
| **equipmentApiVersion** | 14.5      |
| **equipmentAppVersion** | 2.8.43    |
| **equipmentModel**      | iPhone 11 |
| isPass                  | 0         |
| **newToken**            | @04.....b |
| page                    | 1         |
| sourceType              | 3         |
| **stuId**               | 9.....w   |

说明：

- 实际测试，前三参数可有可无

- isPass：该值无需变动，暂时未知作用，欢迎补充

- stuId：即登陆后返回的Json中`userId`的值

- page：用于实现翻页，一次只会返回10个结果，所以对于大于10个课程，需要构建page实现翻页，当翻页预估获取数大于实际结果时（如3页预估获取30结果，实际只有19个课程），最后一个请求将会返回空结果，如下所示：

  ```json
  {
  	"code": 1,
  	"dataList": []
  }
  ```


##### Form

None

#### Response

##### Code

200

##### Header

| Cache-Control     | no-cache                                       |
| ----------------- | ---------------------------------------------- |
| Content-Type      | text/html; charset=utf-8                       |
| Date              | Tue, 08 Jun 2021 06:51:10 GMT                  |
| Expires           | -1                                             |
| Pragma            | no-cache                                       |
| Set-Cookie        | acw_tc=70......dd;path=/;HttpOnly;Max-Age=1800 |
| Vary              | Accept-Encoding                                |
| X-Powered-By      | TXTEK                                          |
| X-Upstream        | 0-173                                          |
| Transfer-Encoding | chunked                                        |
| Connection        | keep-alive                                     |

##### Json

```json
{
	"code": 1,
	"dataList": [{
		"Id": "6v...aq",
		"courseOpenId": "kv...8q",
		"courseName": "XX英语",
		"courseCode": "",
		"thumbnail": "https://file.icve.com.cn/ssykt/868/675/D9...F2.png?x-oss-process=image/resize,m_fixed,w_220,h_180,limit_0/format,jpg",
		"openClassName": "检验2021",
		"openClassId": "zf...eq",
		"openClassCode": "",
		"mainTeacherName": "XXX",
		"mainTeacherNum": "121212",
		"assistTeacherName": "XXX",
		"assistTeacherNum": "121212",
		"process": 0,
		"totalScore": -1.0,
		"InviteCode": "22abcd",
		"courseSystemType": 0
	},
    ...[中间省略]...
	, {
		"Id": "c3...fa",
		"courseOpenId": "t9....fa",
		"courseName": "大学英语1",
		"courseCode": "",
		"thumbnail": "https://file.icve.com.cn/ssykt/868/675/D...F2.png?x-oss-process=image/resize,m_fixed,w_220,h_180,limit_0/format,jpg",
		"openClassName": "XXXX班",
		"openClassId": "hb...ha",
		"openClassCode": "",
		"mainTeacherName": "XX",
		"mainTeacherNum": "123456",
		"assistTeacherName": "xx",
		"assistTeacherNum": "123456",
		"process": 100,
		"totalScore": -1.0,
		"InviteCode": "123abc",
		"courseSystemType": 0
	}]
}
```

说明（dataList）：

- Id：未知
- **courseOpenId**：开课ID
- **courseName**：课程名称
- courseCode：未知

- **thumbnail**：用于在职教云首页显示的课程封面图地址
- **openClassName**：开课班级名称
- **openClassId**：开课班级ID
- openClassCode：未知
- **mainTeacherName**：主教师姓名（可以开成开课人）
- mainTeacherNum：教师编号（可以看成教职员工号）
- **assistTeacherName**：教师姓名（可以看成实际上课教师，大部分情况下和`mainTeacher`同一个人）
- assistTeacherNum：同上

- process：课程学习进度（实际为课件学习进度，若无课件则永远为0）
- totalScore：课程总得分，`-1`表明当前课程为设置计分比例，无法得出总分
- InviteCode：课程邀请码
- courseSystemType：未知

### 关于课程的班级二维码

通过手机扫码可得到以下结果（文本）：

```json
{
  "openClassId":"EXAMPLE",
  "inviteCode":"123abc"
}
```

所以想要生成班级二维码仅需构建以上文本即可，可以利用在线的免费API（如在线二维码生成器，推荐）或自己利用库构建，甚至生成自己喜欢的样式

### 今日课堂（CourseOpen）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/FaceTeach/getStuFaceTeachList`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | \*/*                                                         |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=0102....5;                                              |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value      |
| ------------------- | ---------- |
| **courseOpenId**    |            |
| equipmentApiVersion | 14.6       |
| equipmentAppVersion | 2.8.43     |
| equipmentModel      | iPhone 11  |
| **faceDate**        | 2021-06-17 |
| **newToken**        | @92d...33b |
| **openClassId**     |            |
| sourceType          | 3          |
| **stuId**           | 9ml...irw  |

说明：

- courseOpenId：课程ID
- openClassId：开课班级ID
- faceDate：查询某日期的开课列表

##### Form

None

#### Response

##### Code

200

##### Header

| Key            | Value                                         |
| -------------- | --------------------------------------------- |
| Cache-Control  | no-cache                                      |
| Content-Type   | text/html; charset=utf-8                      |
| Date           | Thu, 17 Jun 2021 14:14:54 GMT                 |
| Expires        | -1                                            |
| Pragma         | no-cache                                      |
| Set-Cookie     | acw_tc=70....dd6;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                         |
| X-Upstream     | 0-214                                         |
| Content-Length | 364                                           |
| Connection     | keep-alive                                    |

##### Json

```json
{
	"code": 1,
	"msg": "请求成功！",
	"dataList": [{
		"Id": "pqu...hva",
		"courseOpenId": "9ke...zwa",
		"courseName": "XX化学",
		"className": "XX2022",
		"Title": "2021-06-17周四的课堂教学",
		"openClassId": "5la...aa",
		"dateCreated": "2021-06-17 10:11",
		"teachDate": "2021-06-17",
		"classSection": "34~",
		"Address": "实验室",
		"state": 2
	}, {
		"Id": "qlf...jea",
		"courseOpenId": "0cw...iw",
		"courseName": "XXX",
		"className": "XX1234、XX1537",
		"Title": "2021-06-17周四的课堂教学",
		"openClassId": "goy...iuw",
		"dateCreated": "2021-06-17 07:28",
		"teachDate": "2021-06-17",
		"classSection": "1—2",
		"Address": "教A601",
		"state": 2
	}]
}
```

说明请参照 所有开课 列表的说明

### 某一课程的今日课堂（CourseOpen）

#### Request

该API与 今日所有开课 API相同，唯一不同的是，这次请求需要对应的`courseOpenId`和`openClassId`

#### Response

与上相同

## 课件

### 说明

根据职业云APP，课件页内容结构如下所示：

```
Module
|-Topic
	|-Cell
Module
...
```

暂时以章节、单元、课件来分别代表`Module`、`Topic`和`Cell`

例如：

```
Unit1 The first lesson
|- How to learn Python
	|- Hello World.ppt
...
```

### 获取某一课程的所有章节（Module）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/AssistTeacher/getModuleListByClassId`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=01....AF;                                               |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value                             |
| ------------------- | --------------------------------- |
| **courseOpenId**    | 5hnawgroyfj9zgmemcc1g             |
| equipmentApiVersion | 14.6                              |
| equipmentAppVersion | 2.8.43                            |
| equipmentModel      | iPhone 11                         |
| **newToken**        | @92da25c6118d4c1dbf4a8f5dd6e4033b |
| **openClassId**     | 9xuzaoasa4varbkhmmtfg             |
| sourceType          | 3                                 |
| **stuId**           | 9mllaeymkoxf4qpfre9irw            |

##### Form

None

#### Response

##### Code

200

##### Header

| Key            | Value                                         |
| -------------- | --------------------------------------------- |
| Cache-Control  | no-cache                                      |
| Content-Type   | text/html; charset=utf-8                      |
| Date           | Thu, 17 Jun 2021 09:02:48 GMT                 |
| Expires        | -1                                            |
| Pragma         | no-cache                                      |
| **Set-Cookie** | acw_tc=70.....fd;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                         |
| X-Upstream     | 0-7                                           |
| Content-Length | 690                                           |
| Connection     | keep-alive                                    |

##### Json

```json
{
	"code": 1,
	"moduleList": [{
		"moduleId": "yarvaagrwlrhaa60ir41w",
		"isFirstModule": 1,
		"moduleName": "Unit 1 Symbols of culture",
		"sortOrder": 0
	}, 
		....	
   {
		"moduleId": "hnhxaaurjrfizyrmaae4fg",
		"isFirstModule": 0,
		"moduleName": "Unit 6 Dreams",
		"sortOrder": 5
	}],
	"msg": "获取成功！"
}
```

说明：

- **moduleId**：章节ID
- isFirstMoudle：是否是第一个章节
- moduleName：章节标题
- sortOrder：排序序号，从0开始

**注意：**有些课程可能存在无课件的情况，这种情况下`moduleList`的值为空

### 获取某一个章节下的所有小单元（Topic）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/AssistTeacher/getTopicListByModuleId`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=01.....AF;                                              |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value                 |
| ------------------- | --------------------- |
| **courseOpenId**    | 5h...1g               |
| equipmentApiVersion | 14.6                  |
| equipmentAppVersion | 2.8.43                |
| equipmentModel      | iPhone 11             |
| **moduleId**        | ya....1w              |
| **newToken**        | @92...3b              |
| **openClassId**     | 9xuzaoasa4varbkhmmtfg |
| sourceType          | 3                     |

说明：

- **moduleId**：即上一操作获取到“章节ID”

##### Form

None

#### Response

##### Code

200

##### Header

| Key            | Value                                       |
| -------------- | ------------------------------------------- |
| Cache-Control  | no-cache                                    |
| Content-Type   | text/html; charset=utf-8                    |
| Date           | Thu, 17 Jun 2021 09:02:50 GMT               |
| Expires        | -1                                          |
| Pragma         | no-cache                                    |
| Set-Cookie     | acw_tc=2f...f5;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                       |
| X-Upstream     | 0-174                                       |
| Content-Length | 522                                         |
| Connection     | keep-alive                                  |

##### Json

```json
]{
	"code": 1,
	"topicList": [{
		"topicId": "yj...iw",
		"topicName": "Around the Topic",
		"sortOrder": 0,
		"upTopicId": "0"
	}, 
        ....
  {
		"topicId": "it...ca",
		"topicName": "Section B Background knowledge",
		"sortOrder": 3,
		"upTopicId": "4h....tw"
	}],
	"msg": "获取成功！"
}
```

说明：

- **topicId**：单元ID
- topicName：单元标题
- sortOrder：排序序号
- upTopicId：上一单元ID，如若已是首位，则该值为`"0"`

### 获取某一单元下所有课件列表（Cell）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/AssistTeacher/getCellListByTopicId`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=01...AF;                                                |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value     |
| ------------------- | --------- |
| **courseOpenId**    | 5h...1g   |
| equipmentApiVersion | 14.6      |
| equipmentAppVersion | 2.8.43    |
| equipmentModel      | iPhone 11 |
| **newToken**        | @92...3b  |
| **openClassId**     | 9x...fg   |
| sourceType          | 3         |
| **stuId**           | 9m...rw   |
| **topicId**         | yj...iw   |

说明：

- topicId：即上一操作获取到的“单元ID”

##### Form

None

#### Response

##### Code

200

##### Header

| Key            | Value                                       |
| -------------- | ------------------------------------------- |
| Cache-Control  | no-cache                                    |
| Content-Type   | text/html; charset=utf-8                    |
| Date           | Thu, 17 Jun 2021 09:02:51 GMT               |
| Expires        | -1                                          |
| Pragma         | no-cache                                    |
| **Set-Cookie** | acw_tc=70...0f;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                       |
| X-Upstream     | 0-7                                         |
| Content-Length | 1010                                        |
| Connection     | keep-alive                                  |

##### Json

```json
{
	"code": 1,
	"msg": "获取成功！",
	"cellList": [{
		"topicId": "yj....iw",
		"cellId": "pvtpagkruqlhnysi7ehttq",
		"upCellId": "0",
		"cellType": 1,
		"sortOrder": 0,
		"cellName": "U1",
		"cellContent": null,
		"categoryName": "ppt",
		"externalLinkUrl": "",
		"extension": "其他",
		"isAllowDownLoad": true,
		"cellChildNodeList": [],
		"isStuSeeCell": 1,
		"studyCellPercent": 100.0
	}, 
     ...
  {
		"topicId": "yj...iw",
		"cellId": "u1qgaworb5dav7xoa22h6a",
		"upCellId": "zggbaworlzrmlmyumoczq",
		"cellType": 1,
		"sortOrder": 2,
		"cellName": "Activity3-4",
		"cellContent": null,
		"categoryName": "音频",
		"externalLinkUrl": "",
		"extension": "其他",
		"isAllowDownLoad": false,
		"cellChildNodeList": [],
		"isStuSeeCell": 1,
		"studyCellPercent": 100.0
	}]
}
```

说明：

- topicId：所属单元ID

- **cellId**：课件ID
- upCellId：上一课件ID，如若本身已是首位则值为`"0"`
- cellType：未知该值变化规律
- sortOrder：排序序号
- cellName：课件标题
- cellContent：未知作用
- categoryName：课件种类。现在已知有以下值：
  - ppt：PPT课件
  - 文档：文档课件（基本可以视为另一种类型的PPT或视其为PDF）
  - 图片：图片课件，同上
  - 音频：MP3播放课件
  - 视频：视频播放课件
- externalLinkUrl：未知作用
- extension：未知作用
- isAllowDownLoad：是否允许下载，布尔型
- cellChildNodeList：根据名称直译估测为课件附加内容，暂时未遇到相关情况，未知
- isStuSeeCell：根据名称直译估测为课件隐藏开关，值`1`为不隐藏
- **studyCellPercent**：学习进度，值范围：0.0~100.0

### 请求课件（Cell）

- 

### 更新课件的学习情况（未完全实现）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/Student/newStuProcessCellLog`

##### Method

POST

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Content-Type    | application/x-www-form-urlencoded; charset=utf-8             |
| Content-Length  | 490                                                          |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| Cookie          | auth=01.....8AF;                                             |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |

##### Params

None

##### Form

| Key                  | Value                            |
| -------------------- | -------------------------------- |
| **answerTime**       | 1623929862451.751                |
| **cellId**           | yei4adoqhbljzlz2lm2za            |
| **cellLogId**        | n3jdauqtby9ffxxbpwajnq           |
| **courseOpenId**     | 0cwuadoqtlngktdqkchpiw           |
| equipmentApiVersion  | 14.6                             |
| equipmentAppVersion  | 2.8.43                           |
| equipmentModel       | iPhone 11                        |
| **maxPicNum**        | 0                                |
| **maxStudyCellTime** | 1                                |
| **newToken**         | @92da....b                       |
| **openClassId**      | go....uw                         |
| **picNum**           | 0                                |
| **secretKey**        | 8093EB04B223372E6D985564AB40872C |
| sourceType           | 3                                |
| **stuId**            | 9mllaeymkoxf4qpfre9irw           |
| **studyCellTime**    | 5                                |
| **studyNewlyPicNum** | 0                                |
| **studyNewlyTime**   | 1                                |

说明：

- answerTime：时间戳，据观察判断为16位（毫秒单位）时间戳小数点向后位移三位

- cellId：课件ID

- cellLogId：注意，该值可以为空，以上一步请求课件的返回为准

- maxPicNum：课件学习最大页数，基本和下`studyNewlyTime`保持一致或略大于即可

- maxStudyCellTime：课件学习最大时间（位置），同上

- studyCellTime：学习总时长

- studyNewlyPicNum：课件学习页数

- studyNewlyTime：课件学习时间（位置）

- **secreKey**：该值尚未被知晓如何产生，但是经过实验发现，**该值可以被重复使用**（短时间内，仅限同一文件，并不稳定）

  

#### Response

##### Code



##### Header



##### Json



### 请求课件的评论（回复）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/BBS/getCellBBSList`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| Cookie          | auth=01....AF;                                               |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value                  |
| ------------------- | ---------------------- |
| activeType          | 1                      |
| **cellId**          | yei4adoqpk1nkt8lwur1lg |
| **courseOpenId**    | 0cw....piw             |
| equipmentApiVersion | 14.6                   |
| equipmentAppVersion | 2.8.43                 |
| equipmentModel      | iPhone 11              |
| **newToken**        | @92d....33b            |
| **openClassId**     | go....uw               |
| **page**            | 1                      |
| **pageSize**        | 20                     |
| sourceType          | 3                      |
| **userId**          | 9m....irw              |

说明：

- activityType：未知
- cellId：课件ID
- courseOpenId：课程ID
- openClassId：开课班级ID
- page：请求的页数
- pageSize：返回评价列表长度，如上20代表一次性返回20个评论信息，建议保持20
- userId：用户ID

##### Form

None

#### Response

##### Code

200

##### Header

| Key               | Value                                          |
| ----------------- | ---------------------------------------------- |
| Cache-Control     | no-cache                                       |
| Content-Type      | text/html; charset=utf-8                       |
| Date              | Thu, 17 Jun 2021 11:00:17 GMT                  |
| Expires           | -1                                             |
| Pragma            | no-cache                                       |
| Set-Cookie        | acw_tc=2f6...cf48;path=/;HttpOnly;Max-Age=1800 |
| Vary              | Accept-Encoding                                |
| X-Powered-By      | TXTEK                                          |
| X-Upstream        | 0-168                                          |
| Transfer-Encoding | chunked                                        |
| Connection        | keep-alive                                     |

##### Json

```json
{
	"code": 1,
	"isMainTeacher": 0,
	"uploadUrl": "https://upload.icve.com.cn/?space=ssykt&time=637595532170118594&bucket=icve&token=D98019068B43E08CA61461B6D6F19432",
	"previewUrl": "",
	"list": [{
		"Id": "lt6qaowscq5ffuupdyusfg",
		"dateCreated": "2021-03-08 08:47:27",
		"userId": "og...ybw",
		"displayName": "刘XX",
		"avatorUrl": "https://zjy2.icve.com.cn/common/images/default_avatar.jpg",
		"content": "好",
		"star": 5.0,
		"isAccept": 0,
		"docJson": [],
		"isPowerDelete": 0,
		"replyCount": 0
	},
       ....
  {
		"Id": "hwglaowsikxkvi0m94yy5q",
		"dateCreated": "2021-03-08 08:27:28",
		"userId": "kwp...kg",
		"displayName": "李XX",
		"avatorUrl": "https://zjy2.icve.com.cn/common/images/default_avatar.jpg",
		"content": "好",
		"star": 5.0,
		"isAccept": 0,
		"docJson": [],
		"isPowerDelete": 0,
		"replyCount": 0
	}],
	"pagination": {
		"totalCount": 70,
		"pageSize": 20,
		"pageIndex": 4
	}
}
```

说明：

- isMainTeacher：根据名称估测用于判断是否为主教师提供的课件，无使用价值
- uploadUrl：未知
- previewUrl：未知
- **Id**：可以视为该评论ID
- dateCreated：评论提交日期
- userId：评论提交者ID
- displayName：评论提交者姓名
- avatorUrl：评论提交者头像地址
- **content**：评论内容
- **star**：评星，值范围：0.0~5.0
- isAccept：未知
- docJson：未知，可能是附件相关，欢迎补充
- isPowerDelete：未知
- replyCount：回复下他人的评论数
- **totalCount**：评论总数
- pageSize：评论列表长度
- pageIndex：当前请求的页面数

#### 关于获取到完整的评论列表

##### 方法一

由于返回的评论列表长度`pageSize`默认值为`20`（未尝试过其他值，自行尝试，后果自负），初次请求后将会得到评论总数`totalCount`，根据评论总数即可推断应请求的总页数值，如`totalCount`的值为`70`时，`page`参数的取值范围为：1~4

###### 方法二

由于并没有对`page`的值进行约束，官方APP采用的方法是请求到空值时结束，如当`totalCount`值为`70`时，`page`值为`5`的请求将会得到类似以下的返回：

```json
{
	"code": 1,
	"isMainTeacher": 0,
	"uploadUrl": "https://upload.icve.com.cn/?space=ssykt&time=637595532185345877&bucket=icve&token=EAE2FC5B82C9A132AA750FF1EB8D23A9",
	"previewUrl": "",
	"list": [],
	"pagination": {
		"totalCount": 70,
		"pageSize": 20,
		"pageIndex": 5
	}
```

可以看到用于承载评论的列表`list`为空，脚本执行到此时便可以视为已经拿到所有评论

### 对某一课件添加评论（回复）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/BBS/addCellComment`

##### Method

POST

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Content-Type    | application/x-www-form-urlencoded; charset=utf-8             |
| Content-Length  | 575                                                          |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| Cookie          | auth=01021....AF;                                            |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

None

##### Form

| Key                 | Value                                                        |
| ------------------- | ------------------------------------------------------------ |
| **data**            | {  "CellId" : "yei4adoqpk1nkt8lwur1lg",  "CourseOpenId" : "0c...iw",  "OpenClassId" : "goy...uw",  "DocJson" : "[\n\n]",  "UserId" : "9...rw",  "Star" : 5,  "SourceType" : 3,  "Content" : "好" } |
| equipmentApiVersion | 14.6                                                         |
| equipmentAppVersion | 2.8.43                                                       |
| equipmentModel      | iPhone 11                                                    |
| **newToken**        | @92d....3b                                                   |
| sourceType          | 3                                                            |

说明：

- **data**：添加评论的关键参数，值视为json：

  ```json
  {  
   "CellId" : "yei4adoqpk1nkt8lwur1lg",
   "CourseOpenId" : "0cw....iw",
   "OpenClassId" : "go....uw",
   "DocJson" : "[\n\n]",
   "UserId" : "9ml...irw",
   "Star" : 5, 
   "SourceType" : 3,
   "Content" : "好" 
  }
  ```

  - **CellId**：课件ID
  - **courseId**：课程ID
  - **openClassId**：开课班级ID
  - DocJson：附件列表
  - **UserId**：个人用户ID
  - **Star**：评星，取值范围：1~5
  - SourceType：未知
  - **Content**：评论内容

#### Response

##### Code

200

##### Header

| Key            | Value                                        |
| -------------- | -------------------------------------------- |
| Cache-Control  | no-cache                                     |
| Content-Type   | text/html; charset=utf-8                     |
| Date           | Thu, 17 Jun 2021 11:23:35 GMT                |
| Expires        | -1                                           |
| Pragma         | no-cache                                     |
| **Set-Cookie** | acw_tc=2f6....5;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                        |
| X-Upstream     | 0-9                                          |
| Content-Length | 34                                           |
| Connection     | keep-alive                                   |

说明：

- Expires：未知

##### Json

```json
{
	"code": 1,
	"msg": "添加成功！"
}
```

*失败场景请自行尝试*

## 课件操作

### 获取课件信息

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/AssistTeacher/getCellInfoByCellId`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=01...AF;                                                |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value                  |
| ------------------- | ---------------------- |
| **cellId**          | w0i4adoquyfgefitiajzyg |
| equipmentApiVersion | 14.6                   |
| equipmentAppVersion | 2.8.43                 |
| equipmentModel      | iPhone 11              |
| isTeaSee            | 0                      |
| **newToken**        | @92....3b              |
| **openClassId**     | goy....iuw             |
| sourceType          | 3                      |
| **stuId**           | 9m....irw              |

说明：

- cellId：课件ID
- isTeaSee：暂时未知

##### Form

None

#### Response

##### Code

200

##### Header

| Key            | Value                                                   |
| -------------- | ------------------------------------------------------- |
| Cache-Control  | no-cache                                                |
| Content-Type   | text/html; charset=utf-8                                |
| Date           | Thu, 17 Jun 2021 09:57:24 GMT                           |
| Expires        | -1                                                      |
| Pragma         | no-cache                                                |
| **Set-Cookie** | acw_tc=2f6...171a0ddd850ff;path=/;HttpOnly;Max-Age=1800 |
| Vary           | Accept-Encoding                                         |
| X-Powered-By   | TXTEK                                                   |
| X-Upstream     | 0-177                                                   |
| Content-Length | 1655                                                    |
| Connection     | keep-alive                                              |

##### Json

```json
{
	"code": 1,
	"msg": "获得成功！",
	"cellInfo": {
		"topicId": "ceq...2ra",
		"cellId": "w0i4a...ajzyg",
		"cellName": "习近平在纪念毛泽东同志诞辰120周年座谈会上的讲话",
		"cellType": 1,
		"cellContent": "",
		"resourceUrl": "{\"extension\":\"mp4\",\"category\":\"video\",\"urls\":{\"status\":\"https://upload.icve.com.cn/ssykt/g@FB320B52DC51927FA950F053802AE354.mp4/status?time=637595494443280982&token=4013D13D7F1A016A117A3992A6C4441C\",\"preview\":\"https://file.icve.com.cn/ssykt/1004/130/FB320B52DC51927FA950F053802AE354.mp4\",\"download\":\"https://file.icve.com.cn/ssykt/1004/130/FB320B52DC51927FA950F053802AE354.mp4?response-content-disposition=attachment;filename=习近平在纪念毛泽东同志诞辰120周年座谈会上的讲话.mp4\",\"preview_oss_ori\":\"https://file.icve.com.cn/ssykt/1004/130/FB320B52DC51927FA950F053802AE354.mp4\",\"oss_ori_internal_url\":\"https://icve.oss-cn-hangzhou-internal.aliyuncs.com/ssykt/1004/130/FB320B52DC51927FA950F053802AE354.mp4\",\"preview_oss_gen\":\"https://file.icve.com.cn/ssykt_gen/1004/130/FB320B52DC51927FA950F053802AE354.mp4\",\"oss_gen_internal_url\":\"https://icve.oss-cn-hangzhou-internal.aliyuncs.com/ssykt_gen/1004/130/FB320B52DC51927FA950F053802AE354.mp4\",\"owa_url\":\"\"},\"isH5\":0,\"h5PreviewUrl\":\"\",\"args\":{\"360p\":true,\"480p\":true,\"720p\":true},\"status\":2}",
		"categoryName": "视频",
		"externalLinkUrl": "",
		"extension": "video",
		"isAllowDownLoad": false,
		"stuCellViewTime": 249.0,
		"stuCellPicCount": 1,
		"stuStudyNewlyTime": 241.0,
		"stuStudyNewlyPicNum": 0,
		"cellLogId": "",
		"token": "gesnauqtvlzfafyqzgv96w",
		"isNeedUpdate": 0,
		"audioVideoLong": 460.00,
		"studyCellPercent": 52.39
	}
}
```

说明：

- topicId：单元ID

- cellId：课件ID

- cellName：课件标题

- cellTye：未知

- cellContent：未知

- categoryName：课件种类，见上

- externalLinkUrl：未知

- extension：暂时未知，可能用来指示课件种类或打开方式，如ppt时，该值为`office`

- isAllowDownLoad：是否允许下载

- **stuCellViewTime**：用户观看总时长，单位：秒，下同

- stuCellPicCount：未知

- **stuStudyNewlyTime**：（仅限 视频 或 音频 类型，非该类型值为`0.0`）用户上次观看的时间位置，用于定位

- **stuStudyNewlyPicNum**：（仅限 ppt 或 文档 类型，非该类型值为`0`）用户上次观看的页数，用于定位

- cellLogId：未知

- token：未知作用

- isNeedUpdate：未知

- **audioVideoLong**：（任何类型）课件总长度

- **studyCellPercent**：用户学习进度，两位浮点数

- **resourceUrl**：将其值视为Json解析入下：

  ```json
  {
      "extension": "mp4",
      "category": "video",
      "urls": {
          "status": "https://upload.icve.com.cn/ssykt/g@0A358938EB881188FB3699A5B8258406.mp4/status?time=637595554578577843&token=2BF35BED57E77A11C1381D9BC9B6561C",
          "preview": "https://file.icve.com.cn/ssykt/40/354/0A358938EB881188FB3699A5B8258406.mp4",
          "download": "https://file.icve.com.cn/ssykt/40/354/0A358938EB881188FB3699A5B8258406.mp4?response-content-disposition=attachment;filename=走近毛泽东.mp4",
          "preview_oss_ori": "https://file.icve.com.cn/ssykt/40/354/0A358938EB881188FB3699A5B8258406.mp4",
          "oss_ori_internal_url": "https://icve.oss-cn-hangzhou-internal.aliyuncs.com/ssykt/40/354/0A358938EB881188FB3699A5B8258406.mp4",
          "preview_oss_gen": "https://file.icve.com.cn/ssykt_gen/40/354/0A358938EB881188FB3699A5B8258406.mp4",
          "oss_gen_internal_url": "https://icve.oss-cn-hangzhou-internal.aliyuncs.com/ssykt_gen/40/354/0A358938EB881188FB3699A5B8258406.mp4",
          "owa_url": ""
      },
      "isH5": 0,
      "h5PreviewUrl": "",
      "args": {
          "360p": true,
          "480p": true,
          "720p": true
      },
      "status": 2
  }
  ```


### 获取课件

请参考上一教程，获取课件信息后，直接请求其返回结果中`resourceUrl`中`download`的值（全部）即可获取到课件文件

### 评论-获取所有评论

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/BBS/getCellBBSList`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| Cookie          | auth=01....AF;                                               |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value                  |
| ------------------- | ---------------------- |
| activeType          | 1                      |
| **cellId**          | yei4adoqpk1nkt8lwur1lg |
| **courseOpenId**    | 0cw....piw             |
| equipmentApiVersion | 14.6                   |
| equipmentAppVersion | 2.8.43                 |
| equipmentModel      | iPhone 11              |
| **newToken**        | @92d....33b            |
| **openClassId**     | go....uw               |
| **page**            | 1                      |
| **pageSize**        | 20                     |
| sourceType          | 3                      |
| **userId**          | 9m....irw              |

说明：

- activityType：未知
- cellId：课件ID
- courseOpenId：课程ID
- openClassId：开课班级ID
- page：请求的页数
- pageSize：返回评价列表长度，如上20代表一次性返回20个评论信息，建议保持20
- userId：用户ID

##### Form

None

#### Response

##### Code

200

##### Header

| Key               | Value                                          |
| ----------------- | ---------------------------------------------- |
| Cache-Control     | no-cache                                       |
| Content-Type      | text/html; charset=utf-8                       |
| Date              | Thu, 17 Jun 2021 11:00:17 GMT                  |
| Expires           | -1                                             |
| Pragma            | no-cache                                       |
| Set-Cookie        | acw_tc=2f6...cf48;path=/;HttpOnly;Max-Age=1800 |
| Vary              | Accept-Encoding                                |
| X-Powered-By      | TXTEK                                          |
| X-Upstream        | 0-168                                          |
| Transfer-Encoding | chunked                                        |
| Connection        | keep-alive                                     |

##### Json

```json
{
	"code": 1,
	"isMainTeacher": 0,
	"uploadUrl": "https://upload.icve.com.cn/?space=ssykt&time=637595532170118594&bucket=icve&token=D98019068B43E08CA61461B6D6F19432",
	"previewUrl": "",
	"list": [{
		"Id": "lt6qaowscq5ffuupdyusfg",
		"dateCreated": "2021-03-08 08:47:27",
		"userId": "og...ybw",
		"displayName": "刘XX",
		"avatorUrl": "https://zjy2.icve.com.cn/common/images/default_avatar.jpg",
		"content": "好",
		"star": 5.0,
		"isAccept": 0,
		"docJson": [],
		"isPowerDelete": 0,
		"replyCount": 0
	},
       ....
  {
		"Id": "hwglaowsikxkvi0m94yy5q",
		"dateCreated": "2021-03-08 08:27:28",
		"userId": "kwp...kg",
		"displayName": "李XX",
		"avatorUrl": "https://zjy2.icve.com.cn/common/images/default_avatar.jpg",
		"content": "好",
		"star": 5.0,
		"isAccept": 0,
		"docJson": [],
		"isPowerDelete": 0,
		"replyCount": 0
	}],
	"pagination": {
		"totalCount": 70,
		"pageSize": 20,
		"pageIndex": 4
	}
}
```

说明：

- isMainTeacher：根据名称估测用于判断是否为主教师提供的课件，无使用价值
- uploadUrl：未知
- previewUrl：未知
- **Id**：可以视为该评论ID
- dateCreated：评论提交日期
- userId：评论提交者ID
- displayName：评论提交者姓名
- avatorUrl：评论提交者头像地址
- **content**：评论内容
- **star**：评星，值范围：0.0~5.0
- isAccept：未知
- docJson：未知，可能是附件相关，欢迎补充
- isPowerDelete：未知
- replyCount：回复下他人的评论数
- **totalCount**：评论总数
- pageSize：评论列表长度
- pageIndex：当前请求的页面数

#### 关于获取到完整的评论列表

##### 方法一

由于返回的评论列表长度`pageSize`默认值为`20`（未尝试过其他值，自行尝试，后果自负），初次请求后将会得到评论总数`totalCount`，根据评论总数即可推断应请求的总页数值，如`totalCount`的值为`70`时，`page`参数的取值范围为：1~4

##### 方法二

由于并没有对`page`的值进行约束，官方APP采用的方法是请求到空值时结束，如当`totalCount`值为`70`时，`page`值为`5`的请求将会得到类似以下的返回：

```json
{
	"code": 1,
	"isMainTeacher": 0,
	"uploadUrl": "https://upload.icve.com.cn/?space=ssykt&time=637595532185345877&bucket=icve&token=EAE2FC5B82C9A132AA750FF1EB8D23A9",
	"previewUrl": "",
	"list": [],
	"pagination": {
		"totalCount": 70,
		"pageSize": 20,
		"pageIndex": 5
	}
```

可以看到用于承载评论的列表`list`为空，脚本执行到此时便可以视为已经拿到所有评论

### 评论-添加评论

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/BBS/addCellComment`

##### Method

POST

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Content-Type    | application/x-www-form-urlencoded; charset=utf-8             |
| Content-Length  | 575                                                          |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| Cookie          | auth=01021....AF;                                            |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

None

##### Form

| Key                 | Value                                                        |
| ------------------- | ------------------------------------------------------------ |
| **data**            | {  "CellId" : "yei4adoqpk1nkt8lwur1lg",  "CourseOpenId" : "0c...iw",  "OpenClassId" : "goy...uw",  "DocJson" : "[\n\n]",  "UserId" : "9...rw",  "Star" : 5,  "SourceType" : 3,  "Content" : "好" } |
| equipmentApiVersion | 14.6                                                         |
| equipmentAppVersion | 2.8.43                                                       |
| equipmentModel      | iPhone 11                                                    |
| **newToken**        | @92d....3b                                                   |
| sourceType          | 3                                                            |

说明：

- **data**：添加评论的关键参数，值视为json：

  ```json
  {  
   "CellId" : "yei4adoqpk1nkt8lwur1lg",
   "CourseOpenId" : "0cw....iw",
   "OpenClassId" : "go....uw",
   "DocJson" : "[\n\n]",
   "UserId" : "9ml...irw",
   "Star" : 5, 
   "SourceType" : 3,
   "Content" : "好" 
  }
  ```

  - **CellId**：课件ID
  - **courseId**：课程ID
  - **openClassId**：开课班级ID
  - DocJson：附件列表
  - **UserId**：个人用户ID
  - **Star**：评星，取值范围：1~5
  - SourceType：未知
  - **Content**：评论内容

#### Response

##### Code

200

##### Header

| Key            | Value                                        |
| -------------- | -------------------------------------------- |
| Cache-Control  | no-cache                                     |
| Content-Type   | text/html; charset=utf-8                     |
| Date           | Thu, 17 Jun 2021 11:23:35 GMT                |
| Expires        | -1                                           |
| Pragma         | no-cache                                     |
| **Set-Cookie** | acw_tc=2f6....5;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                        |
| X-Upstream     | 0-9                                          |
| Content-Length | 34                                           |
| Connection     | keep-alive                                   |

说明：

- Expires：未知

##### Json

```json
{
	"code": 1,
	"msg": "添加成功！"
}
```

*失败场景请自行测试*

### 问答-获取所有问答

### 问答-添加问答

### 笔记-获取所有笔记

### 笔记-添加笔记

### 纠错-获取所有纠错

### 纠错-添加纠错

## 课堂

### 获取某一课程的所有开课（CourseOpen）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/FaceTeach/getAllFaceTeachListByStu`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=01.....87;                                              |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.5.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value     |
| ------------------- | --------- |
| **courseOpenId**    | 82....og  |
| equipmentApiVersion | 14.5      |
| equipmentAppVersion | 2.8.43    |
| equipmentModel      | iPhone 11 |
| **newToken**        | @8e....d0 |
| **openClassId**     | qi....1w  |
| **page**            | 1         |
| sourceType          | 3         |
| **stuId**           | 9.....rw  |

说明：

- courseOpenId：即前获取所有课程中所包含的`courseOpenId`
- openClassId：同上
- stuId：即登陆后获取到的个人ID（`userId`）
- page：重要的参数值，由于返回的课程列表长度有限，需要使用该参数获取后续信息，具体操作请见下面Response部分

##### Form

None

#### Response

##### Code

200

##### Header

| Key               | Value                                          |
| ----------------- | ---------------------------------------------- |
| Cache-Control     | no-cache                                       |
| Content-Type      | text/html; charset=utf-8                       |
| Date              | Tue, 08 Jun 2021 13:23:29 GMT                  |
| Expires           | -1                                             |
| Pragma            | no-cache                                       |
| **Set-Cookie**    | acw_tc=2f......dc;path=/;HttpOnly;Max-Age=1800 |
| Vary              | Accept-Encoding                                |
| X-Powered-By      | TXTEK                                          |
| X-Upstream        | 0-197                                          |
| Transfer-Encoding | chunked                                        |
| Connection        | keep-alive                                     |

##### Json

```json
{
	"code": 1,
	"msg": "请求成功！",
	"dataList": [{
		"Id": "xu...vg",
		"courseOpenId": "82...og",
		"courseName": "XXXX",
		"className": "XXXX1234",
		"Title": "2021-04-27周二的课堂教学",
		"openClassId": "qi...1w",
		"dateCreated": "2021-04-27 11:14",
		"teachDate": "2021-04-27",
		"classSection": "34",
		"Address": "XX206",
		"state": 3
	}, 
    ......
 {
		"Id": "d3....kw",
		"courseOpenId": "82...og",
		"courseName": "XXXX",
		"className": "XXXX1234",
		"Title": "2021-04-06周二的课堂教学",
		"openClassId": "qi....1w",
		"dateCreated": "2021-04-06 08:16",
		"teachDate": "2021-04-06",
		"classSection": "12",
		"Address": "XX206",
		"state": 3
	}],
	"pagination": {
		"pageSize": 10,
		"pageIndex": 2,
		"totalCount": 28
	}
}
```

说明：

- Id：开课ID（即每一节课的ID）
- courseOpenId：课程ID
- courseName：课程名
- className：班级名
- Title：标题
- openClassId：开课班级ID，即上 获取所有课程 中的`openClassId`
- dateCreated：创建开课的时间
- teachDate：上课时间
- classSection：开课排序，如12即表示 第一节和第二节
- Address：上课地点
- state：未知



- pageSize：表示返回开课列表的长度，这里的10表示一次返回10节课的信息
- pageIndex：表示当前返回的课列表为第几页，与Request中的page参数关联
- totalCount：开课的总数

#### 关于获取完整的开课列表

由于返回的开课列表长度有限，获取完整列表即需要多次请求，首次请求page自然为`1`，根据返回的Json数据中的totalCount和pageSize即可计算出page的范围，如：

totalCount为28，pageSize为10，即可得出page值范围应为1～3才能获取完整的开课列表

### 获取某一天的开课

请参考 今日课堂 ，可以观察到请求参数中包含重要的`faceDate`参数（今日课堂实现原理），格式为：

`[year]-[month]-[day]`

通过修改参数日期即可获取到不同日期的开课情况

**注意：**即使日期不正确（如未来日期或不切实际的日期），返回的情况依然和无课情况相同，即返回的`dataList`值为空（`code`值仍然为`1`）

## 课堂操作

### 获取课堂信息（课前、课中、课后）

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/faceTeach/getStuFaceActivityList`

**特殊说明**：

课堂的三标签——课前、课中和课后公用上述API，使用参数`classState`来区别，定义如下

| classState值 | 对应 |
| ------------ | ---- |
| 1            | 课前 |
| 2            | 课中 |
| 3            | 课后 |

**注意：**由于课后项目：课堂表现，课堂评价，自我总结是固定的，以上API并不会获取到这3个项目，请看下一章节

##### Method

GET

##### Header

| Host            | zjyapp.icve.com.cn                                           |
| --------------- | ------------------------------------------------------------ |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| Cookie          | auth=010......564;                                           |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value                 |
| ------------------- | --------------------- |
| activityId          | ucpiaettodeqf0jlpdvoq |
| classState          | 2                     |
| equipmentApiVersion | 14.6                  |
| equipmentAppVersion | 2.8.43                |
| equipmentModel      | iPhone 11             |
| newToken            | @d4......92           |
| openClassId         | 9x......fg            |
| sourceType          | 3                     |
| stuId               | 9mll......rw          |

##### Form

None

#### Response

##### Code

200

##### Header

| Key            | Value                                         |
| -------------- | --------------------------------------------- |
| Cache-Control  | no-cache                                      |
| Content-Type   | text/html; charset=utf-8                      |
| Date           | Thu, 24 Jun 2021 13:56:09 GMT                 |
| Expires        | -1                                            |
| Pragma         | no-cache                                      |
| Set-Cookie     | acw_tc=2f6....38;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                         |
| X-Upstream     | 0-4                                           |
| Content-Length | 596                                           |
| Connection     | keep-alive                                    |

##### Json

```json
{
	"code": 1,
	"msg": "请求成功！",
	"isEvaluation": 0,
	"faceEvaluation": 0,
	"dataList": [{
		"Id": "gzhiaets59plvcjaa2rhw",
		"Title": "2021-06-22 13:43的签到",
		"DateCreated": "2021/6/22 13:43:33",
		"CreatorId": "uc50aacmllzjp8z4u43viw",
		"DataType": "签到",
		"State": 3,
		"SignType": 1,
		"Gesture": "",
		"AskType": -1,
		"ViewAnswer": 0,
		"resourceUrl": null,
		"cellType": 0,
		"categoryName": null,
		"moduleId": null,
		"cellSort": 0,
		"hkOrExamType": 0,
		"paperType": 0,
		"termTimeId": null,
		"isForbid": 0,
		"fixedPublishTime": null,
		"examStuId": null,
		"examWays": 0,
		"isAuthenticate": 0,
		"isAnswerOrPreview": 0,
		"isPreview": 0,
		"StuStartDate": null,
		"StuEndDate": null
	}]
}
```

### 课后

## 考试

### 获取所有的考试列表

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/OnlineExam/getExamList_new`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| Cookie          | auth=0102....E5;                                             |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value                             |
| ------------------- | --------------------------------- |
| courseOpenId        | 6k3gakmsgadkt7pgmcsbvg            |
| equipmentApiVersion | 14.6                              |
| equipmentAppVersion | 2.8.43                            |
| equipmentModel      | iPhone 11                         |
| exType              | 0                                 |
| examState           | 0                                 |
| newToken            | @92da25c6118d4c1dbf4a8f5dd6e4033b |
| openClassId         | wydyakmsdlzi493wixlcdw            |
| page                | 1                                 |
| pageSize            | 10                                |
| sourceType          | 3                                 |
| stuId               | 9mllaeymkoxf4qpfre9irw            |
| title               |                                   |

##### Form

None

#### Response

##### Code

200

##### Header

| Key            | Value                                        |
| -------------- | -------------------------------------------- |
| Cache-Control  | no-cache                                     |
| Content-Type   | text/html; charset=utf-8                     |
| Date           | Thu, 17 Jun 2021 14:24:37 GMT                |
| Expires        | -1                                           |
| Pragma         | no-cache                                     |
| Set-Cookie     | acw_tc=2f6...c7;path=/;HttpOnly;Max-Age=1800 |
| X-Powered-By   | TXTEK                                        |
| X-Upstream     | 0-168                                        |
| Content-Length | 618                                          |
| Connection     | keep-alive                                   |

##### Json

```json
{
	"code": 1,
	"msg": "请求成功！",
	"examList": [{
		"examId": "vipaakqszahao7ong0eqjq",
		"examType": 1,
		"ztWay": 2,
		"examTermTimeId": "ijbakqskjxbci7aagqkra",
		"title": "《XXX史》（A）2020-2021学年第一学期期末考试试卷",
		"remark": "",
		"startDate": "2021-01-12 09:00:00",
		"endDate": "2021-01-12 10:30:00",
		"readStuCount": 0,
		"unReadStuCount": 0,
		"unTakeCount": 0,
		"stuExamState": "90.00",
		"examStuId": "2nspak6soppm0ft6khyd2w",
		"isExamEnd": 0,
		"isAnswerOrPreview": 3,
		"isSetTime": 1,
		"isPreview": 1,
		"fixedPublishTime": "2021-01-12 10:31:00",
		"isForbid": 0,
		"examWays": 1,
		"isAuthenticate": 0,
		"isValidExam": 1,
		"reasonText": "",
		"isVerified": 0
	}]
}
```

说明：

- examId：考试ID
- examType：据估测`1`对应为 题库考试（类型包括题库考试和登分考试）
- ztWay：未知
- examTermTimeId：未知
- title：考试标题
- remark：未知
- startDate：开始时间
- endDate：结束时间
- readStuCount：根据字意估测为 已读学生数 或 已做学生数
- unReadStuCount：根据字意估测为 未读学生数 或 未做学生数
- unTakeCount：未知
- stuExamState：考试得分，范围：0.00~100.00
- examStuId：未知
- isExamEnd：估测用来判断考试是否关闭
- isAnswerOrPreview：未知
- isSetTime：估测用于判断是否设置了期限
- isPreview：未知
- fixedPublishTime：估测为考试结束后公开查看时间
- isForbid：未知
- examWays：估测`1`为 网页端，移动端 考试方式，
- isAuthenticate： 0,
- isValidExam:：未知
- reasonText：估测为考试说明
- isVerified：是否开启考试验证开关，0-False,1-True





### 获取某一考试内容

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/onlineexam/getStuExamPreviewNew`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=010...E5;                                               |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value                  |
| ------------------- | ---------------------- |
| **courseOpenId**    | 6k3....vg              |
| equipmentApiVersion | 14.6                   |
| equipmentAppVersion | 2.8.43                 |
| equipmentModel      | iPhone 11              |
| **examId**          | vipaakqszahao7ong0eqjq |
| **examStuId**       | 2nspak6soppm0ft6khyd2w |
| **newToken**        | @92da...3b             |
| **openClassId**     | wy...dw                |
| sourceType          | 3                      |

说明：

- examId：见上一操作
- examStuId：见上一操作

##### Form

None

#### Response

##### Code

200

##### Header

| Key               | Value                                         |
| ----------------- | --------------------------------------------- |
| Cache-Control     | no-cache                                      |
| Content-Type      | text/html; charset=utf-8                      |
| Date              | Thu, 17 Jun 2021 14:39:26 GMT                 |
| Expires           | -1                                            |
| Pragma            | no-cache                                      |
| Set-Cookie        | acw_tc=2f6...af5;path=/;HttpOnly;Max-Age=1800 |
| Vary              | Accept-Encoding                               |
| X-Powered-By      | TXTEK                                         |
| X-Upstream        | 0-13                                          |
| Transfer-Encoding | chunked                                       |
| Connection        | keep-alive                                    |

##### Json

```json
{
	"code": 1,
	"msg": "获取成功",
	"data": {
		"examId": "vipaakqszahao7ong0eqjq",
		"courseOpenId": "6k3gakmsgadkt7pgmcsbvg",
		"openClassId": "wydyakmsdlzi493wixlcdw",
		"ztWay": 2,
		"examTitle": "《XXX》（A）2020-2021学年第一学期期末考试试卷",
		"totalScore": 100.00,
		"remark": "",
		"uploadUrl": "https://upload.icve.com.cn/?space=ssykt&time=637595663663441630&bucket=icve&token=7EF9A1EF56C4E43188A4A79B61935B9A",
		"previewUrl": "",
		"state": 2,
		"canRead": 1,
		"questions": [{
			"paperStuQuestionId": "r3guak6srbzmo6hafnkbfa_0",
			"questionId": "qipaakqsszhne268flpcha",
			"questionType": 1,
			"queTypeName": "单选题",
			"sortOrder": 0,
			"title": "<p>XXXX</p>",
			"dataJson": "[{\"SortOrder\":0,\"Content\":\"X\",\"IsAnswer\":true},{\"SortOrder\":1,\"Content\":\"X\",\"IsAnswer\":false},{\"SortOrder\":2,\"Content\":\"X\",\"IsAnswer\":false},{\"SortOrder\":3,\"Content\":\"X\",\"IsAnswer\":false}]",
			"answer": "0",
			"newAnswer": "0",
			"resultAnalysis": "教材XXXX物。",
			"questionScore": 2.00,
			"isAssignmented": 1,
			"studentAnswer": "0",
			"newStudentAnswer": "0",
			"uploadUrl": "https://upload.icve.com.cn/?space=ssykt&time=637595663663441630&bucket=icve&token=7EF9A1EF56C4E43188A4A79B61935B9A",
			"previewUrl": "",
			"isRight": 1,
			"getScore": 2.00,
			"bigQuestionId": "",
			"commentary": "",
			"commentaryFileData": [],
			"subQuestionList": []
		}, 
           .....
    {
			"paperStuQuestionId": "r3guak6srbzmo6hafnkbfa_32",
			"questionId": "qipaakqsg4nj5bzfg3wddw",
			"questionType": 6,
			"queTypeName": "问答题",
			"sortOrder": 32,
			"title": "<p>谈一谈你学习XXXX的心得体会，并结合自身谈一谈启示。</p>",
			"dataJson": "",
			"answer": "<p>参考思路：</p><p>可以参考以下几个方面谈体会或启示，同时可以结合相关历史人物、技术发明等进行论证：</p><p>（1）有助于了解我国XXX发展历程，增进对XXXX的喜爱；</p>
                  ....
                  <p>5-7分：有一定体会和感悟，整体比较宏观抽象，但缺少具体事例或相关细节论据；能够联系自身，但联系不够具体；</p><p>5分以下：体会和感悟比较空洞，联系自身较少；</p>",
			"newAnswer": "<p>参考思路：</p><p>可以参考以下几个方面谈体会或启示，同时可以结合相关历史人物、技术发明等进行论证：</p>
                  ....
                  <p>5分以下：体会和感悟比较空洞，联系自身较少；</p>",
			"resultAnalysis": "",
			"questionScore": 10.00,
			"isAssignmented": 1,
			"studentAnswer": "在学习XXX
                  ....
                  取得进步。",
			"uploadUrl": "https://upload.icve.com.cn/?space=ssykt&time=637595663663441630&bucket=icve&token=7EF9A1EF56C4E43188A4A79B61935B9A",
			"previewUrl": "",
			"isRight": 3,
			"getScore": 7.00,
			"bigQuestionId": "",
			"commentary": "",
			"commentaryFileData": [],
			"subQuestionList": []
		}]
	}
}
```



## 作业

### 获取某一课的所有作业

#### Request

##### API

`https://zjyapp.icve.com.cn/newMobileAPI/homework/getHomeworkList_new`

##### Method

GET

##### Header

| Key             | Value                                                        |
| --------------- | ------------------------------------------------------------ |
| Host            | zjyapp.icve.com.cn                                           |
| Accept          | */*                                                          |
| Connection      | keep-alive                                                   |
| **Cookie**      | auth=010.....E5;                                             |
| User-Agent      | yktIcve/2.8.43 (com.66ykt.66yktteacherzhihui; build:2021042101; iOS 14.6.0) Alamofire/4.7.3 |
| Accept-Language | zh-Hans-CN;q=1.0                                             |
| Referer         | https://file.icve.com.cn/                                    |
| Accept-Encoding | gzip;q=1.0, compress;q=0.5                                   |

##### Params

| Key                 | Value     |
| ------------------- | --------- |
| **courseOpenId**    | 9k...wa   |
| equipmentApiVersion | 14.6      |
| equipmentAppVersion | 2.8.43    |
| equipmentModel      | iPhone 11 |
| **hkState**         | 0         |
| **homeworkType**    | 0         |
| **newToken**        | @92....3b |
| **openClassId**     | 5la...aa  |
| **page**            | 1         |
| **pageSize**        | 10        |
| sourceType          | 3         |
| **stuId**           | 9m...rw   |
| title               |           |

说明：



##### Form

None

#### Response

##### Code

200

##### Header

| Key               | Value                                         |
| ----------------- | --------------------------------------------- |
| Cache-Control     | no-cache                                      |
| Content-Type      | text/html; charset=utf-8                      |
| Date              | Thu, 17 Jun 2021 14:49:22 GMT                 |
| Expires           | -1                                            |
| Pragma            | no-cache                                      |
| **Set-Cookie**    | acw_tc=2f6....60;path=/;HttpOnly;Max-Age=1800 |
| Vary              | Accept-Encoding                               |
| X-Powered-By      | TXTEK                                         |
| X-Upstream        | 0-168                                         |
| Transfer-Encoding | chunked                                       |
| Connection        | keep-alive                                    |

##### Json

```json
{
	"code": 1,
	"msg": "请求成功！",
	"homeworkList": [{
		"homeworkId": "3bq5aestaq5brhsv4s4wa",
		"homeworkTermTimeId": "d6g5aestdppevotteauf3a",
		"title": "染料部分",
		"homeworkType": 4,
		"ztWay": 3,
		"remark": "1、染料与颜料的区别\r\n2、染料怎样命名？\r\n3、染料的一般生产过程包括哪些步骤？",
		"startDate": "2021-06-11 11:15",
		"endDate": "2021-06-19 00:00",
		"readStuCount": 0,
		"unReadStuCount": 0,
		"unSubmitCount": 0,
		"replyCount": 1,
		"stuAnwerHomeworkCount": 1,
		"stuHomeworkState": "待批阅",
		"isTakeHomework": true,
		"isSetTime": 1,
		"isForbid": 0,
		"IsGrouped": 0,
		"paperType": 2,
		"isShowStuEva": 0
	}, 
          .....
  {
		"homeworkId": "x3cmap6swajewgh0m5nlkq",
		"homeworkTermTimeId": "1lnap6so79f5k7gdyanw",
		"title": "什么是化学键？化学键有几种类型？分别是什么含义？",
		"homeworkType": 4,
		"ztWay": 3,
		"remark": "",
		"startDate": "2021-04-02 09:56",
		"endDate": "2021-04-16 23:34",
		"readStuCount": 0,
		"unReadStuCount": 0,
		"unSubmitCount": 0,
		"replyCount": 1,
		"stuAnwerHomeworkCount": 1,
		"stuHomeworkState": "95.00",
		"isTakeHomework": true,
		"isSetTime": 1,
		"isForbid": 0,
		"IsGrouped": 0,
		"paperType": 2,
		"isShowStuEva": 0
	}],
	"hkPageSize": 10
}
```

说明：



### 课堂测试查看答案

——https://www.cqrzr.com/post/55.html

#### Request

##### API

`https://zjy2.icve.com.cn/api/teacher/faceTeachInfos/testPreview`

##### Method

GET

##### Header

省略

##### Params

| Name         | Value | 说明 |
| ------------ | ----- | ---- |
| courseOpenId |       |      |
| activityId   |       |      |
| classTest    |       |      |
| type         | 1     |      |



##### Form



#### Response

##### Code



##### Header



##### Json



### 模版

#### Request

##### API

``

##### Method

GET

##### Header



##### Params



##### Form



#### Response

##### Code



##### Header



##### Json



### 
