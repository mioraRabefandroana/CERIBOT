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

        "C'est l'histoire de 2 patates qui traversent la route,. L’une d’elles se fait écraser. L’autre dit :, « Oh purée ! »",

        "Pourquoi les Geek sont-ils fiers ?,
        Parce qu'ils ont une Gygabyte. (Giga bite)",

        "Tu sais pourquoi l'iPhone 6 se plie ?,
        Parce que l'Apple Store.",

        "Pourquoi les geeks doivent-ils suivre une formation incendie ?,
        A cause des pare-feux.",

        "Quel Pokemon a une mitraillette ?,
        Ratatatatatatatatata",

        "A quoi sert Internet Explorer ?, 
        A télécharger Google Chrome",

        "Quand est ce que Windows ne bug pas ?,
        Quand l'ordinateur est éteint.", 

        "De quelle couleur sont tes yeux ?,
        #1292f4 et toi ?",

        "Les filles c'est comme les noms de domaine.,
        Celles que j'aime sont déjà prises. ",

        "Que dit une mère à son fils geek quand le diner est servi ?,
        Alt Tab !!!"
    ];

    $chosen = array_rand($jokes);
    return [
        "results"=> $jokes[$chosen]
    ];
}


