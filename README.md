# rekoCards
Some python class to read the Amiga card sets or the PC card sets. These card sets have been created since the Amiga was out there and also adapted for some PC games. The sets are still useable or could be implemented on a mobile device or wherever. There are more then 2700+ card sets available in different resolutions. Even you can make your own set using the software from R Productions.

At the moment there is no automatic solution to choosing the correct class on a file input. I added some files, so you can use it right away. During coding I tested quite a lot of the sets - all I tried work but I’m not sure the Amiga class is 100% perfect. And of course, this is fast solution, without any error handling.

Card sets can be found here:

https://www.rproductions.nl/cardgames/

or here:

https://www.rekonet.org/ (a little bit outdated but still there)

Information for the REKO or RKP files can be found inside this archive:

https://www.rekonet.org/programs/Amiga/sdiREKO-DT.lha

For the newer card set (PCRKP) I did some reverse engineering, so possible to use them too.


There are different file types:

REKO = Amiga card sets

RKP = PC card sets

For testing the card images are converted to TGA's images and saved in the output folder. (see TGA class)

The newer format containss JPG's so they are saves as JPG's of course.

