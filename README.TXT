**********************************    README    **********************************


- Organisation du Programme: 


Nous avons organisé le programme en 4 parties : 


        Une première qui contient les imports de fonctions venant d'autres programmes
et les bibliothèques Python. Nous les mettons en tout premier afin d'être sûr de les 
avoir avant l'utilisation de l'une d'entre elles


        Une deuxième qui contient les Fonctions nécessaires à l'exécution du 
programme et créées par nous-même. Cela permet de ne pas se perdre dans le code 
lorsque l'on cherche une fonction à modifier ou consulter. 


        Une troisième contenant toutes les valeurs utilisées dans l'exécution du jeu.
Nous avons décidé de toutes les mettre ensemble afin qu’elles soient bien lisibles et séparées de la partie dédiée à l’exécution du code. De cette manière, elles sont aisément modifiables, on peut en ajouter facilement et aller les consulter rapidement. 


        Et enfin la dernière, dédiée à l'exécution. Elle est elle-même divisée en trois parties: 
* La première dédiée à la création de la partie, où il y a l’input pour le nombre de parties que les joueurs choisissent et la création de la fenêtre.
* La deuxième dédiée au déroulement du jeu avec les différentes contraintes et évènements selon la situation du clic. Avec d’un côté, le code du joueur 1 et de l’autre celle du joueur 2
* Et une dernière concernant la fin de la partie avec l’affichage des scores et la fermeture de la fenêtre. 




Choix techniques : 
Les premiers choix à effectuer étaient la taille de la fenêtre de l’aire de jeu et le rayon des cercles. Nous avons choisi une fenêtre de 600 x 600 px et un rayon de 30 px, ce qui permet de faire des parties suffisamment longues pour poser des stratégies tout en ayant des cercles "visibles" en cas de clic à l’intérieur d’un autre notamment.  
Nous avons décidé de faire le jeu en tour par tour en mettant toute la partie dans une boucle “while” où la valeur d’un booléen désigne à qui est le tour, en changeant à chaque itération. La boucle while à été choisie afin de pouvoir intégrer la variante “Terminaison” plus tard, en changeant simplement la valeur du nombre de tours qu’il reste. Ensuite, nous avons décidé, pour le style graphique et la cohérence lors de la partie, d’afficher à qui est-ce de jouer à tel ou tel moment en haut à gauche de la fenêtre. 
        Chaque coordonnée, à laquelle un joueur a cliqué, est enregistrée dans une liste. Cela permettra de comparer chaque clic avec les autres coordonnées pour savoir s' il touchera l’autre. Si c’est le cas, le cercle n’est pas dessiné et le tour revient à l’adversaire. Afin de pouvoir différencier chaque cercle, nous avons ajouté dans la liste des coordonnées de chaque cercle un identifiant unique qui permettra de supprimer chaque cercle sur lequel un joueur choisit de cliquer pour laisser la place aux deux autres ainsi que les rayons des cercles. 
        Nous avons pris la décision de retirer le tour du joueur si son cercle dépasse de la zone de jeu, n’avoir aucune partie de cercle en dehors de la zone de jeu facilite le comptage des points. En effet, il se fera pixel par pixel, chaque pixel coloré à la fin de la partie ajoutera un point au joueur. 
        Nous avons décidé, pour ce premier rendu, d’ajouter à notre code la variante “Sablier”. Pour ce faire, nous avons créé une fonction attente_click_jusqua() qui s’inspire d’une autre fonction de upemtk (attente_touche_jusqua()) dans le même principe la fonction attendra un click dans un temps, imparti elle retournera les coordonnées si il y a clique, sinon elle retournera None.


Problèmes rencontrés : 
        La première difficulté rencontrée était de trouver une bonne manière d’organiser le tour de chaque joueur. Quelles étapes et conditions mettre dans une fonction? Lesquelles en dehors? Ces questions nous ont mené à un long temps de réflexion pour avoir la meilleure structure possible. 
        Nous avons longtemps été bloqués à la création des cercles divisés en 2 autres, le premier créé à l’endroit du clic était plutôt simple, mais le second s’est présenté comme un obstacle difficile à surmonter. En effet, trouver le centre de ce cercle tangent à un cercle et un deuxième qui est lui même tangent à ce dernier nous a demandé énormément de temps, si ce n’est ce qui nous en a pris le plus. 
        Lorsque nous pensions que nous avions réussi à ajouter cette partie au programme, un autre problème est apparu : les boulles de l’un des joueurs s’éclatent avec succès, mais celles de l’autre le font, parfois de la bonne manière, et d’autre de la mauvaise de manière aléatoire, en mettant un petit espace entre les deux nouveaux cercles. Nous n’avons malheureusement toujours pas réussi à résoudre ce souci pour le premier rendu. [a]


**********************************    DEUXIÈME RENDU    **********************************
Pour le deuxième rendu, nous avons gardé la même structure de programme dans l’ensemble.
Tout d’abord nous arrivons sur un écran de lancement
Nous avons rajouté un menu qui nous propose trois options.
La première “Jouer” nous proposera directement de jouer au jeu sinon on peut afficher les règles du jeu, la troisième option “classement” est un bonus que nous ajouterons au prochain rendu et nous ne l’avons pas encore implémenté.
Avant de lancer une partie on nous demandera de choisir les variantes, on saisira dans le terminal si on souhaite ou non activer une variante.


