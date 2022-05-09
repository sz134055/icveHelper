var makeUUID = function(){
    var s = [];
    var hexDigits = "0123456789abcdef";
    for (var i = 0; i < 36; i++) {
        s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
    }
    s[14] = "4";  // bits 12-15 of the time_hi_and_version field to 0010
    s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);  // bits 6-7 of the clock_seq_hi_and_reserved to 01
    s[8] = s[13] = s[18] = s[23] = "";

    var uuid = s.join("");
    return uuid;
}

layui.use(['layer', 'form', 'element'], function(){
    var layer = layui.layer;
    var form = layui.form;
    var element = layui.element;

    //……
    //你的代码都应该写在这里面
    form.render();
    //表单取值

    layui.$('#LAY-component-form-getval').on('click', function(){
        var data = form.val('loginForm');
        layer.load(2);
        login(data);
        //alert(JSON.stringify(data));
    });

    //表单赋值
    layui.$('#LAY-component-form-setval').on('click', function(){
        form.val('loginForm', {
            'app':'2.8.43',
            'os':'15.0',
            'device':'iPhone 11',
            'clientId':makeUUID
        });
    });
    layui.$('#whyNeedMore').on('click',function () {
        layer.open({
            type:1,
            title:'为什么需要更多信息',
            content:layui.$('#questionBox'),
            cancel:function () {
                $('#questionBox').css('display','none');
                return true;
            }
        });
    });


    var login = function (loginInfo) {
        layer.closeAll('loading'); //关闭加载层
        $.ajax('/login/add',{
            type: 'POST',
            timeout:30000,
            data:loginInfo,
            dataType:'json',
            success:function (data,status) {

                if (data.code==='1'){
                    layer.msg(data.msg, {icon: 1});
                    setTimeout(function(){
                        window.location.href='/';
                    },3000);
                }else {
                    layer.msg(data.msg, {icon: 5});
                }
            },
            error:function () {
                layer.msg('服务器无响应，请稍后再试', {icon: 5});
            }
        })
    }
});

window.onload =function () {
    document.getElementById('LAY-component-form-setval').click();
}