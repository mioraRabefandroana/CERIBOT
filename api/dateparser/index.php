<?php
header('Content-Type: application/json; charset=utf-8');

$text = getTextValue();

if(!$text)
{
    echo json_encode(null);
    return;
}

$text = str_replace("'"," ", $text);

try{

    $command = "curl -XPOST http://localhost:8000/parse --data 'locale=fr_FR&text=\". $text .\"&dims=\"[\"time\"]'";

    exec($command, $output);

    $dateTime =  json_decode($output[0], true); 

    // print_r($dateTime[0]["value"]["values"][0]["value"]);

    $dateTime = $dateTime[0]["value"]["value"];

    $date = substr($dateTime, 0, 10);
    if(!$date)
    {
        echo json_encode(null);
        return;
    }
    $hour = substr($dateTime, 11, 5);

    $res = json_encode([
        "results" => [
            "date" => $date,
            "hour" => $hour
        ]
    ]);

    echo $res;
}
catch(Exception $e)
{
    echo json_encode(null);
}



/**
 * get text
 *  from json post or form-post or GET
 */
function getTextValue()
{
    try{        
        $text = json_decode(file_get_contents('php://input'), true)["text"];
        if(!$text)
            $text = $_POST["text"] ?? $_GET["text"];
        return $text;
    }
    catch(Exception $e)
    {
        return null;
    }
}