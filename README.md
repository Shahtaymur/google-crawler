# google-crawler
This is a python and flask based get api of google search engine. it will scrape the search retsult and back to you in json.
run the project using run the following file `crawl.py` and run the folling url in browser or postman.
<pre>
http://127.0.0.1:5000/search?q=apple
</pre>
  <h3>Required Parameter (your search keyword)</h3>
  <ul>
    <li>q</li>
  </ul>
  <h3>Optional Parameter with yes|no (by default no)</h3>
  <ul>
    <li>faqs</li>
    <li>r_cache</li>
  </ul>
  <h4>Crawl - Topics</h3>
  <ol>
    <li>links</li>
    <li>meta description</li>
    <li>top sights</li>
    <li>knowledge panel</li>
    <li>dictionary</li>
    <li>organic</li>
    <li>related search</li>
    <li>feature snippet</li>
    <li>direct answer</li>
    <li>unit converter</li>
  </ol>

  <h5>Required packegs</h4>
  <ul>
    <li>pip install fake_useragent</li>
    <li>pip install flask</li>
    <li>pip install flask_restful</li>
    <li>pip install pandas</li>
    <li>pip install requests</li>
    <li>pip install beautifulsoup4</li>
  </ul>
