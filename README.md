# mtlauncher

The worlds first ~~or so we think~~ launcher for mt that works with both 0.4x and 5.x (*just need to compile and add in the 4.x engine*).  
Written in Qt & Python, it attempts to be a clean and modern take on the launcher.  
Please note that things are still *very* pre alpha right now. It is known to work on latest arch linux.

## WARNING
Currently not working. You may help fix it if you wish.

## Installation

install pyside2, qt5 and the pyCryptoDome library on your system. This varies from distro to distro.
On Arch Linux, use
```bash
pacman -Sy pyside2 qt5 python-pycryptodome
```
Then, clone this repo into any location. /opt can be used as well. I personally use ``~/Documents/minetest/client``.
Ensure that you HOME variable is set. That is where the good stuff is stored.  

For your convenience, I have provided two pre compiled versiond of minetest with source included. One is latest stable, while the other is minetest 0.4.17.1, the last of the monetest 0.4.x series.

## Using

On first run (~~or whenever ~/.config/mtclient/database.sqlite is non existent~~), you are prompted to create a new username and password.  
After that, you will be directed to the "go" page. You can only join remote games currently (sue me, but this only alpha).

If you are joining using a new account, the password manager will store your password in its database, and will auto retrieve it as needed.  
Effort has been taken to make the passwords somewhat secure. they are a jumble of your username & upto 2 numbers.  
The idea behind that was to provide something memorable, yet *somewhat* secure.


## Engines

To plug your own engine in, compile minetest with the ``-DRUN_IN_PLACE`` commandline switch.
Place the entire directory in the ``runners`` directory. To demarcate engines, the following nomenclature is used:  
`e`+ ``< l if Linux, w if Windows >`` + ``< engine version with dots removed >``.

A few patches have been applied to the client side to tighten integration with the launcher.  

The ``exit to menu`` option & the ``exit to OS`` option now have the same meaning from the point of view of the client.

---

## Notes

If you lose your master password, there is NO way of retriving your saved passwords. KEEP IT SAFE.  
We use ChaCha20 to encrypt your passwords (via the pyCryptoDome module). The flow goes as such:

login -> We store your password in memory -> Create a new password/ save your password -> we encrypt using ChaCha20 -> we store it into the database.

login -> We store your password in memory -> You join a server -> We retrive your encrypted password from database -> We decrypt using same salt -> we store the decrypted password in memory -> minetest is launched with --password = < password > switch.

