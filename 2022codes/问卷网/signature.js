function get_sign(s, appkey) {
    s = JSON.parse(s);
    var t ={}
    for (var key in s) {
    //将字典的键值对添加到JavaScript对象中
        t[key] = s[key];
    }

    var e = {
        appkey: appkey,
        web_site: (t && t.web_site ? t.web_site : "") || "wenjuan_web",
        // timestamp: (new Date).getTime()
    }
      , o = t || {};
    Object.assign(o, e);
    var n = Object.keys(o).sort()
      , i = [];
    console.log(o)



    return n.forEach((function(t) {
        ["secret", "__FORMDATA__"].includes(t) || i.push(o[t])
    }
    )),
    o.signature = l(i.join("") + "rltfin41xhvwjgyd75s8aq2oebm0369u")
    o
}

function getUuid(t, e) {
        var o = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split("")
          , n = [];

        if (e = e || o.length, t)
            for (var i = 0; i < t; i++)
                n[i] = o[0 | Math.random() * e];
        else {
            var r = null;
            n[8] = n[13] = n[18] = n[23] = "-",
            n[14] = "4";
            for (var l = 0; l < 36; l++)
                n[l] || (r = 0 | 16 * Math.random(),
                n[l] = o[19 === l ? 3 & r | 8 : r])
        }
        return n.join("")
}


