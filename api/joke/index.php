<?php
header('Content-Type: application/json; charset=utf-8');
echo json_encode(getJoke());



function getJoke()
{
    $jokes = [
        "J'ai une blague sur les magasins,.
        Mais elle a pas supermarché",

        "Deux lions discutent,
        « T’as une belle crinière »,        
        « Arrête. tu vas me faire rugir »",

        "Que dit une imprimante dans l'eau ?,
        J’ai papier!",

        "Quel est le super héros qui a tout le temps peur ?,
        Le super-sticieux",

        "C'est l'histoire de 2 patates qui traversent la route,. L’une d’elles se fait écraser. L’autre dit :, « Oh purée ! »"
    ];

    $chosen = array_rand($jokes);
    return [
        "results"=> $jokes[$chosen]
    ];
}


