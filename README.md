## Read me
The server I currently have for games does not support downloading workshops collections.

This script takes the modlist text file and compares it against a workshop collection.
It will then spit out any descrpancies between the too.

I will work on adding it all later.

As far as I can see the Steam API does not support a method for querying collections directly.
So what this script does, is it visits the collection id povided by the user, then pulls the links out of the dom.


#### Usage

```
python main.py --modlist [file_path] --collection id
python main.py --collection 123456789
```
