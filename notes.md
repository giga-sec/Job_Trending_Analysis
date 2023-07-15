## You can break down paths
So this is the full **Selector Path**:
-> `#mosaic-provider-jobcards > ul > li:nth-child(1)`

What we're going to do below is to separate the ul_element
While also *preserving ul_element* to get the li_element
```H
ul_element = browser.find_element(By.CSS_SELECTOR, "#mosaic-provider-jobcards > ul")
li_element = ul_element.find_element(By.CSS_SELECTOR, "li:nth-child(1)")
```


## In console, you can find element through using selector path
```H
document.querySelector("#mosaic-provider-jobcards > ul")
```

