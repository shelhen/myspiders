var navigator={
    appName:'Netscape',
    version:undefined,
    language:'zh-CN',
    browserLanguage:undefined,
    platform:'Win32',
    userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}
var window={
    screen: {width:1920,height:1080,colorDepth:24},
    history:{length:2}
}
var document= {
    referrer:'',
    domain:'www.sou.com'
}
var I3 = {
    utf8: {
        stringToBytes: function(e) {
            return I3.bin.stringToBytes(unescape(encodeURIComponent(e)))
        },
        bytesToString: function(e) {
            return decodeURIComponent(escape(I3.bin.bytesToString(e)))
        }
    },
    bin: {
        stringToBytes: function(e) {
            for (var t = [], r = 0; r < e.length; r++)
                t.push(e.charCodeAt(r) & 255);
            return t
        },
        bytesToString: function(e) {
            for (var t = [], r = 0; r < e.length; r++)
                t.push(String.fromCharCode(e[r]));
            return t.join("")
        }
    }
},lU = I3;
var xj, h_
(function() {
        var e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
            , t = {
            rotl: function(r, n) {
                return r << n | r >>> 32 - n
            },
            rotr: function(r, n) {
                return r << 32 - n | r >>> n
            },
            endian: function(r) {
                if (r.constructor == Number)
                    return t.rotl(r, 8) & 16711935 | t.rotl(r, 24) & 4278255360;
                for (var n = 0; n < r.length; n++)
                    r[n] = t.endian(r[n]);
                return r
            },
            randomBytes: function(r) {
                for (var n = []; r > 0; r--)
                    n.push(Math.floor(Math.random() * 256));
                return n
            },
            bytesToWords: function(r) {
                for (var n = [], u = 0, i = 0; u < r.length; u++,
                    i += 8)
                    n[i >>> 5] |= r[u] << 24 - i % 32;
                return n
            },
            wordsToBytes: function(r) {
                for (var n = [], u = 0; u < r.length * 32; u += 8)
                    n.push(r[u >>> 5] >>> 24 - u % 32 & 255);
                return n
            },
            bytesToHex: function(r) {
                for (var n = [], u = 0; u < r.length; u++)
                    n.push((r[u] >>> 4).toString(16)),
                        n.push((r[u] & 15).toString(16));
                return n.join("")
            },
            hexToBytes: function(r) {
                for (var n = [], u = 0; u < r.length; u += 2)
                    n.push(parseInt(r.substr(u, 2), 16));
                return n
            },
            bytesToBase64: function(r) {
                for (var n = [], u = 0; u < r.length; u += 3)
                    for (var i = r[u] << 16 | r[u + 1] << 8 | r[u + 2], o = 0; o < 4; o++)
                        u * 8 + o * 6 <= r.length * 8 ? n.push(e.charAt(i >>> 6 * (3 - o) & 63)) : n.push("=");
                return n.join("")
            },
            base64ToBytes: function(r) {
                r = r.replace(/[^A-Z0-9+\/]/ig, "");
                for (var n = [], u = 0, i = 0; u < r.length; i = ++u % 4)
                    i != 0 && n.push((e.indexOf(r.charAt(u - 1)) & Math.pow(2, -2 * i + 8) - 1) << i * 2 | e.indexOf(r.charAt(u)) >>> 6 - i * 2);
                return n
            }
        };
        xj= t
    }
)();
(function() {
        var e = xj
            , t = lU.utf8
            , r = Gye
            , n = lU.bin
            , u = function(i, o) {
            i.constructor == String ? o && o.encoding === "binary" ? i = n.stringToBytes(i) : i = t.stringToBytes(i) : r(i) ? i = Array.prototype.slice.call(i, 0) : !Array.isArray(i) && i.constructor !== Uint8Array && (i = i.toString());
            for (var s = e.bytesToWords(i), a = i.length * 8, l = 1732584193, A = -271733879, c = -1732584194, d = 271733878, f = 0; f < s.length; f++)
                s[f] = (s[f] << 8 | s[f] >>> 24) & 16711935 | (s[f] << 24 | s[f] >>> 8) & 4278255360;
            s[a >>> 5] |= 128 << a % 32,
                s[(a + 64 >>> 9 << 4) + 14] = a;
            for (var p = u._ff, h = u._gg, F = u._hh, C = u._ii, f = 0; f < s.length; f += 16) {
                var v = l
                    , E = A
                    , B = c
                    , x = d;
                l = p(l, A, c, d, s[f + 0], 7, -680876936),
                    d = p(d, l, A, c, s[f + 1], 12, -389564586),
                    c = p(c, d, l, A, s[f + 2], 17, 606105819),
                    A = p(A, c, d, l, s[f + 3], 22, -1044525330),
                    l = p(l, A, c, d, s[f + 4], 7, -176418897),
                    d = p(d, l, A, c, s[f + 5], 12, 1200080426),
                    c = p(c, d, l, A, s[f + 6], 17, -1473231341),
                    A = p(A, c, d, l, s[f + 7], 22, -45705983),
                    l = p(l, A, c, d, s[f + 8], 7, 1770035416),
                    d = p(d, l, A, c, s[f + 9], 12, -1958414417),
                    c = p(c, d, l, A, s[f + 10], 17, -42063),
                    A = p(A, c, d, l, s[f + 11], 22, -1990404162),
                    l = p(l, A, c, d, s[f + 12], 7, 1804603682),
                    d = p(d, l, A, c, s[f + 13], 12, -40341101),
                    c = p(c, d, l, A, s[f + 14], 17, -1502002290),
                    A = p(A, c, d, l, s[f + 15], 22, 1236535329),
                    l = h(l, A, c, d, s[f + 1], 5, -165796510),
                    d = h(d, l, A, c, s[f + 6], 9, -1069501632),
                    c = h(c, d, l, A, s[f + 11], 14, 643717713),
                    A = h(A, c, d, l, s[f + 0], 20, -373897302),
                    l = h(l, A, c, d, s[f + 5], 5, -701558691),
                    d = h(d, l, A, c, s[f + 10], 9, 38016083),
                    c = h(c, d, l, A, s[f + 15], 14, -660478335),
                    A = h(A, c, d, l, s[f + 4], 20, -405537848),
                    l = h(l, A, c, d, s[f + 9], 5, 568446438),
                    d = h(d, l, A, c, s[f + 14], 9, -1019803690),
                    c = h(c, d, l, A, s[f + 3], 14, -187363961),
                    A = h(A, c, d, l, s[f + 8], 20, 1163531501),
                    l = h(l, A, c, d, s[f + 13], 5, -1444681467),
                    d = h(d, l, A, c, s[f + 2], 9, -51403784),
                    c = h(c, d, l, A, s[f + 7], 14, 1735328473),
                    A = h(A, c, d, l, s[f + 12], 20, -1926607734),
                    l = F(l, A, c, d, s[f + 5], 4, -378558),
                    d = F(d, l, A, c, s[f + 8], 11, -2022574463),
                    c = F(c, d, l, A, s[f + 11], 16, 1839030562),
                    A = F(A, c, d, l, s[f + 14], 23, -35309556),
                    l = F(l, A, c, d, s[f + 1], 4, -1530992060),
                    d = F(d, l, A, c, s[f + 4], 11, 1272893353),
                    c = F(c, d, l, A, s[f + 7], 16, -155497632),
                    A = F(A, c, d, l, s[f + 10], 23, -1094730640),
                    l = F(l, A, c, d, s[f + 13], 4, 681279174),
                    d = F(d, l, A, c, s[f + 0], 11, -358537222),
                    c = F(c, d, l, A, s[f + 3], 16, -722521979),
                    A = F(A, c, d, l, s[f + 6], 23, 76029189),
                    l = F(l, A, c, d, s[f + 9], 4, -640364487),
                    d = F(d, l, A, c, s[f + 12], 11, -421815835),
                    c = F(c, d, l, A, s[f + 15], 16, 530742520),
                    A = F(A, c, d, l, s[f + 2], 23, -995338651),
                    l = C(l, A, c, d, s[f + 0], 6, -198630844),
                    d = C(d, l, A, c, s[f + 7], 10, 1126891415),
                    c = C(c, d, l, A, s[f + 14], 15, -1416354905),
                    A = C(A, c, d, l, s[f + 5], 21, -57434055),
                    l = C(l, A, c, d, s[f + 12], 6, 1700485571),
                    d = C(d, l, A, c, s[f + 3], 10, -1894986606),
                    c = C(c, d, l, A, s[f + 10], 15, -1051523),
                    A = C(A, c, d, l, s[f + 1], 21, -2054922799),
                    l = C(l, A, c, d, s[f + 8], 6, 1873313359),
                    d = C(d, l, A, c, s[f + 15], 10, -30611744),
                    c = C(c, d, l, A, s[f + 6], 15, -1560198380),
                    A = C(A, c, d, l, s[f + 13], 21, 1309151649),
                    l = C(l, A, c, d, s[f + 4], 6, -145523070),
                    d = C(d, l, A, c, s[f + 11], 10, -1120210379),
                    c = C(c, d, l, A, s[f + 2], 15, 718787259),
                    A = C(A, c, d, l, s[f + 9], 21, -343485551),
                    l = l + v >>> 0,
                    A = A + E >>> 0,
                    c = c + B >>> 0,
                    d = d + x >>> 0
            }
            return e.endian([l, A, c, d])
        };
        u._ff = function(i, o, s, a, l, A, c) {
            var d = i + (o & s | ~o & a) + (l >>> 0) + c;
            return (d << A | d >>> 32 - A) + o
        }
            ,
            u._gg = function(i, o, s, a, l, A, c) {
                var d = i + (o & a | s & ~a) + (l >>> 0) + c;
                return (d << A | d >>> 32 - A) + o
            }
            ,
            u._hh = function(i, o, s, a, l, A, c) {
                var d = i + (o ^ s ^ a) + (l >>> 0) + c;
                return (d << A | d >>> 32 - A) + o
            }
            ,
            u._ii = function(i, o, s, a, l, A, c) {
                var d = i + (s ^ (o | ~a)) + (l >>> 0) + c;
                return (d << A | d >>> 32 - A) + o
            }
            ,
            u._blocksize = 16,
            u._digestsize = 16,
            h_ = function(i, o) {
                if (i == null)
                    throw new Error("Illegal argument " + i);
                var s = e.wordsToBytes(u(i, o));
                return o && o.asBytes ? s : o && o.asString ? n.bytesToString(s) : e.bytesToHex(s)
            }
    }
)();
var Gye = function(e) {
    return e != null && (yj(e) || qye(e) || !!e._isBuffer)
};
function yj(e) {
    return !!e.constructor && typeof e.constructor.isBuffer == "function" && e.constructor.isBuffer(e)
}
function qye(e) {
    return typeof e.readFloatLE == "function" && typeof e.slice == "function" && yj(e.slice(0, 0))
}

