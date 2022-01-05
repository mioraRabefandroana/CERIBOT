<?php
header('Content-Type: application/json; charset=utf-8');

/** vérification d'un quizz */
$quizzId = $_GET["quizz"];
$reponse = $_GET["reponse"];
if($quizzId && $reponse)
{
    echo json_encode([
        "results" => verifyQuizz($quizzId, $reponse) 
    ]);
    return;
}


/** récuperation d'un quizz au hasard*/
echo json_encode([
    "results" => getQuizz()
]);

function getQuizz(){    
    
    $tabQuizz = getQuizzList();
    $quizzAleatoire = array_rand($tabQuizz);
    return $tabQuizz[$quizzAleatoire];    
}


function verifyQuizz($quizzId, $reponse)
{
    $tabQuizz = getQuizzList();
    $quizz = $tabQuizz[$quizzId];

    $reponse = clean($reponse);

    $reponseExact = $quizz["reponse"]." , ".$quizz["choix"][$quizz["reponse"]];

    if(is_null($reponse))
        return false;
    $juste = ($quizz && $quizz["reponse"] == $reponse);
    return [
        "juste" => $juste,
        "proposer" => $reponse,
        "reponse" => $reponseExact,
        "quizz" => $quizz
    ];
}

function clean($reponse)
{
    if(is_numeric($reponse))
        return $reponse;
    
    switch ($reponse) {
        case "un":
            return 1;
        case "deux":
            return 2;
        case "trois":
            return 3;
            break;
        case "quatre":
            return 4;
    }
    
    return null;
}

function getQuizzList()
{
    return [

        "1" => [
            "id" => 1,
            "question"=>"Quel est le langage informatique le plus couramment utilisé pour écrire les pages web ?",
            "choix"=>["HTML","HTTP","Java"],
            "reponse"=> 1
        ],

        "2" => [
            "id" => 2,
            "question"=>"Comment s’appelle la technique utilisée par les fraudeurs qui consiste à dérober vos informations personnelles (n° de carte de crédit, mots de passe, etc.) en se faisant passer pour votre banque via un courrier électronique ou un site web falsifié ?",
            "choix"=>["Le spamdexing","Le backdoor","Le phishing"],
            "reponse"=> 3
        ],

        "3" =>[
            "id" => 3,
            "question"=>"Qu'est-ce qu'un CPU ?",
            "choix"=>["Un processeur","Une carte ,video","Un disque dur"],
            "reponse"=> 1
        ],

        "4" =>[
            "id" => 4,
            "question"=>"Que signifie l'action Drag and Drop ?",
            "choix"=>["Copier/Coller","Couper/déposer","Glisser/déposer"],
            "reponse"=> 3
        ],

        "5" => [
            "id" => 5,
            "question"=>"Comment appelle-t-on l´écran de l’ordinateur ?",
            "choix"=>["L'unité centrale","Le CPU","Le moniteur"],
            "reponse"=> 3
        ],

        "6" => [ 
            "id" => 6,
            "question"=>"Que signifie wwww en informatique ?",
            "choix"=>["World Wide Wireless","World Wide Web","Rien du tout","Web World Widget"],
            "reponse"=> 2
        ]
    ];

}