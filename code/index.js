window.onload = function () {
	var el = document.getElementById("input");
	var myCodeMirror = CodeMirror.fromTextArea(el, {
		mode: "python", // 语言模式
		// theme: "leetcode", // 主题
		// keyMap: "sublime", // 快键键风格
		lineNumbers: true, // 显示行号
		smartIndent: true, // 智能缩进
		indentUnit: 4, // 智能缩进单位为4个空格长度
		indentWithTabs: true, // 使用制表符进行智能缩进
		lineWrapping: true, // 
		// 在行槽中添加行号显示器、折叠器、语法检测器
		gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"], 
		foldGutter: true, // 启用行槽中的代码折叠
		autofocus: true, // 自动聚焦
		matchBrackets: true, // 匹配结束符号，比如"]、}"
		autoCloseBrackets: true, // 自动闭合符号
		styleActiveLine: true, // 显示选中行的样式
	});
	// myCodeMirror.setOption("value", initValue);
	// 编辑器按键监听
	myCodeMirror.on("keypress", function() {
		// 显示智能提示
		// myCodeMirror.showHint();
	});
	var runs = document.getElementById("runs");
	runs.onclick = function() {
		var value = myCodeMirror.getValue();

		$.ajax({
			type: 'POST',
			url: "http://100.64.255.212:7001/runs",
			dataType: "json",
			data: JSON.stringify({
				"student_id": "a001",
				"file_name": "test01.py",
				"code_src": value
			}),
			success: function (data, status) {
				console.log(data)
				$("#stdout").val(data.stdout);
				$("#stderr").val(data.stderr);
			}
		});

	};
};