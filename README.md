# mtlauncher

The worlds first ~~or so we think~~ launcher for mt that works with both 0.4x and 5.x (*just need to compile and add in the 4.x engine*).  
Written in Qt & Python, it attempts to be a clean and modern take on the launcher.  
Please note that things are still *very* pre alpha right now. It is known to work on latest arch linux.

## Installation

install pyside2, qt5 on your system. This varies from distro to distro.
On Arch Linux, use
```bash
pacman -Sy pyside2 qt5
```
Then, clone this repo into any location. /opt can be used as well. I personally use ``~/Documents/minetest/client``.
Ensure that you HOME variable is set. That is where the good stuff is stored.  

For your convenience, I have provided a pre compiled version of minetest with all source included.

## Using
On first run (~~or whenever ~/.config/mtclient/database.sqlite is non existent~~), you are prompted to create a new username and password.  
After that, you will be directed to the "go" page. You can only join remote games currently (sue me, but this only alpha).

If you are joining using a new account, the password manager will store your password in its database, and will auto retrieve it as needed.  
Effort has been taken to make the passwords somewhat secure. they are a jumble of your username & upto 2 numbers.  
The idea behind that was to provide something memorable, yet *somewhat* secure.
