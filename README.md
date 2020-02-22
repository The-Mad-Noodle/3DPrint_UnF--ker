# 3D Print Unfucker
A failed 3D print Unfucker gcode processor by **_The Mad Noodle_**  
This software takes the gcode file of a failed 3D print and can reprocess and injects
the correct series of gcode commands to restart the print at the exact line where it failed. 
![3D Print Unfucker](https://static.wixstatic.com/media/59d0ff_8fffa2a8428f49a7a68ba5bdfdca01ec~mv2.png)
The Shame of 3D Printing Failures
-

Do you ever walk up to your 3D printer the morning of expected completion, only to find that your _**30-hour print fucked up with only 3 hours left to go**_?   

There is no worse feeling in the world. Trust me; I've dealt with it many times myself.  
Sometimes it's not something you can prevent, but it doesn't make it hurt any less. 

Most often, the only thing you can do is scrape your fucked print off of the 3D printer and take a shower (_to scrape the stink of shame and failure off of yourself_) and **start again...**   

Some more advanced 3D printing enthusiast who is more comfortable with editing gcode files can find the spot in the gcode where it failed and edit the file to start exactly where it stopped.  
Unfortunately, for most people, it's not that easy and it can be very **_intimidating and time-consuming_**. 

#### That's where the **_3D print Unfucker_** comes in.

How does it work?
-

The 3D Print Unfucker takes in a few parameters, as well as the original gcode file of your failed print, the software then parses the file removes every command from the beginning of the file to the move it failed at. Once it only has the lines that are needed, it inserts a series of gcode commands that allows the printer to start from the exact move command (G1) it left off at without the need of the standard start script that would severely interfere with the print that's on the bed. 

Using the software
-

>A more comprehensive guide on how to preform some of the these task is coming soon!

1. **Find out where your print failed**
    - Look for blobs or abruptly ending move lines
    
2. **Open the gcode in your slicer**
    - This can be tricky but use a pair of calipers to get a  
    general _Z-HEIGHT_ and idea of where to start looking
    
    - Use "Landmarks" on the 3D print and count layers from  
    there to get an exact layer number if needed
    
3. **Get the _LINE NUMBER & Z-HEIGHT_ from the slicer** 
    - We often use _Simplify 3D_, it displays the _Line Number_ next  
    to the navigation slider (Make sure _Preview by Line_ is selected NOT _Layer_)
    
    - The _Z-Height_ can be obtained through the tool heads coordinates
