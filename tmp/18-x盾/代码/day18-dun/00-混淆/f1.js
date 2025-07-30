var QC = Cf
  , K = arguments['length'] > 0x1 && void 0x0 !== arguments[0x1] ? arguments[0x1] : 0x0;
if (!Array[QC(0x784)](y))
    return y;
for (var T = {}, m = [], A = 0x0, O = y[QC(0x3ff)]; A < O; A++) {
    var L = y[A][K];
    null === L || void 0x0 === L || T[L] || (T[L] = !0x0,
    m[QC(0x31b)](y[A]));
}
return m;