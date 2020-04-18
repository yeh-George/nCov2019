# nCov2019： 新冠肺炎数据发布的SPA项目
 本项目通过调用[GitHub: 2019新型冠状病毒疫情实时爬虫](https://github.com/BlankerL/DXY-COVID-19-Crawler)提供的Web API接口来获取新冠肺炎相关数据，再基于jQuery（JavaScript）实现一个简单的单页程序（Single Page Application, SPA）。  

**Demo: [nCov2019](http://203.195.141.243/)**

## 主要功能：
 * 疫情数据展示页：新冠肺炎实时数据的展示
 * 祝福语展示页：发送祝福、分页展示祝福语以及祝福语点赞
 
## 技术概要
 * Flask Web框架
 * 基于Google Material Design的Materialize框架
 * AJAX

## 实现的功能
 * **使用requests库调用Web API获取所需的数据** 
 
 * **单页程序的模板组织**：
     - 根页面：加载CSS和JavaScript文件，储存指向子页面URL的JavaScript变量，包含一个用来填充页面主体内容的main元素；
     - 子页面：分为疫情数据展示页（_intro.html）、祝福语展示页（_bless.html）两个局部模板。局部模板通过AJAX请求获取并动态插到根页面中。另外，为了方便组织局部模板，定义了一个包含导航栏和页脚的基模板（base.html）。为了分页展示祝福语信息，自己手动编写宏，实现了一个render_pagination分页组件;
     - 祝福语条目页面：为了让JavaScript可以操控条目， 将_bless.html中的祝福语条目内容分离成一个局部模板(\_bless_item.html)。  
     
 * **子页面切换的实现**：通过在URL后面添加hash来记录状态，再在window上绑定hashchange事件，在hash值发生变化时执行回调函数，发起相应的AJAX请求，获取到数据后替换到main元素中，实现动态切换页面的效果  
 
 * **祝福语条目的添加**：监听输入框的key up事件，通过event.which判断是回车键时，验证输入框数据,触发AJAXPOST请求，并设置相应的Content-Type首部，成功后，将返回的局部模板_bless_item.html通过prepend()方法添加到相应元素的开头  
 
 * **祝福语条目的点赞**：监听点赞图标的click事件，通过图标上的data-href获取对应的URL，触发type为PATCH的AJAX请求，成功后更新点赞数    
 
## 不足  
对Web API发起请求时，如果相邻两次请求时间间隔过短，会出现503错误，可以调用time.sleep( )解决该问题，但是会导致疫情数据展示页的加载时间过长。  
     
**解决思路**:   
       1. 由于数据爬虫的爬取间隔为1小时，可以用Flask-Caching结合Redis缓存疫情数据展示页视图，但是第一次访问响应时间仍然过长；  
       2. 建立数据库模型，结合Celery定时任务，每隔1小时调取Web API数据后写入模型中，每次使用模型数据渲染疫情数据展示页模板。
      
 
