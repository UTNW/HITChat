<%@ page language="java"  pageEncoding="UTF-8"%>
<%@ taglib uri="/struts-tags" prefix="s" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">

<html>

<!-- 最新 Bootstrap 核心 CSS 文件 -->
<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">

<!-- 可选的Bootstrap主题文件（一般不用引入） -->
<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap-theme.min.css">

<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>

<link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>
</head>
<body>

  <ul class="nav nav-pills nav-stacked">
  <li class="active"><a href="#"><span class="glyphicon glyphicon-align-justify"></span>教育背景</a></li>
  </ul>


<div class="line">
 <div class="col-sm-9 col-md-3">
    <div class="thumbnail">
      <div class="caption">

<div class="list-group">

 <ul class="nav nav-pills nav-stacked">
 <li ><a href="#" class="list-group-item"><span class="glyphicon glyphicon-send"></span>个人设置</a></li>
 </ul>

 <a href="BasicMessage.jsp" class="list-group-item">基本资料</a>
 <a href="Educate.jsp" class="list-group-item active">教育背景</a>
 <a href="Work.jsp" class="list-group-item">工作信息</a>
 <a href="#" class="list-group-item">头像设置</a>
 <br></br>

 <ul class="nav nav-pills nav-stacked">
 <li ><a href="#" class="list-group-item"><span class="glyphicon glyphicon-star"></span>隐私设置</a></li>
 </ul>

 <a href="BasicMessage.jsp" class="list-group-item" >我在贴吧</a>
 <br></br>
 <img src="image/3.jpg" alt="..." class="img-thumbnail">
</div>

      </div>
    </div>
  </div>
</div>


<div class="line">
 <div class="col-sm-9 col-md-8">
    <div class="thumbnail">
      <div class="caption">

 <div class="list-group">

 <ul class="nav nav-pills nav-stacked">
 <li ><a href="#" class="list-group-item"><span class="glyphicon glyphicon-send"></span>教育背景</a></li>
 </ul>

 <br></br>

<label class="inline col-md-offset-1">体型：&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</label>

<label class="select-inline">
<select class="form-control">
  <option>未知</option>
  <option>苗条</option>
  <option>丰满</option>
  <option>中等身材</option>
  <option>高大</option>
  <option>小巧</option>
  <option>运动型</option>
  <option>健美</option>
</select>
</label>
<br></br>


<label class="inline  col-md-offset-1">婚姻状况：</label>
<label class="select-inline">
<select class="form-control">
  <option>未知</option>
  <option>单身</option>
  <option>已婚</option>
  <option>恋爱</option>
  <option>离异</option>
</select>
</label>
<br></br>

<label class="inline   col-md-offset-1">个人习惯：</label>

<label class="select-inline">
<select class="form-control">
  <option>憎恶抽烟</option>
  <option>从不抽烟</option>
  <option>偶尔抽烟</option>
  <option>应酬时抽烟</option>
  <option>心情不好时抽烟</option>
</select>
</label>


<label class="select-inline">
<select class="form-control">
  <option>憎恶饮酒</option>
  <option>从不饮酒</option>
  <option>偶尔饮酒</option>
  <option>应酬时饮酒</option>
  <option>心情不好时饮酒</option>
</select>
</label>


<label class="select-inline">
<select class="form-control">
  <option>早睡早起</option>
  <option>爱谁懒觉</option>
  <option>经常熬夜</option>
  <option>昼伏夜出</option>
  <option>经常失眠</option>
</select>
</label>
<br></br>

<label class="inline   col-md-offset-1">性格：&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</label>


<label class="checkbox-inline">
  <input type="checkbox" value="man"> 温柔
</label>

<label class="checkbox-inline col-md-offset-2">
  <input type="checkbox" value="woman"> 粗犷
</label>


<label class="checkbox-inline col-md-offset-2">
  <input type="checkbox" value="woman"> 活泼
</label>

<label class="checkbox-inline col-md-offset-2">
  <input type="checkbox" value="woman"> 老成
</label>

<label class="checkbox-inline col-md-offset-2">
  <input type="checkbox" value="woman"> 内向
</label>
<br></br>

<label class="inline   col-md-offset-1">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</label>

<label class="checkbox-inline">
  <input type="checkbox" value="man"> 开朗
</label>

<label class="checkbox-inline col-md-offset-2">
  <input type="checkbox" value="woman"> 豪爽
</label>

<label class="checkbox-inline col-md-offset-2">
  <input type="checkbox" value="woman"> 沉默
</label>


<label class="checkbox-inline col-md-offset-2">
  <input type="checkbox" value="woman"> 急躁
</label>

<label class="checkbox-inline col-md-offset-2">
  <input type="checkbox" value="woman"> 稳重
</label>
<br></br>

<label class="inline  col-md-offset-1">教育程度：</label>
<label class="select-inline">
<select class="form-control">
  <option>未知</option>
  <option>初中</option>
  <option>高中</option>
  <option>大学</option>
  <option>硕士</option>
  <option>博士</option>
  <option>中专/技校</option>
  <option>其他</option>
</select>
</label>
<br></br>


<label class="inline  col-md-offset-1">当前职业：</label>
<label class="select-inline">
<select class="form-control">
  <option>未知</option>
  <option>广告/营销/公关</option>
  <option>航天</option>
  <option>汽车</option>
  <option>建筑</option>
  <option>计算机/电子产品</option>
  <option>农业/化工/林业</option>
  <option>教育</option>
  <option>招待</option>
  <option>能源/采矿</option>
  <option>金融</option>
  <option>政府</option>
  <option>招待</option>
  <option>传媒</option>
  <option>医疗</option>
  <option>零售</option>
  <option>服务</option>
  <option>其他</option>
</select>
</label>
<br></br>

<label class="inline   col-md-offset-1">联系方式：</label>
<label class="select-inline">
<input type="text" class="form-control" placeholder="电子邮箱或者手机号码">
</label>
<br></br>

<p>
<label class="inline">&nbsp&nbsp&nbsp&nbsp</label>
<a href="#" class="btn btn-primary btn-lg     col-md-offset-2">保存</a>
</p>

      </div>
    </div>
  </div>
</div>

</body>
</html>