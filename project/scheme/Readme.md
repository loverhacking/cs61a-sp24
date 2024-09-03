## 测试
~~~
python ok --local
python ok --score --local 
python ok -q optional1 --local
python ok -q optional2 --local
~~~
Note: 对于 optional question1 需要找到能够进行尾递归的函数，将其对 `scheme_eval` 函数调用额外增加一个参数` True`。
* eval_all 
* do_if_form 
* do_and_form (此处参数值为 `True if expressions.rest is nil else False`)
* do_or_form (此处参数值为 `True if expressions.rest is nil else False`)