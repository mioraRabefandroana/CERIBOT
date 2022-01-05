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
    $hour = substr($dateTime, 11, 5);

    $hours = [];
    if(!$hour)
    {
        $hours0 = json_decode($output[0], true)[0]["value"]["values"];
        foreach($hours0 as $dt)
        {
            $h = substr($dt["from"]["value"], 11, 5) ;
            $hours[] = $h;

            // $date = ($date) ? $date : substr($dt["from"]["value"], 0, 10);
        }
        $hours = array_unique($hours);
    }
    

    $res = json_encode([
        "results" => [
            "date" => $date,
            "hour" => $hour,
            "hours" =>  $hours
        ]
    ]);

    echo $res;
}
catch(Exception $e)
{
    echo json_encode('strval($output)');
//    echo json_encode(null);
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
