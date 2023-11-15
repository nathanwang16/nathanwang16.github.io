
var binft = function (r) {
    var isTransparent = true;
    function getRandomColor() {
        if(isTransparent){
            isTransparent = false;
            //此处修改字体颜色,最后的 0 和 1 不要改
            return "rgba(255,255,255,0)"
        }else{
            isTransparent = true;
            return "rgba(255,255,255,1)"
        }
    }  
    function n(r) {
        for (var n = document.createDocumentFragment(), i = 0; r > i; i++) {
            var oneword = document.createElement("span");
            oneword.textContent = "_"; // 此处是末尾字符,如果想用光标样式可以改为"|"
            oneword.style.color = getRandomColor();
            n.appendChild(oneword);
        }
        return n
    }
    function i() {
        var t = wordList[c.skillI];
        c.step ? c.step-- : (c.step = refreshDelayTime, c.prefixP < l.length ? (c.prefixP >= 0 && (c.text += l[c.prefixP]), c.prefixP++) : "forward" === c.direction ? c.skillP < t.length ? (c.text += t[c.skillP], c.skillP++) : c.delay ? c.delay-- : (c.direction = "backward", c.delay = showTotalWordDelayTime) : c.skillP > 0 ? (c.text = c.text.slice(0, -1), c.skillP--) : (c.skillI = (c.skillI + 1) % wordList.length, c.direction = "forward")), r.textContent = c.text, r.appendChild(n(c.prefixP < l.length ? Math.min(maxLength, maxLength + c.prefixP) : Math.min(maxLength, t.length - c.skillP))), setTimeout(i, d)
    }
    var l = "",
    //此处改成你自己的诗词
    wordList = [ 
            
            "A Calling Forth",
            "面朝大海，春暖花开。",
            "Carpe Diem!",
            "流尽了最后一滴血 用筋骨还能飞奔一千里",
            "风可以吹起一张白纸，却无法吹走一只蝴蝶，因为生命的力量在于不顺从。",
            "The Only Way Out Is All In",
            "为什么我眼中常含泪水, 因为我对这土地爱得深沉...",
            "Golden Spirit!",
            "心不需要鞘。",
            "The smallest sprout shows there is really no death, And if ever there was it led forward life, and does not wait at the end to arrest it,",
            "我们不吝啬生命，但有求于生命，热爱生命。",
            "Asking Why lets you know the world, Asking Why Not lets you change the world.",
            "消失了，消失了你骄傲的足音！",
            "All goes onward and outward, and nothing collapses,",
            "莫听穿林打叶声,何妨吟啸且徐行.",
            "Still Lying in the backseat, clutching one small hand.",
            "不要哀求，学会争取；若能如此，终有所获。",
            "原来醉着走才最飘逸，这富有韧性的飘逸使我终于感到了我自己。",

        ].map(function (r) {
    return r + ""
    }),
    showTotalWordDelayTime = 15,
    refreshDelayTime = 1,
    maxLength = 1,
    d = 30,
    c = {
        text: "",
        prefixP: -maxLength,
        skillI: 0,
        skillP: 0,
        direction: "forward",
        delay: showTotalWordDelayTime,
        step: refreshDelayTime
    };
    i()
};
binft(document.getElementById('binft'));