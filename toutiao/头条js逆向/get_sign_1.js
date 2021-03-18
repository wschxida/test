// i = {url:'https://so.toutiao.com/search?keyword=%E5%8D%81%E5%9B%9B%E4%BA%94%E8%A7%84%E5%88%92%E7%BA%B2%E8%A6%81&pd=weitoutiao&source=search_subtab_switch&original_source=&in_ogs=&from=weitoutiao'};
i = {url:process.argv[2]};
a = require('./sign.js');
n = a.sign;
console.log(n.call(a,i));