function hash(t) {
    for (var e = 0, r = 0, a = t.length - 1; a >= 0; a--) {
        var i = parseInt(t.charCodeAt(a), 10);
        0 != (r = 266338304 & (e = (e << 6 & 268435455) + i + (i << 14))) && (e ^= r >> 21)
    }
    return e
}
function guid() {
    for (var t = [navigator.appName, navigator.version, navigator.language || navigator.browserLanguage,
        navigator.platform, navigator.userAgent,
        window.screen.width, "x", window.screen.height, window.screen.colorDepth, document.referrer].join(""), e = t.length, r = window.history.length; r; )
        t += r-- ^ e++;
    return 2147483647 * (Math.round(2147483647 * Math.random()) ^ hash(t))
}
function getISO8601Time(){
    var e = new Date
    let t = e.getHours() + 8;
    return e.setHours(t), new Date(e).toISOString().replace(/\.[\d]{3}Z/, "+08:00")
}
function getMid(){
    let i = [hash(document.domain), guid(), +new Date + Math.random() + Math.random()].join("")
    return i.replace(/\./gi, "e").substr(0, 32)
}
function get_zm_token(isotime, mid, ua_hash){
    let e = ["Web", isotime, "1.2", mid, ua_hash]
    return h_(e.join(""))
}
mid = getMid()
isotime = getISO8601Time()
ua = navigator.userAgent
ua_hash = h_(navigator.userAgent)
zm_token = get_zm_token(isotime, mid, ua_hash)

console.log(mid)
console.log(isotime)
console.log(ua_hash)
console.log(zm_token)