function l(key){
    function s(t, e, r, n, i, o, s) {
            return a(e & r | ~e & n, t, e, i, o, s)
        }
    function u(t, e, r, n, i, o, s) {
            return a(e & n | r & ~n, t, e, i, o, s)
        }
    function h(t, e, r, n, i, o, s) {
            return a(e ^ r ^ n, t, e, i, o, s)
        }
    function f(t, e, r, n, i, o, s) {
            return a(r ^ (e | ~n), t, e, i, o, s)
        }
    function l(t, e) {
            var r, n, i, a, l;
            t[e >> 5] |= 128 << e % 32,
            t[14 + (e + 64 >>> 9 << 4)] = e;
            var c = 1732584193
              , d = -271733879
              , p = -1732584194
              , m = 271733878;
            for (r = 0; r < t.length; r += 16)
                n = c,
                i = d,
                a = p,
                l = m,
                c = s(c, d, p, m, t[r], 7, -680876936),
                m = s(m, c, d, p, t[r + 1], 12, -389564586),
                p = s(p, m, c, d, t[r + 2], 17, 606105819),
                d = s(d, p, m, c, t[r + 3], 22, -1044525330),
                c = s(c, d, p, m, t[r + 4], 7, -176418897),
                m = s(m, c, d, p, t[r + 5], 12, 1200080426),
                p = s(p, m, c, d, t[r + 6], 17, -1473231341),
                d = s(d, p, m, c, t[r + 7], 22, -45705983),
                c = s(c, d, p, m, t[r + 8], 7, 1770035416),
                m = s(m, c, d, p, t[r + 9], 12, -1958414417),
                p = s(p, m, c, d, t[r + 10], 17, -42063),
                d = s(d, p, m, c, t[r + 11], 22, -1990404162),
                c = s(c, d, p, m, t[r + 12], 7, 1804603682),
                m = s(m, c, d, p, t[r + 13], 12, -40341101),
                p = s(p, m, c, d, t[r + 14], 17, -1502002290),
                c = u(c, d = s(d, p, m, c, t[r + 15], 22, 1236535329), p, m, t[r + 1], 5, -165796510),
                m = u(m, c, d, p, t[r + 6], 9, -1069501632),
                p = u(p, m, c, d, t[r + 11], 14, 643717713),
                d = u(d, p, m, c, t[r], 20, -373897302),
                c = u(c, d, p, m, t[r + 5], 5, -701558691),
                m = u(m, c, d, p, t[r + 10], 9, 38016083),
                p = u(p, m, c, d, t[r + 15], 14, -660478335),
                d = u(d, p, m, c, t[r + 4], 20, -405537848),
                c = u(c, d, p, m, t[r + 9], 5, 568446438),
                m = u(m, c, d, p, t[r + 14], 9, -1019803690),
                p = u(p, m, c, d, t[r + 3], 14, -187363961),
                d = u(d, p, m, c, t[r + 8], 20, 1163531501),
                c = u(c, d, p, m, t[r + 13], 5, -1444681467),
                m = u(m, c, d, p, t[r + 2], 9, -51403784),
                p = u(p, m, c, d, t[r + 7], 14, 1735328473),
                c = h(c, d = u(d, p, m, c, t[r + 12], 20, -1926607734), p, m, t[r + 5], 4, -378558),
                m = h(m, c, d, p, t[r + 8], 11, -2022574463),
                p = h(p, m, c, d, t[r + 11], 16, 1839030562),
                d = h(d, p, m, c, t[r + 14], 23, -35309556),
                c = h(c, d, p, m, t[r + 1], 4, -1530992060),
                m = h(m, c, d, p, t[r + 4], 11, 1272893353),
                p = h(p, m, c, d, t[r + 7], 16, -155497632),
                d = h(d, p, m, c, t[r + 10], 23, -1094730640),
                c = h(c, d, p, m, t[r + 13], 4, 681279174),
                m = h(m, c, d, p, t[r], 11, -358537222),
                p = h(p, m, c, d, t[r + 3], 16, -722521979),
                d = h(d, p, m, c, t[r + 6], 23, 76029189),
                c = h(c, d, p, m, t[r + 9], 4, -640364487),
                m = h(m, c, d, p, t[r + 12], 11, -421815835),
                p = h(p, m, c, d, t[r + 15], 16, 530742520),
                c = f(c, d = h(d, p, m, c, t[r + 2], 23, -995338651), p, m, t[r], 6, -198630844),
                m = f(m, c, d, p, t[r + 7], 10, 1126891415),
                p = f(p, m, c, d, t[r + 14], 15, -1416354905),
                d = f(d, p, m, c, t[r + 5], 21, -57434055),
                c = f(c, d, p, m, t[r + 12], 6, 1700485571),
                m = f(m, c, d, p, t[r + 3], 10, -1894986606),
                p = f(p, m, c, d, t[r + 10], 15, -1051523),
                d = f(d, p, m, c, t[r + 1], 21, -2054922799),
                c = f(c, d, p, m, t[r + 8], 6, 1873313359),
                m = f(m, c, d, p, t[r + 15], 10, -30611744),
                p = f(p, m, c, d, t[r + 6], 15, -1560198380),
                d = f(d, p, m, c, t[r + 13], 21, 1309151649),
                c = f(c, d, p, m, t[r + 4], 6, -145523070),
                m = f(m, c, d, p, t[r + 11], 10, -1120210379),
                p = f(p, m, c, d, t[r + 2], 15, 718787259),
                d = f(d, p, m, c, t[r + 9], 21, -343485551),
                c = o(c, n),
                d = o(d, i),
                p = o(p, a),
                m = o(m, l);
            return [c, d, p, m]
        };
    function o(t, e) {
            var r = (65535 & t) + (65535 & e);
            return (t >> 16) + (e >> 16) + (r >> 16) << 16 | 65535 & r
        }
    function p(t) {
            var e, r, n = "0123456789abcdef", i = "";
            for (r = 0; r < t.length; r += 1)
                e = t.charCodeAt(r),
                i += n.charAt(e >>> 4 & 15) + n.charAt(15 & e);
            return i
        };
    function m(t) {
            return unescape(encodeURIComponent(t))
        };
    function v(t) {
            return function(t) {
                return c(l(d(t), 8 * t.length))
            }(m(t))
        };
    function d(t) {
            var e, r = [];
            for (r[(t.length >> 2) - 1] = void 0,
            e = 0; e < r.length; e += 1)
                r[e] = 0;
            var n = 8 * t.length;
            for (e = 0; e < n; e += 8)
                r[e >> 5] |= (255 & t.charCodeAt(e / 8)) << e % 32;
            return r
        }
    function a(t, e, r, n, i, a) {
            return o((s = o(o(e, t), o(n, a))) << (u = i) | s >>> 32 - u, r);
            var s, u
        }
    function c(t) {
            var e, r = "", n = 32 * t.length;
            for (e = 0; e < n; e += 8)
                r += String.fromCharCode(t[e >> 5] >>> e % 32 & 255);
            return r
        }
    function y(t,e,r){return e?r?g(e,t):p(g(e,t)):r?v(t):p(v(t))}

    function g(t, e) {
            return function(t, e) {
                var r, n, i = d(t), o = [], a = [];
                for (o[15] = a[15] = void 0,
                i.length > 16 && (i = l(i, 8 * t.length)),
                r = 0; r < 16; r += 1)
                    o[r] = 909522486 ^ i[r],
                    a[r] = 1549556828 ^ i[r];
                return n = l(o.concat(d(e)), 512 + 8 * e.length),
                c(l(a.concat(n), 640))
            }(m(t), m(e))
        }
    function y(t, e, r) {
            return e ? r ? g(e, t) : p(g(e, t)) : r ? v(t) : p(v(t))
        };
    return y(key)
}


// var t = {"data_type": "7,8","appkey": "sqjDmXVd5LNYf9r4", "web_site": "wenjuan_web", "timestamp": 1693680359201}

// var appkey = 'sqjDmXVd5LNYf9r4'
// console.log(get_sign(JSON.stringify(t), appkey))


console.log(getUuid())

// 2ea7c6bd88d188c8d9c37075c06072b5