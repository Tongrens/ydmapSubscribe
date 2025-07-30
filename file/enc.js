var i = 0;
function r(e) {
    return a(o(s(e)))
}
function o(e) {
    return u(c(l(e), 8 * e.length))
}
function a(e) {
    for (var t, n = i ? "0123456789ABCDEF" : "0123456789abcdef", r = "", o = 0; o < e.length; o++)
        t = e.charCodeAt(o),
        r += n.charAt(t >>> 4 & 15) + n.charAt(15 & t);
    return r
}
function s(e) {
    var t, n, i = "", r = -1;
    while (++r < e.length)
        t = e.charCodeAt(r),
        n = r + 1 < e.length ? e.charCodeAt(r + 1) : 0,
        55296 <= t && t <= 56319 && 56320 <= n && n <= 57343 && (t = 65536 + ((1023 & t) << 10) + (1023 & n),
        r++),
        t <= 127 ? i += String.fromCharCode(t) : t <= 2047 ? i += String.fromCharCode(192 | t >>> 6 & 31, 128 | 63 & t) : t <= 65535 ? i += String.fromCharCode(224 | t >>> 12 & 15, 128 | t >>> 6 & 63, 128 | 63 & t) : t <= 2097151 && (i += String.fromCharCode(240 | t >>> 18 & 7, 128 | t >>> 12 & 63, 128 | t >>> 6 & 63, 128 | 63 & t));
    return i
}
function l(e) {
    for (var t = Array(e.length >> 2), n = 0; n < t.length; n++)
        t[n] = 0;
    for (n = 0; n < 8 * e.length; n += 8)
        t[n >> 5] |= (255 & e.charCodeAt(n / 8)) << n % 32;
    return t
}
function u(e) {
    for (var t = "", n = 0; n < 32 * e.length; n += 8)
        t += String.fromCharCode(e[n >> 5] >>> n % 32 & 255);
    return t
}
function c(e, t) {
    e[t >> 5] |= 128 << t % 32,
    e[14 + (t + 64 >>> 9 << 4)] = t;
    for (var n = 1732584193, i = -271733879, r = -1732584194, o = 271733878, a = 0; a < e.length; a += 16) {
        var s = n
          , l = i
          , u = r
          , c = o;
        n = h(n, i, r, o, e[a + 0], 7, -680876936),
        o = h(o, n, i, r, e[a + 1], 12, -389564586),
        r = h(r, o, n, i, e[a + 2], 17, 606105819),
        i = h(i, r, o, n, e[a + 3], 22, -1044525330),
        n = h(n, i, r, o, e[a + 4], 7, -176418897),
        o = h(o, n, i, r, e[a + 5], 12, 1200080426),
        r = h(r, o, n, i, e[a + 6], 17, -1473231341),
        i = h(i, r, o, n, e[a + 7], 22, -45705983),
        n = h(n, i, r, o, e[a + 8], 7, 1770035416),
        o = h(o, n, i, r, e[a + 9], 12, -1958414417),
        r = h(r, o, n, i, e[a + 10], 17, -42063),
        i = h(i, r, o, n, e[a + 11], 22, -1990404162),
        n = h(n, i, r, o, e[a + 12], 7, 1804603682),
        o = h(o, n, i, r, e[a + 13], 12, -40341101),
        r = h(r, o, n, i, e[a + 14], 17, -1502002290),
        i = h(i, r, o, n, e[a + 15], 22, 1236535329),
        n = f(n, i, r, o, e[a + 1], 5, -165796510),
        o = f(o, n, i, r, e[a + 6], 9, -1069501632),
        r = f(r, o, n, i, e[a + 11], 14, 643717713),
        i = f(i, r, o, n, e[a + 0], 20, -373897302),
        n = f(n, i, r, o, e[a + 5], 5, -701558691),
        o = f(o, n, i, r, e[a + 10], 9, 38016083),
        r = f(r, o, n, i, e[a + 15], 14, -660478335),
        i = f(i, r, o, n, e[a + 4], 20, -405537848),
        n = f(n, i, r, o, e[a + 9], 5, 568446438),
        o = f(o, n, i, r, e[a + 14], 9, -1019803690),
        r = f(r, o, n, i, e[a + 3], 14, -187363961),
        i = f(i, r, o, n, e[a + 8], 20, 1163531501),
        n = f(n, i, r, o, e[a + 13], 5, -1444681467),
        o = f(o, n, i, r, e[a + 2], 9, -51403784),
        r = f(r, o, n, i, e[a + 7], 14, 1735328473),
        i = f(i, r, o, n, e[a + 12], 20, -1926607734),
        n = p(n, i, r, o, e[a + 5], 4, -378558),
        o = p(o, n, i, r, e[a + 8], 11, -2022574463),
        r = p(r, o, n, i, e[a + 11], 16, 1839030562),
        i = p(i, r, o, n, e[a + 14], 23, -35309556),
        n = p(n, i, r, o, e[a + 1], 4, -1530992060),
        o = p(o, n, i, r, e[a + 4], 11, 1272893353),
        r = p(r, o, n, i, e[a + 7], 16, -155497632),
        i = p(i, r, o, n, e[a + 10], 23, -1094730640),
        n = p(n, i, r, o, e[a + 13], 4, 681279174),
        o = p(o, n, i, r, e[a + 0], 11, -358537222),
        r = p(r, o, n, i, e[a + 3], 16, -722521979),
        i = p(i, r, o, n, e[a + 6], 23, 76029189),
        n = p(n, i, r, o, e[a + 9], 4, -640364487),
        o = p(o, n, i, r, e[a + 12], 11, -421815835),
        r = p(r, o, n, i, e[a + 15], 16, 530742520),
        i = p(i, r, o, n, e[a + 2], 23, -995338651),
        n = m(n, i, r, o, e[a + 0], 6, -198630844),
        o = m(o, n, i, r, e[a + 7], 10, 1126891415),
        r = m(r, o, n, i, e[a + 14], 15, -1416354905),
        i = m(i, r, o, n, e[a + 5], 21, -57434055),
        n = m(n, i, r, o, e[a + 12], 6, 1700485571),
        o = m(o, n, i, r, e[a + 3], 10, -1894986606),
        r = m(r, o, n, i, e[a + 10], 15, -1051523),
        i = m(i, r, o, n, e[a + 1], 21, -2054922799),
        n = m(n, i, r, o, e[a + 8], 6, 1873313359),
        o = m(o, n, i, r, e[a + 15], 10, -30611744),
        r = m(r, o, n, i, e[a + 6], 15, -1560198380),
        i = m(i, r, o, n, e[a + 13], 21, 1309151649),
        n = m(n, i, r, o, e[a + 4], 6, -145523070),
        o = m(o, n, i, r, e[a + 11], 10, -1120210379),
        r = m(r, o, n, i, e[a + 2], 15, 718787259),
        i = m(i, r, o, n, e[a + 9], 21, -343485551),
        n = v(n, s),
        i = v(i, l),
        r = v(r, u),
        o = v(o, c)
    }
    return Array(n, i, r, o)
}
function d(e, t, n, i, r, o) {
    return v(g(v(v(t, e), v(i, o)), r), n)
}
function h(e, t, n, i, r, o, a) {
    return d(t & n | ~t & i, e, t, r, o, a)
}
function f(e, t, n, i, r, o, a) {
    return d(t & i | n & ~i, e, t, r, o, a)
}
function p(e, t, n, i, r, o, a) {
    return d(t ^ n ^ i, e, t, r, o, a)
}
function m(e, t, n, i, r, o, a) {
    return d(n ^ (t | ~i), e, t, r, o, a)
}
function v(e, t) {
    var n = (65535 & e) + (65535 & t)
      , i = (e >> 16) + (t >> 16) + (n >> 16);
    return i << 16 | 65535 & n
}
function g(e, t) {
    return e << t | e >>> 32 - t
}
function y(e) {
    return r(e)
}