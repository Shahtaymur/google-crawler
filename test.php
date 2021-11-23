<?php

$url = 'https://www.google.com/search?q=how+to';
$proxy = 'rotating-residential.geonode.com:9000';
$proxyauth = 'geonode_uMZlIrin1i:b35b456b-90f7-4d88-88c4-b1bae00143a6';
do{
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_PROXY, $proxy);
    curl_setopt($ch, CURLOPT_PROXYUSERPWD, $proxyauth);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36");
    $curl_scraped_page = curl_exec($ch);
    
    echo curl_getinfo($ch,CURLINFO_HTTP_CODE);
    echo "\n";
 
    if (curl_getinfo($ch,CURLINFO_HTTP_CODE) == 302 && preg_match('~Location: (.*)~i', $curl_scraped_page, $match)) {
        $url = trim($match[1]);
        echo $url;
    }
} while(curl_getinfo($ch,CURLINFO_HTTP_CODE) != 200);
// echo $curl_scraped_page;
curl_close($ch);

?>