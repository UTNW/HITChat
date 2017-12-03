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

<head>
<title>Insert title here</title>

</head>
<body>

  <ul class="nav nav-pills nav-stacked">
  <li class="active"><a href="#"><span class="glyphicon glyphicon-align-justify"></span>个人资料</a></li>
  </ul>


<div class="row">
 <div class="col-sm-9 col-md-3">
    <div class="thumbnail">
      <div class="caption">

<div class="list-group">

 <ul class="nav nav-pills nav-stacked">
 <li ><a href="#" class="list-group-item"><span class="glyphicon glyphicon-send"></span>个人设置</a></li>
 </ul>

  <a href="BasicMessage.jsp" class="list-group-item">基本资料</a>
  <a href="Educate.jsp" class="list-group-item">教育背景</a>
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


</body>
</html>