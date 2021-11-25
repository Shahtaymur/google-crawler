<?php

$url = 'https://www.google.com/';
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
    $google_page = curl_exec($ch);
    
    echo curl_getinfo($ch,CURLINFO_HTTP_CODE) . "\t" . $url . "\n";

 
    // if (curl_getinfo($ch,CURLINFO_HTTP_CODE) == 302 && preg_match('~Location: (.*)~i', $curl_scraped_page, $match)) {
    //     $url = trim($match[1]);
    //     echo $url;
    // }
} while(curl_getinfo($ch,CURLINFO_HTTP_CODE) != 200);
file_put_contents("test.html",$google_page);
preg_match('/<input value="(.*?)" name="ei" type="hidden">/is', $google_page, $ei_matches);
preg_match('/name="ei" type="hidden"><input value="(.*?)" name="iflsig" type="hidden">/is', $google_page, $iflsig_matches);
preg_match('/style> <center> <input .*? name="btnK" type="submit" data-ved="(.*?)">/is', $google_page, $ved_matches);

// print_r($ved_matches);exit;

$ei = $ei_matches[1];
$iflsig = $iflsig_matches[1];
$ved = $ved_matches[1];

$q = "how to code";
$q = urlencode($q);
$url = "https://www.google.com/search?q=$q&source=hp&ei=$ei&iflsig=$iflsig&ved=$ved&uact=5&oq=$q&sclient=gws-wiz";
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
    
    echo curl_getinfo($ch,CURLINFO_HTTP_CODE) . "\t" . $url . "\n";
 
    if (preg_match('~Location: (.*)~i', $curl_scraped_page, $match)) {
        $url = trim($match[1]);
        echo $url;
    }
} while(curl_getinfo($ch,CURLINFO_HTTP_CODE) != 200);
echo $curl_scraped_page;
curl_close($ch);

?>