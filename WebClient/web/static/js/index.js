var now_user;
function divSwitch(status,info) {
    var info_box = $('.info_box');
    //重置
    info_box.find('div').remove();
    if (status==='user'){
        if (now_user===undefined||now_user!==info.id) {
            var user_info_box = $('.user_info').clone();
            user_info_box.removeAttr('style')
            user_info_box.find('img').attr('src', info.header);
            user_info_box.find('span.user_num').text(info.num);
            user_info_box.find('span.user_id').text(info.id);
            info_box.append(user_info_box);
        }
    }else if (status==='free'){
        var now_free_box = $('.now_free_box').clone();
        now_free_box.removeAttr('style');
        info_box.append(now_free_box);

    }else{
        var ajax_info_box = $('.ajax_info_box').clone();
        ajax_info_box.removeAttr('style');
        info_box.append(ajax_info_box);
    }

}

function get_status(){
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState === 4){
            var getInfo = JSON.parse(req.responseText);
            //var nowUser = document.getElementById('nowUser');
            var nowInfo = document.getElementById('nowInfo');
            if (getInfo.code === '1'){
                nowInfo.innerText = getInfo.msg;
            }else {
                nowInfo.innerText = "获取失败";
            }

        }
    }
    req.open('GET','/api/nowInfo');
    req.send();
}
function get_user() {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState === 4) {
            var getInfo = JSON.parse(req.responseText);

            if (getInfo.code === '1') {
                divSwitch('user',getInfo.info)
            }else if(getInfo.code === '10'){
                divSwitch('free',{});
            }else {
                let ajax_info_box = $('.ajax_info_box');
                ajax_info_box.find('p.ajax_info_msg').text('获取失败');
                ajax_info_box.find('p.ajax_info_tips').text('稍等片刻或刷新重试');
                divSwitch('',{});
            }

        }
    }
    req.open('GET','/api/nowUser');
    req.send();
}
window.onload = function (){
    //get_status();
    divSwitch('',{});
    setInterval(get_user,5000);
}