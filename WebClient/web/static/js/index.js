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
            var nowUser = document.getElementById('nowUser');

            if (getInfo.code === '1') {
                nowUser.innerText = "序号：" + getInfo.info.num + " ID：" + getInfo.info.id;
            }else if(getInfo.code === '10'){
                nowUser.innerText = '队列当前无用户';
            }else {
                nowUser.innerText = "获取失败";
            }

        }
    }
    req.open('GET','/api/nowUser');
    req.send();
}
window.onload = function (){
    get_status();
    get_user();
}