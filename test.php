<?php
// $_GET = array();
// foreach($argv as $key => $pair) {
//     if ($key == 0) { //skip first element which is script name (test.php)
//         continue;
//     }

//     list($key, $value) = explode(":", $pair);
//     $_GET[$key] = $value;
// }

// $proxies = array();
// $handle = fopen("proxies.txt", "r");
// if ($handle) {
//     while (($line = fgets($handle)) !== false) {
//         array_push($proxies,preg_replace( "/\r|\n/", "", $line ));
//     }

//     fclose($handle);
// } else {
//     // error opening the file.
// } 

// $q = $_GET['keyword'];

// $q = urlencode($q);

// $url = "https://www.google.com/search?q=$q&gl=pk&hl=en";
// $proxy = $proxies[array_rand($proxies)];
// $PROXY_USER = "geonode_uMZlIrin1i";
// $PROXY_PASS = "b35b456b-90f7-4d88-88c4-b1bae00143a6";
// $proxyauth = "$PROXY_USER:$PROXY_PASS";
// $headers = [
//     'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
//     'accept-language: en-US',
//     'scheme: https'
// ];

// do{
//     $ch = curl_init();
//     $proxy = $proxies[array_rand($proxies)];
//     curl_setopt($ch, CURLOPT_URL, $url);
//     curl_setopt($ch, CURLOPT_PROXY, $proxy);
//     curl_setopt($ch, CURLOPT_PROXYUSERPWD, $proxyauth);
//     curl_setopt($ch, CURLOPT_AUTOREFERER, true);
//     curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//     curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
//     curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
//     curl_setopt($ch, CURLOPT_HEADER, 1);
//     curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
//     //curl_setopt($ch, CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36');
//     $curl_scraped_page = curl_exec($ch);
// } while(curl_getinfo($ch,CURLINFO_HTTP_CODE) != 200);
// echo $curl_scraped_page;
// curl_close($ch);
//require_once __DIR__ . '/./vendor/autoload.php';
include("simple_html_dom.php");
$obj = new GoogleScraper('car');

$arr=$obj->getUrlList(urlencode('car'),'');
echo date('Y-m-d');
print_r($arr);
?>

<?php

class GoogleScraper
{
    var $keyword    = "";
    var $urlList    = array();
    var $time1      = 4000000;
    var $time2      = 8000000;
    var $proxy      = "";
    var $cookie     = "";
    var $header     = "";
    var $ei         = "";
    var $ved        = "";


    function __construct($keyword) {
        $this->keyword = $keyword;
        $this->cookie = tempnam ("/tmp", "cookie");
        $this->headers[] = "Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5";
        $this->headers[] = "Connection: keep-alive";
        $this->headers[] = "Keep-Alive: 115";
        $this->headers[] = "Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7";
        $this->headers[] = "Accept-Language: en-us,en;q=0.5";
        $this->headers[] = "Pragma: ";
    }

    function getpagedata($url)
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36');
        curl_setopt($ch, CURLOPT_ENCODING, 'gzip,deflate');
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->headers);
        curl_setopt($ch, CURLOPT_COOKIEFILE,  $this->cookie);
        curl_setopt($ch, CURLOPT_COOKIEJAR,  $this->cookie);
        curl_setopt($ch, CURLOPT_PROXY, $this->proxy);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
        $data=curl_exec($ch);
        curl_close($ch);
        return $data;
    }

    function pause() {
        usleep(rand($this->time1,$this->time2));
    }

    function fetchUrlList()
    {
        $url  = 'https://www.google.com/search?hl=en&tbo=d&site=&source=hp&q='.$this->keyword.'&oq='.$this->keyword.'';

        print $url."<br>";

        $html = file_get_html($url);

        $i=0;
        $linkObjs = $html->find('h3.r a'); 
        foreach ($linkObjs as $linkObj) {
            $title = trim($linkObj->plaintext);
            $link  = trim($linkObj->href);

            // if it is not a direct link but url reference found inside it, then extract
            if (!preg_match('/^https?/', $link) && preg_match('/q=(.+)&amp;sa=/U', $link, $matches) && preg_match('/^https?/', $matches[1])) {
                $link = $matches[1];
            } else if (!preg_match('/^https?/', $link)) { // skip if it is not a valid link
                continue;
            }

            $descr = $html->find('span.st',$i); // description is not a child element of H3 thereforce we use a counter and recheck.
            $i++;   
            echo '<p>Title: ' . $title . '<br />';
            echo 'Link: ' . $link . '<br />';
            echo 'Description: ' . $descr . '</p>';
        }
    }

    function getUrlList($keyword,$proxy='') {
        $this->keyword=$keyword;
        $this->proxy=$proxy;
        $this->pause();
        $this->fetchUrlList();
        return $this->urlList;
    }
}