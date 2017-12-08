 /**
 * title hitchat聊天室 处理socket聊天逻辑组件
 * author UTNW
 * 2017-11-29
 */

/**
 * 通过渲染jade文件 运行聊天
 * @param  {[type]} dir [模板路径]
 * @param  {[type]} req [响应对象]
 * @param  {[type]} res [请求对象]
 * @param  {[type]} io  [socket.io对象]
 */
exports.renderJade=function(io,users){

	io.on("connection",function(socket){
		socket.on("login",function(nickname,photoid){
			console.log(users.indexOf(nickname));

			function exitsn(){
				var f=false;
				for(var i=0;i<users.length;i++){
					if(users[i]['user']==nickname){
						f=true;
						break;
					}else{
						f=false;
					}
				}
				return f;
			}
			if(exitsn()===false){
				socket.userIndex = users.length;
				socket.nickname = nickname;
				socket.photoid = photoid;
				users.push({"user":nickname,"photoid":photoid});
				socket.emit('loginSuccess');
				io.sockets.emit('system',nickname,users,users.length,'login');
			}else{
				socket.emit("nickExisted");
			}
		})
		socket.on("send msg",function(message){
			console.log(message);
			io.sockets.emit("newMsg",message,socket.nickname,users,socket.userIndex,socket.photoid);
		})

		socket.on("shake",function(){
			io.sockets.emit("newShake",socket.nickname)
		})

		socket.on("disconnect",function(){
			if(socket.nickname){
				users.splice(socket.userIndex,1);
				// console.log(users);
				socket.broadcast.emit('system',socket.nickname,users,users.length,"logout");

			}else{
				console.log("窗口关闭");
			}
		})
	})

}