Ensuite il nous sera demandé d’entrer le nom du joueur 1 et celui du joueur 2 ainsi que le nombre de manches que l’on souhaite jouer.
En fonction des variantes on peut nous demander de choisir des paramètres spécifiques à celles-ci.


Une fois les paramètres et variantes choisis, la partie peut commencer.


*** Explication des différentes variantes et comment nous les avons réaliser : ***


Sablier : Pour ce faire, nous avons créé une fonction attente_click_jusqua() qui s’inspire d’une autre fonction de upemtk (attente_touche_jusqua()) dans le même principe la fonction attendra un click dans un temps, imparti elle retournera les coordonnées si il y a clique, sinon elle retournera None et le joueur perdra alors son tour car si les coordonnées récupérées dans le programme sont égale à None ça équivaut à une perte de tour. Les joueurs choisissent la durée du sablier en début de partie.


Score : Cette variante à été compliqué à coder, car nous ne savions pas comment faire pour qu’un joueur puisse voir son score en tout instant.
Nous avons alors décidé de créer une fonction (var_score()), à chaque début de tour le joueur à 1 seconde pour afficher le score des deux joueurs sinon il peut jouer, le score s’affiche pendant deux secondes. Pour laisser le score s’afficher pendant deux secondes nous nous sommes inspirés de la fonction (attente_touche_jusqua()) qui utilise while time < t pour définir un chronomètre.


Taille des boules : A chaque fois qu’on veut poser un cercle on écrit dans le terminale la valeur du rayon du cercle que nous voulons poser. Une fois que notre réservoir est vide, on ne peut plus poser de cercle mais toujours diviser ceux de l’adversaire.


Version dynamique : Nous avons créé une fonction qui permet d'agrandir les cercles à chaque tour (agrandissement_cercles()). Afin d'arrêter l'agrandissement des cercles, nous avons créé une fonction qui vérifie si 2 cercles de couleur différente se touchent et si c’est le cas, elle le marque en ajoutant un ‘t’ dans le tag. Ensuite, la fonction agrandissement_cercles() vérifie si il y a un ‘t’ dans le tag de chaque cercle, ce qui arrête l'agrandissement de ceux-ci.


                                                           
Terminaison : Nous avons créé une variable ter qui est un booléen et à chaque fin de tour si le nombre de tour est supérieur à 5, on demande au joueur s' il veut activer la variante.
Si il clique sur la touche o la variante sera activé et ter sera changé en false  et si il clique sur la touche n la partie continue et on passe au tour suivant.
                                                
                                                                         
Obstacle : Nous avons créé une fonction obstacle, qui renvoie des coordonnées aux hasard x,y ainsi qu’un rayon au hasard entre 20 et 50.
Après la création de la fenêtre, nous générons un nombre au hasard entre 3,6 qui déterminera le nombre d’obstacles. A la création de la fenêtre un nombre d’obstacles représentés par des cercles orange sont alors créés.
                
**********************************    TROISIÈME RENDU    **********************************
Pour le troisième rendu, nous avons ajouté un menu pause permettant de choisir soit de reprendre la partie, soit de quitter ou de sauvegarder et quitter la partie. Pour sauvegarder la partie, on utilise un fichier qui contiendra un dictionnaire contenant toutes les informations dont on a besoin, la liste des cercles des joueurs et des obstacles, les noms des joueurs et le nombre de tours à l'aide de la fonction sauvegarder_partie qui prend en paramètres toutes ces données ainsi que le chemin du fichier . Afin de récupérer ces données, on utilise la fonction recup_data, qui prend en paramètre le chemin du fichier et renvoie les valeurs du dictionnaire du fichier. Afin de mettre les données dans ce fichier, nous avons décidé d’utiliser des fonctions du module JSON, notamment dump() et load() : dump() sert à encoder le dictionnaire et load() sert à le décoder. 


La deuxième variante que nous avons implémentée est la variante classement.
Pour réaliser celle-ci, on a d’abord une fonction classement() qui viendra écrire le nom de chaque joueur dans le fichier ‘fichierj.txt’ et le score de chacun dans le fichier ‘fichier_sc.txt’.
Ce qui fait que pour chaque nom dans le fichier joueur on à son score à la même ligne dans le fichier score.
Cette fonction intervient à chaque fin de partie.
Ensuite pour afficher le classement on à la fonction affiche_classement(), qui créent deux listes à partir de nos deux fichiers, on crée un dictionnaire et on parcourt tous les éléments et on crée pour chaque score une clé dans le dictionnaire qui aura pour valeur un ensemble avec les noms des joueurs ayant obtenu les dits score.
Ensuite on trie la liste des scores de manière décroissante et on ajoute ces 5 meilleurs scores a une nouvelle liste m_s (meilleure score) on affiche ensuite pour chaque score sa valeur dans le dictionnaire.
[a]modifier si on y arrive dcp