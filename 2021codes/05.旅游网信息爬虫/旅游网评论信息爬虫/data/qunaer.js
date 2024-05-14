
function hashCode(e) {
    var t = 0, n, r, i;
    e = "" + e;
    for (n = 0, i = e.length; n < i; n++) {
        r = e.charCodeAt(n);
        t = (t << 5) - t + r;
        t |= 0
    }
    return t
}
function generateUUID(){
    function e() {
        return ((1 + Math.random()) * 65536 | 0).toString(16).substring(1)
    }
    return e() + e()
}
function _initUserKey(QN,QG) {
    // 假设QN2为null
    var e = QN||QG||null|| generateUUID();
    e = hashCode(e);
    if (e < 0) {
        e = "0" + (0 - e)
    } else {
        e = "" + e
    }
    return e
}



