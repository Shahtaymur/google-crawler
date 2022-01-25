<?php
$_GET = array();
foreach($argv as $key => $pair) {
    if ($key == 0) { //skip first element which is script name (test.php)
        continue;
    }

    list($key, $value) = explode(":", $pair);
    $_GET[$key] = $value;
}

$proxies = array();
$handle = fopen("proxies.txt", "r");
if ($handle) {
    while (($line = fgets($handle)) !== false) {
        array_push($proxies,preg_replace( "/\r|\n/", "", $line ));
    }

    fclose($handle);
} else {
    // error opening the file.
} 

$q = $_GET['keyword'];

$q = urlencode($q);

$url = "https://www.google.com/search?q=$q&gl=pk&hl=en";
$proxy = $proxies[array_rand($proxies)];
$PROXY_USER = "geonode_uMZlIrin1i";
$PROXY_PASS = "b35b456b-90f7-4d88-88c4-b1bae00143a6";
$proxyauth = "$PROXY_USER:$PROXY_PASS";
$headers = [
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'accept-language: en-US',
    'scheme: https'
];

do{
    $ch = curl_init();
    $proxy = $proxies[array_rand($proxies)];
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_PROXY, $proxy);
    curl_setopt($ch, CURLOPT_PROXYUSERPWD, $proxyauth);
    curl_setopt($ch, CURLOPT_AUTOREFERER, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    //curl_setopt($ch, CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36');
    $curl_scraped_page = curl_exec($ch);
} while(curl_getinfo($ch,CURLINFO_HTTP_CODE) != 200);
echo $curl_scraped_page;
curl_close($ch);
?>