<?php
    header('Content-Type: application/json; charset=utf-8');
    
    function getQuizz(){    
        $tabQuizz = array(

            array(
                "id"=>1,
                "question"=>"Quel est le langage informatique le plus couramment utilisé pour écrire les pages web ?",
                "choix"=>["HTML","HTTP","Java"],
                "reponse"=>"HTML (Hypertext Markup Language)"
            ),

            array(
                "id"=>2,
                "question"=>"Comment s’appelle la technique utilisée par les fraudeurs qui consiste à dérober vos informations personnelles (n° de carte de crédit, mots de passe, etc.) en se faisant passer pour votre banque via un courrier électronique ou un site web falsifié ?",
                "choix"=>["Le spamdexing","Le backdoor","Le phishing"],
                "reponse"=>"Le phishing"
            ),

            array(
                "id"=>3,
                "question"=>"Qu'est-ce qu'un CPU ?",
                "choix"=>["Un processeur","Une carte ,video","Un disque dur"],
                "reponse"=>"Un processeur"
            ),

            array(
                "id"=>4,
                "question"=>"Que signifie l'action Drag and Drop ?",
                "choix"=>["Copier/Coller","Couper/déposer","Glisser/déposer"],
                "reponse"=>"Glisser/déposer"
            ),

            array(
                "id"=>5, 
                "question"=>"Comment appelle-t-on l´écran de l’ordinateur ?",
                "choix"=>["L'unité centrale","Le CPU","Le moniteur"],
                "reponse"=>"Le moniteur"
            ),

            array(
                "id"=>6, 
                "question"=>"Que signifie wwww en informatique ?",
                "choix"=>["World Wide Wireless","World Wide Web","Rien du tout","Web World Widget"],
                "reponse"=>"tebgr"
            )
        );


        $quizzAleatoire = array_rand($tabQuizz);
        return $tabQuizz[$quizzAleatoire];
        
    }
    echo json_encode(getQuizz());

?>
