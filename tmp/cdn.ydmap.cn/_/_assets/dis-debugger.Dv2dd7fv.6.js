(()=>{
    if (typeof window > "u" || window.location.port)
        return;
    function o(n, r) {
        return Math.floor(Math.random() * (r - n)) + n
    }
    function t() {
        setInterval(()=>{
            const n = o(0, 100);
            (function() {
                return !1
            }
            ).constructor("\n          // 🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫 禁止调试 🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫\n          ".concat(Array.from({
                length: n
            }).fill("\n          ").join(""), "\n          \n        ")).call()
        }
        , 50)
    }
    try {
        t()
    } catch (n) {}
}
)();
