 b = $("qun-created");
 
 b.innerHTML = genDateStr(new Date(qunInfo.gCrtTime * 1E3));
 
 function genDateStr(a, b) {
 
    b = b || "-";
 
    return a.getFullYear() + b 
           + String(a.getMonth() + 101).substring(1) + b 
           + String(a.getDate() + 100).substring(1);
}
