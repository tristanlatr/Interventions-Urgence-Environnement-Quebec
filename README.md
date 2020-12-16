# Liste des Interventions d'Urgence Environnement Quebec

![Excel Sample](screens/sample.png "Liste des Interventions d'Urgence Environnement Quebec (Excel)")

Beta 🚧  

Ce logiciel génère et met à votre disposition un fichier Excel (ainsi que JSON) contenant toute les informations du registre des interventions d'Urgence-Environnement Québec. Le fichier est actualisé tous les jours. 

[Cliquez ici pour le télécharger](https://github.com/tristanlatr/Interventions-Urgence-Environnement-Quebec/raw/main/Data/InterventionsUrgenceEnvironnementQuebec.json.xlsx) ou naviguez vers le répertoire "Data".

Les données sont aquises via "web scraping" depuis le site web d'[Urgence-Environnement](http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/archive.asp).

Note: Les informations font l'objet d'un traitement ultérieur. 
- Le contenu des dossiers du registre est comparées à une liste de mots clés fréquemments vues. 
- Les information de locatisation (Latitude, Longitude et Geocoder_Infos) sont ajoutés avec l'API de [Bing](https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/?redirectedfrom=MSDN). 

Disclamer : Il s'agit d'un projet NON OFFICIEL et n'est PAS sponsorisé ou soutenu par le gouvernement du Québec ou Urgence-Environnement. 

---

This software generates and upload an Excel file (also JSON) containing all information from the Registre des interventions d'Urgence-Environnement Québec. The file is updated every day.

[Click here to download it](https://github.com/tristanlatr/Interventions-Urgence-Environnement-Quebec/raw/main/Data/InterventionsUrgenceEnvironnementQuebec.json.xlsx) or browse to the "Data" directory.

Data is gathered by scaping the website of [Urgence-Environnement](http://www.environnement.gouv.qc.ca/ministere/urgence_environnement/archive.asp).

Note: Further processing is applied to the informations. 
 - The contents of the registry folders are compared to a list of frequently seen keywords. 
 - Coordinates are added (Latitude, Longitude and Geocoder_Infos) with [Bing](https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/?redirectedfrom=MSDN)'s API. 

Disclamer: This is an UNOFFICIAL project and is NOT sponsored or supported by the Govnerment of Quebec or Urgence-Environnement. 
