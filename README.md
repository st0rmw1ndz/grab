# grab

copy common pastes to the clipboard

## usage

```
usage: grab [-h] {copy,write,rm,list} ...

copy common pastes to the clipboard

options:
  -h, --help            show this help message and exit

commands:
  {copy,write,rm,list}
    copy                copy a paste to the clipboard
    write               write a new paste
    rm                  remove a paste
    list                list all available pastes

source code: https://github.com/st0rmw1ndz/grab
```

## examples

**copying a paste to the clipboard**

```
grab.py copy character
paste 'character' copied to the clipboard
```

**writing a new paste with content**

```
grab.py write afile "a lotta content wowww"
paste 'afile' saved (size: 21 bytes)
```

**removing a paste**

```
grab.py rm anotherfile
paste 'anotherfile' removed
```

**getting the paste list**

```
grab.py list
available pastes:
 - character (size: 259 bytes)
```